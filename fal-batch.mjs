// Batch image generation on fal.ai with local reference images.
// Usage: node tools/fal-batch.mjs <jobs.json> <outdir> [--only name1,name2] [--concurrency 3]
//   jobs.json: [{ "name": "lbp-hero", "endpoint": "fal-ai/nano-banana-pro/edit", "prompt": "...",
//                 "refs": ["path/a.jpg", ...], "params": { "aspect_ratio": "3:2", "resolution": "2K" } }, ...]
// Each job = exactly one generation request (no retries, so no double charges). References are uploaded once and
// cached in <outdir>/.ref-cache.json. Writes <outdir>/<name>.<ext> and <outdir>/<name>.result.json. Skips jobs whose
// output already exists. The key is read from ~/ace/.mcp.json and never printed.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { basename, extname, join } from "node:path";
import { fal } from "@fal-ai/client";

const args = process.argv.slice(2);
const [jobsFile, outDir] = args;
if (!jobsFile || !outDir) throw new Error("usage: node tools/fal-batch.mjs <jobs.json> <outdir> [--only a,b] [--concurrency N]");
const only = args.includes("--only") ? new Set(args[args.indexOf("--only") + 1].split(",")) : null;
const conc = args.includes("--concurrency") ? Number(args[args.indexOf("--concurrency") + 1]) : 3;
const key = JSON.parse(readFileSync(join(homedir(), "ace", ".mcp.json"), "utf8"))?.mcpServers?.fal?.env?.FAL_KEY;
if (!key) throw new Error("FAL_KEY not found");
fal.config({ credentials: key });
mkdirSync(outDir, { recursive: true });
const log = (s) => console.log(`[${new Date().toISOString().slice(11, 19)}] ${s}`);
const cachePath = join(outDir, ".ref-cache.json");
const cache = existsSync(cachePath) ? JSON.parse(readFileSync(cachePath, "utf8")) : {};
const types = { ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp" };

async function refUrl(path) {
  if (cache[path]) return cache[path];
  const buf = readFileSync(path);
  const url = await fal.storage.upload(new File([buf], basename(path), { type: types[extname(path).toLowerCase()] ?? "image/jpeg" }));
  cache[path] = url;
  writeFileSync(cachePath, JSON.stringify(cache, null, 1));
  return url;
}

const jobs = JSON.parse(readFileSync(jobsFile, "utf8")).filter((j) => !only || only.has(j.name));
const todo = jobs.filter((j) => !["png", "jpg", "jpeg", "webp"].some((e) => existsSync(join(outDir, `${j.name}.${e}`))));
log(`${jobs.length} jobs, ${todo.length} to run, concurrency ${conc}`);
// upload references sequentially first (shared across jobs)
for (const p of [...new Set(todo.flatMap((j) => j.refs ?? []))]) await refUrl(p);

let failed = 0;
async function run(job) {
  const refs = job.refs ?? [];
  const input = { prompt: job.prompt, ...(refs.length ? { image_urls: await Promise.all(refs.map(refUrl)) } : {}), ...(job.params ?? {}) };
  const t0 = Date.now();
  try {
    const r = await fal.subscribe(job.endpoint, { input, pollInterval: 2000 });
    const img = (r.data?.images ?? [])[0];
    if (!img?.url) throw new Error("no image in result");
    const res = await fetch(img.url);
    if (!res.ok) throw new Error(`download HTTP ${res.status}`);
    const ext = (img.content_type ?? "").includes("jpeg") ? "jpg" : (img.content_type ?? "").includes("webp") ? "webp" : "png";
    writeFileSync(join(outDir, `${job.name}.${ext}`), Buffer.from(await res.arrayBuffer()));
    writeFileSync(join(outDir, `${job.name}.result.json`), JSON.stringify({ endpoint: job.endpoint, requestId: r.requestId,
      seconds: (Date.now() - t0) / 1000, width: img.width, height: img.height, prompt: job.prompt, refs: job.refs, params: job.params,
      description: r.data?.description }, null, 1));
    log(`ok   ${job.name}  ${img.width}x${img.height}  ${((Date.now() - t0) / 1000).toFixed(0)} s  (${r.requestId})`);
  } catch (e) {
    failed++;
    const detail = e?.body ? JSON.stringify(e.body).slice(0, 300) : String(e?.message ?? e);
    writeFileSync(join(outDir, `${job.name}.error.json`), JSON.stringify({ endpoint: job.endpoint, error: detail }, null, 1));
    log(`FAIL ${job.name}: ${detail}`);
  }
}
const queue = [...todo];
await Promise.all(Array.from({ length: conc }, async () => { while (queue.length) await run(queue.shift()); }));
log(`done: ${todo.length - failed} ok, ${failed} failed`);

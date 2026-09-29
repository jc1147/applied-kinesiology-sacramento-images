// Batch image generation on Higgsfield with the project's SDK wrapper (run from the project root with tsx).
// Usage: npx tsx outputs/ak-sacramento/hf-batch.mts <jobs.json> <outdir> [--only a,b] [--concurrency 2]
//   jobs.json: [{ "name": "...", "model": "higgsfield-ai/soul/v2/standard", "input": { "prompt": "...", ... } }, ...]
// Each job = one generation request, no retries. Gets a free quote first (/estimate) and records it with the request
// id, so every render can be matched to the console. Skips jobs whose output already exists. Key never printed.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { higgsfield } from "@higgsfield/client/v2";
import { download, estimate, imageUrl, loadCredentials, outputUrls } from "../../src/higgsfield.ts";

const args = process.argv.slice(2);
const [jobsFile, outDir] = args;
const only = args.includes("--only") ? new Set(args[args.indexOf("--only") + 1].split(",")) : null;
const conc = args.includes("--concurrency") ? Number(args[args.indexOf("--concurrency") + 1]) : 2;
loadCredentials();
mkdirSync(outDir, { recursive: true });
const log = (s: string) => console.log(`[${new Date().toISOString().slice(11, 19)}] ${s}`);
type Job = { name: string; model: string; input: Record<string, unknown>; images?: string[] };
const jobs = (JSON.parse(readFileSync(jobsFile, "utf8")) as Job[]).filter((j) => !only || only.has(j.name));
const todo = jobs.filter((j) => !["png", "jpg", "jpeg", "webp"].some((e) => existsSync(join(outDir, `${j.name}.${e}`))));
log(`${jobs.length} jobs, ${todo.length} to run, concurrency ${conc}`);
let failed = 0;

async function run(job: Job) {
  const t0 = Date.now();
  if (job.images?.length) job.input.image_urls = await Promise.all(job.images.map((p) => imageUrl(p)));  // local refs -> Higgsfield storage
  let quote = "";
  try { quote = await estimate(job.model, job.input); } catch (e) { quote = `estimate failed: ${String((e as Error).message).slice(0, 120)}`; }
  try {
    const result = await higgsfield.subscribe(job.model, { input: job.input, withPolling: true });
    const { requestId, urls } = outputUrls(result, "images");
    const file = await download(urls[0], outDir, job.name);
    writeFileSync(join(outDir, `${job.name}.result.json`), JSON.stringify({ model: job.model, requestId, quote,
      seconds: (Date.now() - t0) / 1000, file, input: job.input }, null, 1));
    log(`ok   ${job.name}  ${((Date.now() - t0) / 1000).toFixed(0)} s  ${quote}  (${requestId})`);
  } catch (e) {
    failed++;
    writeFileSync(join(outDir, `${job.name}.error.json`), JSON.stringify({ model: job.model, quote, error: String((e as Error).message) }, null, 1));
    log(`FAIL ${job.name}: ${String((e as Error).message).slice(0, 300)}`);
  }
}
const queue = [...todo];
await Promise.all(Array.from({ length: conc }, async () => { while (queue.length) await run(queue.shift()!); }));
log(`done: ${todo.length - failed} ok, ${failed} failed`);

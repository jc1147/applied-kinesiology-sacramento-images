// Free estimates (no generation) for candidate Higgsfield image models; the key is never printed.
import { estimate, loadCredentials } from "../../src/higgsfield.ts";
loadCredentials();
const prompt = "A cinematic photograph of a chiropractic treatment room";
const cands: [string, Record<string, unknown>][] = [
  ["higgsfield-ai/soul/standard", { prompt, aspect_ratio: "3:2", resolution: "1080p" }],
  ["higgsfield-ai/soul/v2/standard", { prompt, aspect_ratio: "3:2" }],
  ["marketing-studio/image/flare", { prompt, quality: "high", resolution: "2k", aspect_ratio: "3:2" }],
  ["marketing-studio/image/sunburst", { prompt, quality: "high", resolution: "2k", aspect_ratio: "3:2" }],
  ["flux-pro/kontext/max/text-to-image", { prompt, aspect_ratio: "3:2" }],
  ["google/nano-banana-pro", { prompt, aspect_ratio: "3:2" }],
  ["bytedance/seedream/v4/text-to-image", { prompt, aspect_ratio: "3:2" }],
];
for (const [m, input] of cands) {
  try { console.log(`${m}: ${await estimate(m, input)}`); }
  catch (e) { console.log(`${m}: ERROR ${String((e as Error).message).slice(0, 160)}`); }
}

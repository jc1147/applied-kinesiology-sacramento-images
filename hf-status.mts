// Print the status payload fields (not the key) for a few request ids, to see whether actual cost is reported.
import { loadCredentials } from "../../src/higgsfield.ts";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { parseEnv } from "node:util";
loadCredentials();
const cred = process.env.HF_CREDENTIALS!;
for (const id of process.argv.slice(2)) {
  const r = await fetch(`https://api.higgsfield.ai/requests/${id}/status`, { headers: { Authorization: `Key ${cred}` } });
  const j = await r.json() as Record<string, unknown>;
  const redacted = JSON.parse(JSON.stringify(j, (k, v) => (typeof v === "string" && v.startsWith("http") ? "<url>" : v)));
  console.log(id, r.status, JSON.stringify(redacted).slice(0, 900));
}

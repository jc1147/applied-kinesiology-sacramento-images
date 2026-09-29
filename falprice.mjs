// Query fal's pricing API for a list of endpoints (key read from ~/ace/.mcp.json, never printed).
import { readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
const key = JSON.parse(readFileSync(join(homedir(), "ace", ".mcp.json"), "utf8"))?.mcpServers?.fal?.env?.FAL_KEY;
const ids = process.argv.slice(2);
const u = "https://api.fal.ai/v1/models/pricing?" + ids.map((i) => "endpoint_id=" + encodeURIComponent(i)).join("&");
const r = await fetch(u, { headers: { Authorization: `Key ${key}` } });
console.log(r.status);
console.log(JSON.stringify(await r.json(), null, 1).slice(0, 3000));

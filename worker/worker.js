// AI Skills Without Borders: website submissions, without a GitHub account.
//
// The site's Share page posts here. This Worker checks the visitor is a person (Cloudflare Turnstile),
// checks the fields against the forms the site publishes (forms.json, built from the GitHub issue forms),
// and opens the GitHub issue with the same layout a GitHub form would produce. The repository's
// automation does the rest, exactly as for GitHub submissions.
//
// Settings (Cloudflare dashboard → the Worker → Settings → Variables and Secrets):
//   GITHUB_TOKEN      secret. Fine-grained token, this repository only, permission Issues: read and write.
//   TURNSTILE_SECRET  secret. The Turnstile widget's secret key.
//   REPO              text. ai-skills-without-borders/skills
//   SITE              text. https://ai-skills-without-borders.github.io/skills/
// Optional: a KV namespace bound as LIMITS, for a per-address limit (5 submissions an hour).
// Optional: a KV namespace bound as FILES, to accept uploaded .skill / .zip files (kept 60 days, served
//           at /file/<id>.zip for the repository's automation to fetch).

const MAX_BODY = 60000;            // GitHub allows 65,536 characters in an issue body
const MAX_FILE = 5 * 1024 * 1024;  // uploaded skill files
const PER_HOUR = 5;

export default {
  async fetch(req, env) {
    const origin = req.headers.get("Origin") || "";
    const allowed = new URL(env.SITE).origin;
    const cors = {
      "Access-Control-Allow-Origin": origin === allowed ? origin : allowed,
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Vary": "Origin",
    };
    const reply = (status, obj) => new Response(JSON.stringify(obj), { status, headers: { ...cors, "Content-Type": "application/json" } });

    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    const path = new URL(req.url).pathname;
    const fm = path.match(/^\/file\/([0-9a-f-]{36})\.zip$/);
    if (req.method === "GET" && fm && env.FILES) {
      const bytes = await env.FILES.get(fm[1], { type: "arrayBuffer" });
      if (!bytes) return new Response("Not found.", { status: 404 });
      return new Response(bytes, { headers: { "Content-Type": "application/zip", "Content-Disposition": `attachment; filename="${fm[1]}.zip"` } });
    }
    if (req.method !== "POST" || path !== "/submit") return reply(404, { error: "Not found." });
    if (origin !== allowed) return reply(403, { error: "Submissions are accepted from the library's site only." });

    const raw = await req.text();
    if (raw.length > MAX_BODY + MAX_FILE * 1.4) return reply(413, { error: "That is too large for one submission. Please send it by email." });
    let data;
    try { data = JSON.parse(raw); } catch { return reply(400, { error: "The form could not be read. Please try again." }); }
    if (data.website) return reply(200, { ok: true });   // honeypot: a field people never see

    const ip = req.headers.get("CF-Connecting-IP") || "";
    const human = await verifyTurnstile(env, data.token, ip);
    if (!human) return reply(403, { error: "The check that you are a person didn't pass. Reload the page and try again." });

    if (env.LIMITS && ip) {
      const key = "n:" + ip + ":" + new Date().toISOString().slice(0, 13);
      const n = parseInt((await env.LIMITS.get(key)) || "0", 10);
      if (n >= PER_HOUR) return reply(429, { error: "Too many submissions from this address. Please try again in an hour." });
      await env.LIMITS.put(key, String(n + 1), { expirationTtl: 3700 });
    }

    const schema = await (await fetch(env.SITE + "forms.json", { cf: { cacheTtl: 300 } })).json();
    const form = schema[data.form];
    if (!form) return reply(400, { error: "Unknown form." });
    const values = data.fields || {};
    const problems = [];
    const lines = [];
    for (const f of form.fields) {
      let v = values[f.id];
      if (f.type === "checkboxes") {
        const ticked = Array.isArray(v) ? v : [];
        if (ticked.some(t => !f.options.includes(t))) problems.push(f.label);
        lines.push(`### ${f.label}`, "", ...f.options.map(o => `- [${ticked.includes(o) ? "X" : " "}] ${o}`), "");
        continue;
      }
      v = typeof v === "string" ? v.replace(/\r\n/g, "\n").trim() : "";
      if (f.required && !v) problems.push(f.label);
      if (f.type === "dropdown" && v && !f.options.includes(v)) problems.push(f.label);
      if (f.type === "input" && v.length > 300) problems.push(f.label);
      lines.push(`### ${f.label}`, "", v ? escapeMentions(v) : "_No response_", "");
    }
    if (problems.length) return reply(400, { error: "Please check: " + problems.join("; ") + "." });
    if (data.file && data.form === "new-skill") {
      if (!env.FILES) return reply(400, { error: "File uploads aren't switched on yet. Please paste the instructions instead." });
      const name = String(data.file.name || "");
      let bytes;
      try { bytes = Uint8Array.from(atob(String(data.file.b64 || "")), c => c.charCodeAt(0)); } catch { bytes = new Uint8Array(); }
      const isZip = bytes.length > 4 && bytes[0] === 0x50 && bytes[1] === 0x4b && bytes[2] === 0x03 && bytes[3] === 0x04;
      if (!/\.(skill|zip)$/i.test(name) || !isZip) return reply(400, { error: "The file should be a .skill or .zip file exported from your AI tool." });
      if (bytes.length > MAX_FILE) return reply(413, { error: "The file is larger than 5 MB. Please send it by email." });
      const id = crypto.randomUUID();
      await env.FILES.put(id, bytes, { expirationTtl: 60 * 24 * 3600 });
      lines.push("### Skill file", "", `${new URL(req.url).origin}/file/${id}.zip`, "");
    } else if (data.form === "new-skill" && !(values.instructions || "").trim()) {
      return reply(400, { error: "Please paste the instructions, or upload the .skill file." });
    }
    lines.push("### Submitted via", "", "The library's website (no GitHub account).", "");
    if (lines.join("\n").length > MAX_BODY) return reply(413, { error: "That is too long for one submission. Upload the .skill file instead of pasting, or send it by email." });

    const pick = id => (values[id] || "").toString().replace(/\s*\([a-z0-9-]+\)$/, "").slice(0, 80);
    const title = form.title.replace("<skill>", pick("skill")).replace("<tool>", pick("tool")).replace("<name>", pick("name"));
    const res = await fetch(`https://api.github.com/repos/${env.REPO}/issues`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
        "Accept": "application/vnd.github+json",
        "User-Agent": "ai-skills-without-borders-forms",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title, body: lines.join("\n"), labels: [...form.labels, "via-website"] }),
    });
    if (!res.ok) return reply(502, { error: "The submission couldn't be filed just now. Please try again later, or send it by email." });
    const issue = await res.json();
    return reply(200, { ok: true, url: issue.html_url, number: issue.number });
  },
};

async function verifyTurnstile(env, token, ip) {
  if (!token) return false;
  const body = new FormData();
  body.append("secret", env.TURNSTILE_SECRET);
  body.append("response", token);
  if (ip) body.append("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body });
  const j = await r.json();
  return j.success === true;
}

// "@someone" in a submission would notify that GitHub user; break the mention.
function escapeMentions(s) {
  return s.replace(/(^|\s)@(?=[A-Za-z0-9-])/g, "$1@​");
}

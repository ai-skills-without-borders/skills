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

const MAX_BYTES = 60000;     // GitHub allows 65,536 characters in an issue body
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
    if (req.method !== "POST" || new URL(req.url).pathname !== "/submit") return reply(404, { error: "Not found." });
    if (origin !== allowed) return reply(403, { error: "Submissions are accepted from the library's site only." });

    const raw = await req.text();
    if (raw.length > MAX_BYTES) return reply(413, { error: "That is too long for one submission. Shorten the instructions, or send them by email." });
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
    lines.push("### Submitted via", "", "The library's website (no GitHub account).", "");

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

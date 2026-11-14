<script>
(function () {
  const { esc, GH, TOOLS } = window.ASBsite;
  const CATALOG = window.ASB_CATALOG || [];
  const LADDER = ["draft", "tested-at-origin", "tested-elsewhere", "reviewed"];
  const LABEL = { "draft": "Draft", "tested-at-origin": "Tested at origin", "tested-elsewhere": "Tested elsewhere", "reviewed": "Reviewed" };
  const STATE = { "untested": "not yet tested", "works": "works", "works-with-limits": "works, with limits", "broken": "broken" };
  const USERS = { "educators": "Educators", "learners": "Learners", "program-staff": "Program staff" };
  const hay = c => [c.name, c.title, c.summary, c.description, ...(c.tasks || []), ...(c.audience || []), ...(c.frameworks || [])].join(" ").toLowerCase();
  // Search in the user's own words: ignore filler words, accept common synonyms and word endings,
  // and rank skills by how many of the words they match instead of requiring every word.
  const STOP = new Set("a an and are as at be by can do for from have help how i in into is it me my need of on or our please should some that the their them these this to want we what which with you your".split(" "));
  const SYN = [
    ["improve", "fix", "rewrite", "revise", "better", "check", "review", "edit", "update"],
    ["write", "create", "draft", "make", "build", "generate", "design", "prepare", "plan"],
    ["objective", "objectives", "outcome", "outcomes", "goal", "goals", "aim", "aims"],
    ["exam", "exams", "question", "questions", "item", "items", "mcq", "test", "quiz", "assessment"],
    ["syllabus", "syllabi", "outline", "course"],
    ["reading", "readings", "paper", "article", "chapter", "pre-reading"],
    ["session", "lesson", "class", "lecture", "seminar", "pbl", "rbl", "case"],
    ["mentor", "mentoring", "mentee", "advisor", "advising", "compact"],
    ["committee", "thesis", "meeting", "meetings"],
    ["journal", "club", "paper"],
    ["notebook", "notebooks", "format", "jupyter"],
    ["calendar", "schedule", "timeline", "dates"],
    ["grant", "t32", "mstp", "application", "renewal"],
    ["map", "mapping", "competency", "competencies", "epa", "epas", "framework", "curriculum"],
    ["feedback", "communication", "leadership"]
  ];
  const stem = w => w.length > 4 ? w.replace(/(ing|ed|es|s)$/, "") : w;
  const alts = w => { const out = new Set([w, stem(w)]); SYN.forEach(g => { if (g.includes(w) || g.includes(stem(w))) g.forEach(x => { out.add(x); out.add(stem(x)); }); }); return [...out]; };
  const FIELDS = c => [[c.title + " " + c.name, 6], [[c.summary, ...(c.tasks || [])].join(" "), 3], [hay(c), 1]].map(([t, wgt]) => [t.toLowerCase(), wgt]);
  // A word scores by where it appears (title > summary and tasks > anywhere) and whether it matched as typed or as a synonym.
  function wordScore(fs, w) {
    let best = 0;
    for (const [t, wgt] of fs) {
      if (t.includes(w) || t.includes(stem(w))) best = Math.max(best, wgt);
      else if (alts(w).some(a => t.includes(a))) best = Math.max(best, wgt * 0.5);
    }
    return best;
  }
  function score(c, words) { const fs = FIELDS(c); const per = words.map(w => wordScore(fs, w)); return [per.filter(x => x > 0).length, per.reduce((a, b) => a + b, 0)]; }
  function render() {
    const q = document.getElementById("q").value.trim().toLowerCase();
    const words = q.split(/[^a-z0-9-]+/).filter(w => w && !STOP.has(w));
    const u = (document.querySelector('#users [aria-pressed="true"]') || {}).dataset?.u || "";
    const scored = CATALOG.filter(c => !u || (c.users || []).includes(u)).map(c => [c, words.length ? score(c, words) : [1, 0]]).filter(([, n]) => n[0] > 0);
    const best = Math.max(0, ...scored.map(([, n]) => n[0]));
    const items = scored.sort((a, b) => (b[1][0] - a[1][0]) || (b[1][1] - a[1][1]) || (b[0].starter - a[0].starter) || a[0].title.localeCompare(b[0].title)).map(([c]) => c);
    const list = document.getElementById("list");
    const note = document.getElementById("closest");
    if (note) note.hidden = !(words.length && items.length && best < words.length);
    if (!items.length) {
      list.innerHTML = `<p class="empty">No skill matches${q ? ` “${esc(q)}”` : ""}${u ? ` for ${esc(USERS[u].toLowerCase())}` : ""}. Try other words, browse <a href="skills.html" onclick="document.getElementById('q').value='';">all skills</a>, or <a href="${GH}/issues/new?template=new-skill.yml">propose a skill for this task</a>.</p>`;
      return;
    }
    list.innerHTML = items.map(c => {
      const lvl = LADDER.indexOf(c.maturity);
      const steps = LADDER.map((_, i) => `<i class="${i <= lvl ? "on" : ""}"></i>`).join("");
      const tested = Object.entries(c.tested_in || {}).map(([t, s]) => `<span class="${s === "works" ? "works" : ""}">${esc(TOOLS[t] ? TOOLS[t].name : t)}: ${esc(STATE[s] || s)}</span>`).join("");
      const li = a => (a || []).map(x => `<li>${esc(x)}</li>`).join("");
      const nv = (c.variants || []).length;
      return `<article class="skill" id="skill-${c.name}">
        <div class="row">
          <div class="titleline"><span class="sk-badge">${c.icon}</span><div><h3><a href="skills/${esc(c.name)}.html">${esc(c.title)}</a>${c.starter ? `<span class="starter-note">Start here</span>` : ""}${nv ? `<span class="variants-note">${nv} institutional variant${nv > 1 ? "s" : ""}</span>` : ""}</h3><p>${esc(c.summary)}</p><p class="for">For ${esc((c.users || []).map(x => USERS[x] || x).join(", ").toLowerCase())}</p></div></div>
          <div class="ladder" aria-label="Maturity: ${LABEL[c.maturity]}"><div class="steps">${steps}</div><span>${LABEL[c.maturity]}${c.runs_code ? " · optional scripts" : ""}</span></div>
          <button class="toggle" type="button" aria-expanded="false" aria-controls="d-${c.name}" aria-label="Show details for ${esc(c.title)}">+</button>
        </div>
        <div class="detail" id="d-${c.name}" hidden>
          <div><h4>Use it to</h4><ul>${li(c.tasks)}</ul></div>
          <div><h4>You bring</h4><ul>${li(c.inputs)}</ul></div>
          <div><h4>You get</h4><ul>${li(c.outputs)}</ul></div>
          <div class="wide"><h4>Tested in</h4><div class="tested">${tested}</div></div>
          <div class="wide actions">
            <a class="btn primary" href="${esc(c.zip)}" download>Download ZIP</a>
            <a class="btn plain" href="${esc(c.paste)}">Paste-in version</a>
            <a class="btn plain" href="skills/${esc(c.name)}.html">Full skill page</a>
          </div>
        </div>
      </article>`;
    }).join("");
    list.querySelectorAll(".toggle").forEach(b => b.addEventListener("click", () => {
      const open = b.getAttribute("aria-expanded") !== "true";
      b.setAttribute("aria-expanded", open);
      b.textContent = open ? "−" : "+";
      document.getElementById(b.getAttribute("aria-controls")).hidden = !open;
    }));
  }
  const params = new URLSearchParams(location.search);
  if (params.get("q")) document.getElementById("q").value = params.get("q");
  document.getElementById("q").addEventListener("input", render);
  document.querySelectorAll("#users button").forEach(b => b.addEventListener("click", () => {
    document.querySelectorAll("#users button").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
    render();
  }));
  if (params.get("for")) { const b = document.querySelector(`#users [data-u="${params.get("for")}"]`); if (b) b.click(); }
  render();
})();
</script>

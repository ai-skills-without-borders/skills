<script>
(function () {
  const { esc, GH, TOOLS } = window.ASBsite;
  const CATALOG = window.ASB_CATALOG || [];
  const LADDER = ["draft", "tested-at-origin", "tested-elsewhere", "reviewed"];
  const LABEL = { "draft": "Draft", "tested-at-origin": "Tested at origin", "tested-elsewhere": "Tested elsewhere", "reviewed": "Reviewed" };
  const STATE = { "untested": "not yet tested", "works": "works", "works-with-limits": "works, with limits", "broken": "broken" };
  const USERS = { "educators": "Educators", "learners": "Learners", "program-staff": "Program staff" };
  const hay = c => [c.name, c.title, c.summary, c.description, ...(c.tasks || []), ...(c.audience || []), ...(c.frameworks || [])].join(" ").toLowerCase();
  function render() {
    const q = document.getElementById("q").value.trim().toLowerCase();
    const words = q.split(/\s+/).filter(Boolean);
    const u = (document.querySelector('#users [aria-pressed="true"]') || {}).dataset?.u || "";
    const items = CATALOG.filter(c => words.every(w => hay(c).includes(w)) && (!u || (c.users || []).includes(u))).sort((a, b) => (b.starter - a.starter) || a.title.localeCompare(b.title));
    const list = document.getElementById("list");
    if (!items.length) {
      list.innerHTML = `<p class="empty">No skill matches${q ? ` “${esc(q)}”` : ""}${u ? ` for ${esc(USERS[u].toLowerCase())}` : ""}. Try a shorter phrase, or <a href="${GH}/issues/new?template=new-skill.yml">propose a skill for this task</a>.</p>`;
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

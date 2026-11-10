// Shared helpers for every page: escaping, tool choice, install instructions.
(function () {
  const C = window.ASB || {};
  const GH = `https://github.com/${C.repo || ""}`;
  function esc(s) { return String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
  const TOOLS = {
    claude: { name: "Claude", how: () => `<strong>Claude</strong>Download the skill's ZIP, then in Claude open Customize → Skills → + → Upload a skill. Switch it on after uploading. Claude Code: <code>/plugin marketplace add ${esc(C.repo)}</code>, then <code>/plugin install ${esc(C.plugin_name)}@${esc(C.plugin_name)}</code>.` },
    chatgpt: { name: "ChatGPT", how: () => `<strong>ChatGPT Business, Enterprise or Edu</strong>Download the skill's ZIP, then Skills → Create → Upload from your computer. Your workspace admin decides who can upload and share skills. On Free or Plus, use the paste-in version in a custom GPT.` },
    gemini: { name: "Gemini", how: () => `<strong>Gemini Enterprise</strong>Download the ZIP, then Skills → + → Upload. In the regular Gemini app, use the paste-in version as the instructions of a Gem.` },
    copilot: { name: "Copilot", how: () => `<strong>Microsoft 365 Copilot</strong>Unzip the skill and put its folder in your OneDrive under Documents/Cowork/Skills/, then start a new Cowork conversation. Copilot Studio agents accept an uploaded skill. Both need a Copilot license.` },
    free: { name: "Free plan", how: () => `<strong>Any assistant without skills</strong>Open the paste-in version, paste the Instructions into a GPT, Gem or Project (or at the start of a chat), and add the reference files as knowledge files.` },
  };
  let tool = "claude";
  try { tool = localStorage.getItem("asb-tool") || "claude"; } catch (e) {}
  if (!TOOLS[tool]) tool = "claude";
  const listeners = [];
  function renderToolPicker() {
    const box = document.getElementById("tools");
    if (box) {
      box.innerHTML = Object.entries(TOOLS).map(([k, t]) => `<button type="button" data-tool="${k}" aria-pressed="${k === tool}">${t.name}</button>`).join("");
      box.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
        tool = b.dataset.tool;
        try { localStorage.setItem("asb-tool", tool); } catch (e) {}
        renderToolPicker();
        listeners.forEach(f => f(tool));
      }));
    }
    const inst = document.getElementById("install");
    if (inst) inst.innerHTML = TOOLS[tool].how();
  }
  window.ASBsite = { esc, GH, TOOLS, getTool: () => tool, onTool: f => listeners.push(f), renderToolPicker };
  document.addEventListener("DOMContentLoaded", renderToolPicker);

  // Sticky header. On narrow screens the brand and menu row tucks away while scrolling down.
  const top = document.querySelector(".top");
  const narrow = window.matchMedia("(max-width: 1099.98px)");
  const navRow = top ? top.querySelector(":scope > .wrap") : null;
  function setTopH() {
    if (!top) return;
    document.documentElement.style.setProperty("--top-h", top.offsetHeight + "px");
    document.documentElement.style.setProperty("--nav-h", (navRow ? navRow.offsetHeight : 0) + "px");
  }
  const visibleTop = () => (top ? Math.max(0, top.getBoundingClientRect().bottom) : 0);
  let lastY = window.scrollY, jumping = false;
  function tuck() {
    if (!top || jumping) { lastY = window.scrollY; return; }
    const y = window.scrollY, open = top.querySelector('.pagebar button[aria-expanded="true"]');
    if (!narrow.matches || y < 160 || open) top.classList.remove("tuck");
    else if (y > lastY + 6) top.classList.add("tuck");
    else if (y < lastY - 6) top.classList.remove("tuck");
    lastY = y;
  }
  window.addEventListener("scroll", tuck, { passive: true });
  // Jump to a section so its heading lands just below whatever header is visible on arrival.
  function jumpTo(h) {
    const y = h.getBoundingClientRect().top + window.scrollY;
    const down = y > window.scrollY;
    const tucked = narrow.matches && down && y > 160;
    top.classList.toggle("tuck", tucked);
    const headerH = top.offsetHeight - (tucked ? (navRow ? navRow.offsetHeight : 0) : 0);
    jumping = true;
    window.scrollTo({ top: Math.max(0, y - headerH - 14), behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
    history.replaceState(null, "", `#${h.id}`);
    clearTimeout(jumpTo.t); jumpTo.t = setTimeout(() => { jumping = false; lastY = window.scrollY; }, 900);
    h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true });
  }

  // Page map for long pages: a rail on the left on wide screens, a bar under the header on narrow ones.
  function pageMap() {
    const main = document.querySelector("main");
    if (!main || !top || main.querySelector(".hero")) return;
    const hs = [...main.querySelectorAll("h2")].filter(h => h.textContent.trim());
    if (hs.length < 4) return;
    const used = new Set([...document.querySelectorAll("[id]")].map(el => el.id));
    hs.forEach(h => {
      if (h.id) return;
      let base = h.textContent.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "section";
      let id = base, n = 2;
      while (used.has(id)) id = `${base}-${n++}`;
      used.add(id); h.id = id;
    });
    const list = () => `<ol>${hs.map(h => `<li><a href="#${h.id}">${esc(h.textContent.trim())}</a></li>`).join("")}</ol>`;
    const rail = document.createElement("nav");
    rail.className = "pagemap pm-rail"; rail.setAttribute("aria-label", "On this page");
    rail.innerHTML = `<p class="pm-title">On this page</p>${list()}`;
    document.body.appendChild(rail);
    const bar = document.createElement("div");
    bar.className = "pagebar wrap";
    bar.innerHTML = `<button type="button" aria-expanded="false" aria-controls="pagebar-list"><span class="pb-label">On this page:</span><span class="pb-current"></span><span class="pb-caret" aria-hidden="true">▾</span></button>
      <nav class="pagemap" id="pagebar-list" aria-label="On this page" hidden>${list()}</nav>`;
    top.appendChild(bar);
    document.body.classList.add("has-map");
    const btn = bar.querySelector("button"), drop = bar.querySelector(".pagemap"), cur = bar.querySelector(".pb-current");
    const close = () => { btn.setAttribute("aria-expanded", "false"); drop.hidden = true; };
    btn.addEventListener("click", () => { const open = drop.hidden; drop.hidden = !open; btn.setAttribute("aria-expanded", String(open)); });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && !drop.hidden) { close(); btn.focus(); } });
    document.addEventListener("click", e => { if (!drop.hidden && !bar.contains(e.target)) close(); });
    const links = [...document.querySelectorAll(".pagemap a")];
    links.forEach(a => a.addEventListener("click", e => {
      const h = document.getElementById(a.getAttribute("href").slice(1));
      if (!h) return;
      e.preventDefault(); close(); jumpTo(h);
    }));
    function spy() {
      const line = visibleTop() + 40;
      let i = 0;
      hs.forEach((h, k) => { if (h.getBoundingClientRect().top <= line) i = k; });
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) i = hs.length - 1;
      links.forEach(a => a.setAttribute("aria-current", String(a.getAttribute("href") === `#${hs[i].id}`)));
      cur.textContent = hs[i].textContent.trim();
      const active = rail.querySelector('a[aria-current="true"]');
      if (active && rail.scrollHeight > rail.clientHeight) {
        const r = active.offsetTop - rail.clientHeight / 2;
        if (Math.abs(rail.scrollTop - r) > rail.clientHeight / 3) rail.scrollTop = r;
      }
    }
    let ticking = false;
    window.addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { spy(); ticking = false; }); } }, { passive: true });
    window.addEventListener("resize", spy);
    spy();
  }
  // Tabs (first-contribution guide): click or arrow keys switch panels.
  function tabs() {
    document.querySelectorAll('[role="tablist"]').forEach(list => {
      const ts = [...list.querySelectorAll('[role="tab"]')];
      const show = t => {
        ts.forEach(x => {
          const on = x === t;
          x.setAttribute("aria-selected", String(on));
          x.tabIndex = on ? 0 : -1;
          document.getElementById(x.getAttribute("aria-controls")).hidden = !on;
        });
      };
      ts.forEach((t, i) => {
        t.addEventListener("click", () => show(t));
        t.addEventListener("keydown", ev => {
          const d = ev.key === "ArrowRight" ? 1 : ev.key === "ArrowLeft" ? -1 : 0;
          if (!d) return;
          const n = ts[(i + d + ts.length) % ts.length];
          show(n); n.focus(); ev.preventDefault();
        });
      });
    });
  }
  document.addEventListener("DOMContentLoaded", () => { tabs(); pageMap(); setTopH(); });
  window.addEventListener("resize", setTopH);
  window.addEventListener("load", setTopH);
})();

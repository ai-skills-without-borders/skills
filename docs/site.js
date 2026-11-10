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
})();

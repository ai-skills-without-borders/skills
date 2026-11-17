// Share page: two forms that go to the library's Worker, which files them on GitHub.
(function () {
  const cfg = window.ASB_FORMS || {};
  const tabs = [...document.querySelectorAll('.share-tabs [role="tab"]')];
  function select(tab) {
    tabs.forEach(t => {
      const on = t === tab;
      t.setAttribute("aria-selected", on);
      document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
    });
  }
  tabs.forEach(t => t.addEventListener("click", () => { select(t); history.replaceState(null, "", "#" + (t.id === "tab-skill" ? "skill" : "report")); }));
  if (location.hash === "#skill") select(document.getElementById("tab-skill"));

  // ?skill=<folder> preselects the skill in the report form.
  const want = new URLSearchParams(location.search).get("skill");
  if (want) {
    const sel = document.querySelector('[data-form="usage-report"] select[name="skill"]');
    const opt = sel && [...sel.options].find(o => o.value.endsWith("(" + want + ")"));
    if (opt) sel.value = opt.value;
  }

  const forms = [...document.querySelectorAll(".share-form")];
  if (!cfg.endpoint) {
    forms.forEach(f => f.querySelectorAll("input, select, textarea, button").forEach(x => x.disabled = true));
    return;
  }
  window.asbTurnstile = () => {
    document.querySelectorAll(".share-form .turnstile").forEach(el => window.turnstile.render(el, { sitekey: cfg.sitekey }));
  };

  forms.forEach(form => form.addEventListener("submit", async ev => {
    ev.preventDefault();
    const status = form.querySelector(".send-status");
    const button = form.querySelector('button[type="submit"]');
    const missing = [...form.querySelectorAll("[required]")].filter(x => !x.value.trim());
    form.querySelectorAll(".invalid").forEach(x => x.classList.remove("invalid"));
    if (missing.length) {
      missing.forEach(x => x.classList.add("invalid"));
      missing[0].focus();
      status.textContent = "Please fill in the fields marked *.";
      return;
    }
    const fields = {};
    form.querySelectorAll("input[name], select[name], textarea[name]").forEach(x => {
      if (x.name === "website" || x.name === "cf-turnstile-response") return;
      if (x.type === "checkbox") { (fields[x.name] = fields[x.name] || []); if (x.checked) fields[x.name].push(x.value); }
      else fields[x.name] = x.value;
    });
    const token = (form.querySelector('[name="cf-turnstile-response"]') || {}).value || "";
    button.disabled = true;
    status.textContent = "Sending…";
    try {
      const r = await fetch(cfg.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ form: form.dataset.form, fields, token, website: form.querySelector('[name="website"]').value }),
      });
      const j = await r.json().catch(() => ({}));
      if (!r.ok || !j.ok) throw new Error(j.error || "The submission couldn't be sent. Please try again.");
      form.innerHTML = `<div class="share-done"><h3>Thank you, it's on its way.</h3><p>${form.dataset.form === "usage-report"
        ? "Your report is being recorded; the skill's page updates within a few minutes."
        : "A maintainer will review your skill, usually within a few days; it then appears in the catalog as a Draft."}</p>` +
        (j.url ? `<p>You can follow it here: <a href="${j.url}">${j.url.replace("https://", "")}</a></p>` : "") + "</div>";
    } catch (e) {
      status.textContent = e.message;
      button.disabled = false;
      if (window.turnstile) window.turnstile.reset(form.querySelector(".turnstile"));
    }
  }));
})();

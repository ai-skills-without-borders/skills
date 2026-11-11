// Workshop slides: keyboard, buttons, swipe, speaker notes, full screen, print.
(function () {
  const slides = [...document.querySelectorAll(".slide")];
  if (!slides.length) return;
  const body = document.body;
  const notes = document.createElement("div");
  notes.className = "notes-box";
  notes.setAttribute("aria-live", "polite");
  document.body.appendChild(notes);
  let cur = 0;

  function fit() {
    const st = document.querySelector(".stage").getBoundingClientRect();
    const room = body.classList.contains("notes") ? st.height * 0.68 : st.height;
    const s = Math.min((st.width - 24) / 1280, (room - 24) / 720);
    document.documentElement.style.setProperty("--scale", Math.max(0.1, s).toFixed(4));
  }
  function show(i) {
    cur = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, k) => s.classList.toggle("on", k === cur));
    notes.innerHTML = slides[cur].querySelector(".sl-notes").innerHTML;
    history.replaceState(null, "", "#" + (cur + 1));
  }
  function toggleNotes() {
    body.classList.toggle("notes");
    document.querySelector('[data-act="notes"]').setAttribute("aria-pressed", body.classList.contains("notes"));
    fit();
  }
  function full() {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen?.().catch(() => {});
    else document.exitFullscreen?.();
  }
  document.addEventListener("fullscreenchange", () => { body.classList.toggle("full", !!document.fullscreenElement); fit(); });
  document.addEventListener("keydown", ev => {
    if (ev.altKey || ev.ctrlKey || ev.metaKey) return;
    const k = ev.key;
    if (["ArrowRight", "PageDown", " ", "Enter"].includes(k)) { ev.preventDefault(); show(cur + 1); }
    else if (["ArrowLeft", "PageUp", "Backspace"].includes(k)) { ev.preventDefault(); show(cur - 1); }
    else if (k === "Home") show(0);
    else if (k === "End") show(slides.length - 1);
    else if (k === "n" || k === "N") toggleNotes();
    else if (k === "f" || k === "F") full();
    else if (k === "p" || k === "P") window.print();
  });
  document.querySelectorAll(".deck-btns button").forEach(b => b.addEventListener("click", () => {
    ({ prev: () => show(cur - 1), next: () => show(cur + 1), notes: toggleNotes, full })[b.dataset.act]();
  }));
  let x0 = null;
  document.querySelector(".stage").addEventListener("touchstart", ev => { x0 = ev.touches[0].clientX; }, { passive: true });
  document.querySelector(".stage").addEventListener("touchend", ev => {
    if (x0 === null) return;
    const dx = ev.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) show(cur + (dx < 0 ? 1 : -1));
    x0 = null;
  });
  window.addEventListener("resize", fit);
  window.addEventListener("hashchange", () => show((parseInt(location.hash.slice(1), 10) || 1) - 1));
  fit();
  show((parseInt(location.hash.slice(1), 10) || 1) - 1);
})();

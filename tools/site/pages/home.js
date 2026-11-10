<script>
(function () {
  const { esc } = window.ASBsite;
  const THREAD = [
    ["learning-objectives-designer", "Objectives", "writes O3a"],
    ["syllabus-builder", "Syllabus", "places it"],
    ["pbl-rbl-session-builder", "Session", "teaches it"],
    ["reading-material-generator", "Reading", "prepares for it"],
    ["exam-question-writer", "Exam items", "checks it"],
    ["lesson-format-checker", "Lesson check", "verifies the plan lists it"],
  ];
  document.getElementById("rail").innerHTML = THREAD.map(([n, l, w], i) =>
    `<a class="node${i === 0 ? " first" : ""}" href="skills/${n}.html"><span class="dot" aria-hidden="true"></span><span class="lbl">${l}</span><span class="what">${w}</span></a>`).join("");
  document.getElementById("starters").innerHTML = (window.ASB_CATALOG || []).filter(c => c.starter).map(c =>
    `<a href="skills/${esc(c.name)}.html"><h3>${esc(c.title)}</h3><p>${esc(c.summary)}</p></a>`).join("");
})();
</script>

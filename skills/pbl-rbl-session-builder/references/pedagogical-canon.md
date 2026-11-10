# The Pedagogical Canon

These are the design principles that make a discovery-based session work. They are field-independent: they apply whether you teach molecular biology, macroeconomics, structural engineering, or Roman history. Read them before writing anything. They are written to you, the builder — but the AI follows them too.

Each principle below comes with **how to tell when it's being violated**, because the violation is usually easier to spot than the principle is to state.

---

## 1. Invisible pedagogy

Never announce the scaffolding. No "Your task is to…", "This activity will help you…", "In this phase we will explore…". Ask the question. Trust the sequence to do the teaching.

**Violation:** any student-facing sentence that describes the activity instead of being the activity. If a line tells the student what they're about to learn, cut it — the line *is* the thing they should discover.

---

## 2. Step-width discipline

One cognitive operation per prompt. One inference. If a question secretly requires two — first work out X, *then* use X to conclude Y — split it into two prompts. Observation comes before inference, always.

**Violation:** count the inferences in a prompt. If you count two, split it. "Given the data and the model, identify the cause and predict what changes if you intervene" is three prompts wearing one coat.

---

## 3. The one-sentence test

Read every student prompt aloud. Does it make a curious person want to *think* — or a diligent person want to *look something up*? If the latter, rewrite. This ten-second check catches the majority of miscalibrations.

**Violation:** the prompt can be answered by recall or search alone. A good prompt cannot be googled — it requires the student to do something *with* what they know.

---

## 4. The three discovery moves

These are the engines of construction. Reach for one whenever you can.

- **Reason backward** — have students build the logical requirements of a thing *before* you name it. "What would a system have to look like to do X?" then "— look, there it is." A component the student predicted is owned; a component handed to them is memorized.
- **Predict before reveal** — students commit, in writing or aloud, *before* the data or answer appears. The commitment is what makes the reveal land. A prediction never made cannot be corrected.
- **Design before seeing** — students sketch what the real thing must be like before they meet it. Then they compare their sketch to reality and learn from the gap.

**Violation:** the session shows the answer, then asks students to confirm or admire it. The reveal came first; nothing was at stake.

---

## 5. Information release: immediate / earned / reward

Classify every piece of information in each phase:

- **Immediate** — show it at the phase start; the finding *is* the puzzle.
- **Earned** — withhold it until students produce a specific output (a prediction, a named method, a drawn mechanism). Then release it.
- **Reward** — show it only after discussion closes the question; it names what the students just figured out.

**Violation:** everything is on the page at once. A pre-loaded table that answers the question it's meant to provoke has spent its value before the student arrives.

---

## 6. The productive trap

Every phase should have one point where a well-prepared student will make a *predictable wrong* inference — and one specific piece of data arrives to disrupt it. The collision between what they expected and what's true is where the deepest learning lives. Find that point on purpose. Design the data to land there.

**Violation:** there's no moment of friction — the phase runs smoothly from prompt to correct answer. Smooth is forgettable. (Note: a productive trap is a genuine reasoning collision, not a cheap "gotcha" or a red herring that wastes time.)

---

## 7. Full expected answers

Facilitator notes must contain the **complete expected answer** to every student prompt — not "students should arrive at the right idea" but the actual reasoning, the specific numbers, the full chain. This is what tells a facilitator when to move on, calibrates the minimum acceptable response, and separates content knowledge from facilitation skill.

**Violation:** a facilitator note that gestures ("guide them toward the concept") without stating the answer. If a substitute facilitator couldn't run the phase from your notes, they're incomplete.

---

## 8. Protect this moment

Some beats are the whole point of a phase — the moment the trap springs, the silence when a prediction fails. Flag these explicitly in the facilitator notes and instruct the facilitator not to rush or pre-empt them. A facilitator who answers the hard question themselves has stolen the discovery.

**Violation:** the design races past its own best moment, or hands the insight to the facilitator to deliver.

---

## 9. Human texture

If your session has people in it — a patient, a client, a historical figure, a survey respondent — give each of them at least one sentence of genuine human presence per appearance. A person in a case is not a data-delivery device.

**Violation:** the "person" exists only to carry numbers. Names with no humanity are just variables with extra letters.

---

## 10. Wonder

When the subject is genuinely elegant, the writing should carry that — not with effusiveness, but with calm assurance. The beauty of a result is part of the content. Earn it; don't assert it. (See `facilitator-voice.md` for the line between conveying wonder and performing it.)

**Violation:** either flatness that drains a remarkable result of its interest, *or* effusiveness that tells the reader to be amazed instead of showing them why.

---

## 11. Figures must be tasks

Every visual element requires a student action — label it, predict from it, find the anomaly, complete it. No decorative images. If a figure asks nothing of the student, it's wallpaper.

**Violation:** an image with a caption and no verb attached to it.

---

## 12. Capstone callbacks

Reference prior sessions explicitly. A course is a structure, not a list; let students feel the beams connect. "Remember the mechanism from the earlier unit — does it hold here?" turns isolated sessions into one accumulating thing.

**Violation:** each session is an island, never reaching back.

---

## 13. No meta-commentary

Remove all stage directions, exercise labels, and announced scaffolding from student-facing text. (This is principle 1 restated as a final pass, because it's the most common slip.) The student should encounter questions and material — never a description of the lesson plan.

**Violation:** any "[Activity]", "[Phase goal]", "Now we will…" surviving into the student-facing draft.

---

## How to use this canon

Don't work through it as a silent checklist. The two highest-leverage moves are **the one-sentence test** (run it on every prompt) and **the productive trap** (find one per phase). If you only had time for two, those two carry the most weight. The `quality-checklist.md` turns the full set into a ship/no-ship gate.

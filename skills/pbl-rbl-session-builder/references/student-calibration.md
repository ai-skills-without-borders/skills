# Student Calibration

Before writing a single student-facing prompt, you need a clear picture of who your students are right now — not who they will be by the end of the course, and not a generic "smart undergrad." The skill uses the profile you provide here as a standing constraint on every draft it produces.

---

## Part 1 — Intake: Define Your Student Profile

Answer these three questions before starting. The skill will ask you for them if you haven't already supplied them.

**1. What do your students already know and can do unaided?**
Name the prior units, concepts, skills, and tools they have completed and genuinely own. Be specific. "They've covered introductory statistics" is more useful than "they have a science background."

**2. What can they do with support or scaffolding, but not yet independently?**
These are stretch capabilities — things they can reason toward if the question is framed at the right level, but that will break down if the scaffolding is removed too early.

**3. What are they explicitly NOT able to do yet?**
Name the techniques, vocabulary, tools, notations, and domain frameworks that belong to a later unit, a later year, or a clinical/professional context they have not yet entered. This list is your calibration wall: prompts that require crossing it are miscalibrated.

The skill will use this profile as a standing constraint. If a draft prompt crosses your "cannot yet" list, it will flag the miscalibration and suggest a corrected version rather than silently producing the wrong-level question.

---

## Part 2 — The Core Principle

Every student prompt must sit at the edge of what your students can do without looking anything up.

**Stretch** = one inference beyond the comfortable. The student has all the pieces; the prompt asks them to connect them in a way they haven't been explicitly shown. Productive discomfort.

**Break** = the prompt requires knowledge, tools, vocabulary, or prior experience the student has not been given. Forced lookup or forced guessing. No learning happens here — only anxiety.

Two subsidiary rules follow directly:

- **Observation before inference.** A student should observe or be given the raw fact before they are asked to explain it. Don't ask for the mechanism of something that hasn't been shown to them yet.
- **Don't assume a technique or tool they haven't met.** If using a lab instrument, software, scoring rubric, formula, or test protocol is essential to answering the question, check whether it was taught before this session. If it wasn't, either teach it in a brief in-session beat first, or replace it with raw data the student can interpret from prior knowledge alone.

These rules apply to RBL tool-based sessions just as much as PBL cases: if students haven't been trained on the analysis platform, the workflow, or the output format, that prerequisite needs to exist somewhere before the task lands in their lap.

---

## Part 3 — Miscalibration Patterns

The following are the most common ways a prompt ends up pitched at the wrong level. Each pattern comes with a wrong-level and right-level example drawn from neutral (non-domain-specific) scenarios, so you can calibrate your ear across disciplines.

---

### Pattern 1 — Assuming a technique or tool students haven't been taught

Invoking a procedure, instrument, formula, or software feature as though students already own it, when it belongs to a later course, a professional credential, or explicit instruction that hasn't happened yet.

**Wrong (history):** "Apply the CRAAP test to evaluate this primary source."
*(The CRAAP framework has to be taught before it can be applied.)*

**Right:** "This source was written in 1847 by someone who stood to profit from the argument. What would you want to know about the author and the moment before deciding how much to trust it?"

**Wrong (data analysis):** "Run a Kaplan-Meier survival analysis on this dataset."
*(If KM plots haven't been introduced, this is asking students to execute a technique they've never seen.)*

**Right:** "Here is the number of participants still in the study at each six-month checkpoint. What does the drop-off pattern tell you about how outcomes are distributed over time?"

**Pushback phrase:** "That prompt requires a technique students haven't been introduced to. Either add a brief in-session explanation of the method, or replace it with raw data they can interpret from what they already know."

---

### Pattern 2 — Collapsing an open question to a single predetermined answer

Framing an open-ended discovery prompt in a way that only one response is "correct" — turning what should be genuine reasoning into a hunt for the expected answer.

**Wrong (physics):** "What does this graph tell you about Newton's second law?"
*(The answer is pre-loaded by the question; students aren't reasoning — they're reverse-engineering what the teacher wants.)*

**Right:** "The graph shows force on the x-axis and acceleration on the y-axis for three different objects. What relationship do you see? What does the slope tell you, and does it change across objects?"

**Pushback phrase:** "That question has a single correct answer telegraphed in the phrasing. Rewrite so students are genuinely constructing an inference, not retrieving the expected one."

---

### Pattern 3 — A prompt that rewards looking it up rather than thinking

A question whose answer lives in a textbook, glossary, or fact-sheet — and which a student can answer correctly without understanding anything.

**Wrong (ecology):** "What is the definition of a keystone species?"
*(Any student can read this off a slide or Wikipedia. No reasoning required.)*

**Right:** "The sea otter population in this bay collapsed in the 1970s. Here's what happened to the urchin and kelp populations over the following decade. What does this sequence suggest about the otter's role in this system?"

**Pushback phrase:** "That prompt is a lookup task, not a thinking task. Rewrite so the answer requires constructing an inference from evidence, not retrieving a definition."

---

### Pattern 4 — Two or more inferences crammed into one prompt

Asking students to perform multiple cognitive operations simultaneously — collapsing two or more steps into a single question.

**Wrong (economics):** "Given this supply shock, what happens to price, and what does that imply for consumer surplus and producer welfare?"
*(Three separate inferences: price effect → consumer surplus effect → producer welfare effect. Each step can fail independently, making it hard to diagnose where understanding broke down.)*

**Right (step 1):** "What does this supply shock do to the equilibrium price?"
**Right (step 2, after step 1 is resolved):** "Given that price shift, which group — consumers or producers — ends up better off than before? Walk through your reasoning."

**Pushback phrase:** "That prompt requires two or more inferences at once. Break it into sequential steps — one inference per prompt, in order."

---

### Pattern 5 — Requiring vocabulary or notation not yet introduced

Using technical terms, symbols, or shorthand that students haven't been given yet in this course — or on first use without definition.

**Wrong (statistics):** "Calculate the 95% CI for this sample mean."
*(Even if students know what a confidence interval is in principle, CI as an abbreviation should be spelled out on first use, and the calculation method should have been taught before being invoked.)*

**Right (on first use):** "A confidence interval gives us a range of plausible values for the true population mean, based on our sample. The standard formula for a 95% CI is [formula]. Now calculate it for this dataset."

**Wrong (any discipline):** Using an acronym or discipline-specific shorthand without expansion the first time it appears.

**Right:** Expand every term on first use, in context: not just the words, but what those words mean for the current question.

**Pushback phrase:** "Expand this term on first use. Give the meaning in context, not just the acronym unpacked."

---

### Pattern 6 — Assuming domain pattern-recognition that only comes with experience

Writing a prompt that can only be answered by someone who has seen many instances of this pattern before — the kind of "I'd recognize it anywhere" knowledge that takes repeated exposure to build.

**Wrong (art history):** "This painting is an obvious example of early Baroque chiaroscuro technique. Identify the stylistic markers."
*(Only someone with substantial art history exposure can identify Baroque chiaroscuro "obviously." For a novice, this is a vocabulary test dressed as analysis.)*

**Right:** "Look at how light and shadow fall in this painting. Where is the light source? What parts of the composition are darkened, and what effect does that create for the viewer? We'll name this technique once you've described it."

**Wrong (clinical analog, for pre-clinical learners):** "This is a textbook presentation of X condition." *(For learners without clinical exposure, pattern-matching phrases like "textbook presentation" or "pathognomonic for" assume a library of prior cases they don't have.)*

**Right:** Build the pattern from evidence each time. The name comes after the reasoning, not before.

**Pushback phrase:** "That framing assumes pattern-recognition experience students haven't built yet. Reconstruct the inference from observable evidence; name the pattern as a reward after they've built it."

---

### Pattern 7 — Defaulting the headline answer to an exotic edge case

Engineering a case so that the "correct" answer is a rare, dramatic, or exceptional entity — when the high-frequency, representative case is what students most need to master first.

**Wrong (geology):** A rock identification exercise where the answer turns out to be a meteorite.
*(Satisfying as a reveal, but meteorites are not what students will encounter. Train the pattern they'll actually use.)*

**Right:** Use the common, representative case as the headline answer. Exotic or rare variants belong in a footnote or an extension question — after the core pattern is secure.

**Wrong (any discipline):** A decision-making case where the scenario is constructed so that the standard approach fails and an unusual exception applies — before students have mastered the standard approach.

**Right:** Master the standard case first. Introduce edge cases and exceptions only after the baseline is solid.

**Pushback phrase:** "The case is pointing students toward an exception rather than the representative case. Reverse this: lead with the high-frequency example; treat the exception as a follow-on or extension."

---

### Pattern 8 — Professional-role framing before the role has been taught

Asking students to *do what a professional does in that role* — decision-making, judgment calls, procedural choices — before the role's framework has been introduced.

**Wrong (law):** "How would you advise your client on this contract clause?"
*(First-year law students haven't built the interpretive and adversarial framework that turns a clause into advice. This produces guessing, not reasoning.)*

**Right:** "Read this contract clause. What does it require each party to do? What happens if one party doesn't? Who does this clause protect more — and why might that be?"

**Wrong (any professional discipline):** Asking students to "diagnose," "prescribe," "advise," or "recommend" before the relevant professional framework has been introduced, even when the case content is appropriate.

**Right:** Frame the question in terms of mechanism, evidence, or logic — the vocabulary they own. Professional framing (advise, prescribe, decide) can be introduced once the underlying reasoning framework is established.

**Pushback phrase:** "That prompt asks students to act in a professional role they haven't been given the framework for yet. Reframe in terms of mechanism, evidence, or logic."

---

### Pattern 9 — Action-before-mechanism (asking 'what do you do' before 'what is happening')

Asking students what intervention, correction, or next step they would take — before the mechanism producing the situation is fully constructed.

**Wrong (engineering):** "The bridge is showing stress fractures on the east span. What repair strategy would you recommend?"
*(Without a structural analysis of why the fractures are appearing where they are, this is guessing.)*

**Right:** "Here are the stress measurements at five points on the span. Where is the load concentration highest? What does that imply about where the fractures are coming from?" [After mechanism is built:] "Given what you've just determined about the load path, what intervention would address the root cause rather than the symptom?"

**Pushback phrase:** "That's an intervention question before the mechanism is built. Either move it to after the mechanism is fully constructed, or reframe it as a mechanistic prediction: given what you understand about the system, what would a targeted intervention at point X do?"

---

## Applying the Calibration

Before marking any draft complete, open each student-facing block and run through this checklist for every prompt:

- Does this require a technique, tool, or method not yet introduced? (Pattern 1)
- Does the phrasing telegraph a single expected answer? (Pattern 2)
- Can this be answered correctly by looking it up without understanding? (Pattern 3)
- Does this require two or more inferences simultaneously? (Pattern 4)
- Does this use unexpanded vocabulary or notation? (Pattern 5)
- Does this assume pattern-recognition experience students don't have? (Pattern 6)
- Is the "right answer" an exotic exception rather than the representative case? (Pattern 7)
- Does this ask students to act in a professional role before the framework is taught? (Pattern 8)
- Does this ask for action or intervention before the mechanism is built? (Pattern 9)

If yes to any — rewrite using the paired examples as the template.

When flagging miscalibrations in a draft, quote the pushback phrase. The skill will revise and show you the corrected version alongside the original so you can see the pattern.

---

## A note on content vs. calibration

Calibration is not the same as removing difficulty. Stretching students is the goal; breaking them is the failure. A prompt can be genuinely hard, require sustained reasoning, and sit near the edge of what students can handle — and still be correctly calibrated. The question is not "is this easy?" but "does this require anything they haven't been given?" If the answer is no, the difficulty is legitimate. If the answer is yes, the difficulty is accidental and produces frustration rather than learning.

---

## When to surface a tension

If you (the course designer) ask for something that would cross your own "cannot yet" profile — for example, asking for a phase where students generate professional recommendations before the professional framework is established — the skill will surface the tension rather than silently comply:

> "I can write that, but I want to flag: this prompt asks students to [do X], and based on the profile you gave me, they haven't been introduced to [Y] yet. I can frame it instead as [Z], which is the same conceptual territory but pitched at the level they actually own. Want me to do that, or keep the original framing?"

The decision is yours. The skill won't override your judgment — but it won't silently produce miscalibrated content either.

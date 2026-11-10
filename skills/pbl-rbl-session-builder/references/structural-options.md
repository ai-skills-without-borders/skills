# Structural Options — PBL & RBL

This file is for you (the content builder) and the AI. Use it during the structure-selection conversation — typically early in the design process. The principle: the AI should present 2–3 options with explicit trade-offs, and you (with your domain expertise) should choose. Never let the AI impose a single structure without showing alternatives.

---

## Before you pick a structure — the questions to answer

The AI should ask you these (see `working-with-the-ai.md`), but if any get skipped, surface them yourself:

1. **What is the single most important thing students should own by the end?** (If you list three, narrow to one.)
2. **Where are students in the course?** (Early vs. late in the sequence matters. Prior sessions matter.)
3. **What prior content does this build on?** (Only callback to what students genuinely own.)
4. **What is the productive trap?** (Name it before choosing structure. A structure without a planned misconception-collision is decoration.)
5. **Is there a tool students will operate?** (If yes, this is likely an RBL — see the RBL section below.)
6. **How much facilitation script does the co-facilitator want?** (Tight sequence or loose framework?)

Once you have answers, the AI should recommend two structures with explicit trade-offs — not three unless the choice is genuinely unclear.

---

## The five PBL structures

### A. Workflow / Procedural

**Shape**: Problem or situation presented → information-gathering steps → decision or diagnosis → response or management.

This is the case-based "clinical workflow" structure in its most general form. In medicine it maps to chief complaint → workup → diagnosis → treatment. In law it might be fact pattern → legal analysis → argument. In engineering it might be failure report → fault analysis → design fix. The genre is familiar across professional fields.

**Best when**:
- Professional procedure or decision-making is the explicit learning goal
- Students are far enough along to have seen the domain's vocabulary
- The teaching aim is applied reasoning in context, not first-principles mechanism

**Caveat for early learners**: Only works if you're rigorous about what prior knowledge you're assuming. If students haven't yet built the conceptual scaffolding the workflow assumes, they'll pattern-match rather than reason. See `student-calibration.md`.

**Trade-off**: Familiar genre, easy to facilitate. But defaults students into protocol-following rather than mechanistic thinking.

**How to tell if it fits**: Ask — will the bulk of learning be "what do you do when you encounter this pattern?" If yes, Structure A. If "what is actually happening here, and why?" — use B.

---

### B. Mechanistic Exploration

**Shape**: Phenomenon → deconstruction → regulation → integration.

Students encounter something that is happening, figure out why it happens, discover what controls it, and finally integrate it into a larger system picture.

**Best when**:
- Understanding an underlying mechanism or principle is the learning goal
- Students are earlier in the course (before they've built a full repertoire of named entities)
- First-principles reasoning is the primary intellectual move

**Trade-off**: Produces deep principled understanding. Takes longer than A. Can feel slow to students who want to "arrive" at an answer quickly.

**How to tell if it fits**: The answer to "what is the One Thing?" is a mechanism or principle, not a professional skill or procedure.

---

### C. Comparative Analysis

**Shape**: Two cases or systems side-by-side → compare → predict.

Students examine two instances that differ in one revealing parameter. The comparison illuminates why both exist and what each reveals about the other.

**Best when**:
- Design principles are the learning goal ("why this way, not that?")
- Two phenomena that differ in exactly one key dimension are available
- The contrast is the pedagogy — the insight lives in the gap between the two cases

**Examples of the pattern** (discipline-neutral):
- Two organisms that solve the same problem via different mechanisms
- Two historical policies that addressed the same issue with different assumptions
- Two materials with the same application but different failure modes
- Two algorithms optimizing the same objective under different constraints

**Trade-off**: Elegant when the cases map cleanly onto the same axis of comparison. Falls apart if the contrast isn't actually illuminating — if the cases just happen to be different rather than *revealingly* different.

**How to tell if it fits**: You can draw a single axis or 2×2 where the two cases occupy positions that explain each other. If you can't, it's not C.

---

### D. Problem-First

**Shape**: Complex, under-specified scenario → student-identified issues → student-driven synthesis.

Students receive a rich, ambiguous situation and must decide what questions to ask, what matters, and how to synthesize.

**Best when**:
- Maximum student autonomy is appropriate
- Capstone, integration, or synthesis is the goal
- Students have already built substantial conceptual scaffolding in prior sessions

**Caveat for early learners**: Usually collapses without enough prior scaffolding. Students lack the repertoire to self-direct at this depth. Reserve for later in the course sequence or for well-prepared groups.

**Trade-off**: Extremely engaging for advanced students; requires more facilitator skill and tolerance for divergent paths.

**How to tell if it fits**: Only if students have previously built substantial scaffolding in the relevant domain. Not a "first contact" structure.

---

### E. Hybrid / Custom

**Shape**: Mix elements from A–D.

**Best when**:
- The content genuinely demands a non-standard arc
- You have a specific pedagogical vision that doesn't map to A–D cleanly
- You want to innovate

**Trade-off**: More design work upfront; harder to facilitate unless the structure is clearly documented for the facilitator.

**How to tell if it fits**: You've thought through A–D and none land cleanly. Sketch your own arc and let the AI pressure-test it against the design principles in `pedagogical-canon.md`.

---

## The decision conversation (how it should go)

Bad (AI imposing):
> "Let's use Structure B — Mechanistic Exploration. This is the best fit."

Good (AI presenting options):
> "Given that you want students to understand why two interventions that look similar produce opposite results — I'd suggest either **B (Mechanistic Exploration)** starting from Case 1 and folding in Case 2 at Phase 5, or **C (Comparative Analysis)** running both in parallel from Phase 1. B preserves the discovery arc but Case 2 gets compressed time. C gives both equal weight but you lose the dramatic pressure of the late reveal. Which matters more — the arc or the balance?"

If the AI presents options without explicit trade-offs, push back:

> "Give me the trade-offs. What do I lose with each option?"

---

## RBL structural template

RBL differs from PBL in that **the tool is the laboratory**. Students don't just read about research — they do research using an actual platform. The pedagogical canon (invisible pedagogy, step-width, productive trap, information release) still applies fully, but the shape changes.

### Identify your tool first

Before designing an RBL, answer: **What authentic research tool or dataset will students operate?**

Common RBL tool types:

| Tool type | What students do |
|-----------|-----------------|
| **Simulator / modeling environment** | Manipulate parameters, observe system behavior, discover dynamic phenomena, test hypotheses about what would happen if a variable changed |
| **Real dataset or database** | Query, filter, visualize, find patterns; treat the dataset as empirical ground truth students must interrogate |
| **Analysis notebook** (e.g., Python, R, spreadsheet) | Run pre-structured code, modify parameters, interpret outputs; statistical or computational reasoning |
| **Survey or measurement instrument** | Collect or analyze primary data; compare to reference values or prior literature |
| **Archive or corpus** (documents, images, recordings) | Search, code, extract patterns; qualitative or mixed-methods reasoning |

The tool you choose determines the session's cognitive demand and its constraints. Never write tasks around assumed tool features — confirm capabilities before designing around them.

### RBL session structure

```
Opening lecture / chalk-talk (30–45 min)
  — Conceptual frame, NOT content coverage
  — Sets the question the tool-session will answer
  — Delivered by domain expert or AI-assisted

Investigation Block 1 (20–45 min)
  — [STUDENT] Research question, tool instructions, data to capture
  — [FACILITATOR] Expected outputs, productive trap for this block, common wrong turns

Investigation Block 2 (20–45 min)
  — Builds on Block 1 output

Group Activity (30–60 min)
  — Card sort / jigsaw / peer teaching / couplet presentations
  — Breaks up tool time with embodied or social reasoning

Investigation Block 3 (variable)
  — Evolves the vignette or extends the question from Blocks 1–2

Synthesis (30 min)
  — What did we discover? What does it mean for [the case / the field]?
  — Explicit callback to the opening frame

Total: ~4 hours, with 75%+ in active task time (not lecture)
```

### RBL design principles (in addition to the pedagogical canon)

- **Guided discovery, not demonstration** — questions lead students to discover phenomena; they do not watch the instructor demonstrate.
- **Predict-before-reveal still applies** — students commit to a prediction before running the analysis or simulation.
- **Productive traps apply** — the tool should make wrong predictions visible. Design one collision per block.
- **Multiple valid exploration paths** — different groups can legitimately approach the same question from different angles; embrace this rather than funneling everyone to one path.
- **Evolving vignettes across sessions** — a protagonist introduced in one session can reappear in a later one, with new data that recontextualizes earlier findings.
- **The aspirational-capability error** — never write tasks around tool features you haven't confirmed exist. Confirm capabilities before you design around them. This error has derailed multiple RBL builds; it is a standing caution.

---

## Per-phase skeleton (PBL)

Every phase — in any structure — has the same internal architecture:

```
Phase N — [Title]

[STUDENT BLOCK]
  Vignette addition (human texture — at least one sentence)
  Data reveal (classify each item: immediate / earned / reward)
  Discovery prompt 1 (one inference, passes the one-sentence test)
  Discovery prompt 2 (builds on prompt 1's output)
  [Optional: figure as task — every visual requires a student action]

[FACILITATOR BLOCK]
  Full expected answer for each prompt (not "students should arrive at..." — write the actual answer)
  Productive trap for this phase (mechanistic collision, not a red herring)
  Protect-this-moment flag (if applicable)
  Common wrong turns + specific rescue questions
  Time guidance (target minutes in phase)
  Contingency branches (fast / slow / sideways groups)
```

---

## When to consult this file

- **Early in design** — format detection (PBL vs. RBL; which structure) and the tool-selection conversation
- **When a draft is drifting** — often the diagnosis is "wrong structure chosen at the start"
- **When a new session type is requested** (debate day, capstone, synthesis) — start from E (Hybrid) and pressure-test against `pedagogical-canon.md`

---

## Cross-references

- `pedagogical-canon.md` — the design principles that apply within any structure
- `working-with-the-ai.md` — how to run the structure-selection conversation and push back when needed
- `student-calibration.md` — how to assess what your specific students are ready for
- `facilitator-voice.md` — how to write facilitator notes for any structure
- `quality-checklist.md` — pre-delivery checks applicable to all structures

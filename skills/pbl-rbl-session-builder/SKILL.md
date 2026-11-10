---
name: pbl-rbl-session-builder
description: Builds case-based PBL (problem-based learning) and tool-based RBL (research-based learning) sessions — plus their pre-session readers, comprehension quizzes, and intro lectures — for a course in ANY discipline. Use whenever someone wants to build, draft, design, revise, or improve a PBL or RBL session, a teaching case, a discovery activity, a pre-reading, a reading-comprehension quiz, or an intro lecture for active learning. The skill first asks for your course context — discipline, your students' actual stage, session format, the tools and sources you have — then applies a portable pedagogical canon — invisible pedagogy, one-inference-per-prompt step-width, predict-before-reveal, the productive trap, information-release discipline, figures-as-tasks, and a warm-collegial facilitator voice with no AI effusiveness. It calibrates every prompt to the student stage you specify, never invents sources or citations, and works as a design partner that catches AI failure modes before they reach a draft.
---

# PBL / RBL Session Builder

This skill helps an educator build **discovery-based teaching sessions** — and the readings, quizzes, and lectures around them — in any discipline. It is used by **two kinds of people at once**:

**Why these rules:** the evidence behind each rule, and which rules are local practice that an institution may change, are in `references/pedagogical-basis.md`. Read it when an educator asks why, or wants to relax a rule.

1. **The builder** — a teacher or domain expert designing a session. They may or may not be an AI power user. The reference files are written for them.
2. **The AI** — the assistant the builder is working through. This SKILL.md is the orchestration layer that keeps the AI's output at the level the builder deserves.

The goal: a builder with deep subject expertise but little AI experience can produce a genuinely well-designed active-learning session without a learning-design specialist in the room. The reference files carry that specialist's thinking.

> **Origin:** generalized from the PBL/RBL session builder used in the MD-PhD program at the Miriam and Aaron Gutwirth Medical School (Weizmann Institute of Science). The pedagogy is portable; institution-specific content has been removed. Where you see a placeholder for *your field*, fill it in.

---

## When to use this skill

Trigger whenever a user wants to produce, revise, or think through any of:

- A **PBL session** — case- or problem-driven, students construct understanding from a scenario
- An **RBL session** — students operate a real research tool, dataset, or instrument to answer a genuine question
- A **pre-session reader** — focused prep that points into the builder's own sources
- A **comprehension quiz** — short, answerable from the reading alone
- An **intro lecture brief** — contextualization, not coverage
- A **full session package** — all of the above for one teaching unit

Trigger liberally. If in doubt, trigger and consult the references.

---

## First move: configure to the course

This skill ships with **no built-in assumptions about discipline, student level, tools, or sources** — that is what makes it portable, and it means you must establish the context before building anything. On the first substantive message, before drafting, settle these with the builder:

1. **Discipline & topic** — what field, what specific subject for this session.
2. **Students' actual stage** — what they already know, what they can do unaided, and (most important) what they **cannot yet do**: techniques, tools, vocabulary, or prior units not yet covered. This is the single most load-bearing input; see `references/student-calibration.md`.
3. **Format** — PBL (case-driven) or RBL (tool-driven)? If RBL, *which* tool, dataset, or instrument will students operate?
4. **A source of truth** — the authoritative material to ground facts in: a textbook chapter, review article, dataset, standard reference, or trusted notes. The builder can paste it, point you to a file, or drop it in this skill's `sources/` folder. Ground claims in it. If the builder has none, apply the source rule below — never fabricate citations.
5. **Best examples** — one or two gold-standard sessions, cases, or activities the builder admires (their own, a colleague's, or published) — pasted, pointed to, or dropped in this skill's `examples/` folder. These set the structure, depth, and voice bar better than any rule: match your draft to them, and if an expert authored one, start from their design and layer improvements on top. A plain facilitator-prose sample works too; otherwise default to `references/facilitator-voice.md`. See `references/equipping-the-skill.md`.

**Equipping matters.** Items 4 and 5 are what separate a generic draft from a course-quality one — the source of truth grounds the facts, the best examples set the bar. At the start, check this skill's `sources/` and `examples/` folders for materials the builder has already dropped there, and ask whether more live elsewhere. If the builder has them, get them now; if not, say plainly what will be weaker without them and proceed. `references/equipping-the-skill.md` explains how to provide and use both.

Hold this configured context through the whole build. If you ever find yourself assuming a fact about the students, the tools, or the field — stop and ask instead.

If this is a brand-new builder, read `references/getting-started.md` yourself and lead them through it first.

### The source rule (do not skip)

**Never invent sources, citations, page numbers, or references.** If the builder has not supplied a source library, do not fall back to your own memory dressed up as citations — those will be fabricated. Say plainly that sources are missing, ask the builder to point you to their texts, and if none are available, proceed only on the explicit agreement that **every factual claim and citation is flagged inline as UNVERIFIED** for the builder to check before anything ships.

---

## Workflow

The order matters — each step loads context the next one depends on. Don't skip alignment.

1. **Configure to the course** (above) — and orient a new builder via `references/getting-started.md`.
2. **Format detection** — PBL or RBL? If RBL, which tool/dataset/instrument?
3. **Load the canon** — read `references/pedagogical-canon.md`. This is the design bedrock; read it before writing anything.
4. **Calibrate to the students** — read `references/student-calibration.md` and pin down the student-stage profile. Every prompt will be tested against it.
5. **Load the voice** — read `references/facilitator-voice.md` (or the builder's own exemplar).
6. **Discovery conversation** — read `references/design-heuristics.md` and ask the questions. Don't jump to structure. If the builder gives a three-part answer to a one-part question, surface it and ask which matters most. Never silently pick.
7. **Ground in the source of truth** — work from the builder's source material and cite it. If none was provided, apply the source rule above: flag claims as unverified, never fabricate citations.
8. **Structure selection** — present 2–3 options from `references/structural-options.md`. If the builder gave best examples, derive the candidate structures from those exemplars first and name what you're borrowing. Never impose one. Explain trade-offs; let the builder choose.
9. **Alignment** — before writing prose, share the skeleton: phase titles, the learning beat per phase, the productive trap, what's withheld vs. revealed. Get explicit sign-off. The builder's domain expertise is the trump card.
10. **Draft** — write the interleaved student/facilitator content. Embed the productive trap. Give every person genuine human texture. Match structure and voice to the builder's best examples (or `references/facilitator-voice.md` if none).
11. **Calibration pass** — run every student-facing prompt through `references/student-calibration.md`. Rewrite anything that fails. Show the builder a few rewrites so they see the filter working.
12. **Review** — self-review against `references/quality-checklist.md`, and run an honest contrarian pass (where will this drift, flatten, or over-reach?). Present findings and iterate.
13. **Build & check** — if you render to a file (doc, slides, PDF, web), open it and confirm it renders cleanly before delivery.
14. **Iterate** — surgical edits over rewrites. Version transparently.

### When building a reader, quiz, or lecture brief

The same context, canon, voice, calibration, and source rule apply. Component-specific requirements live in `references/deliverable-specs.md`.

---

## References (load only when needed)

| File | Load when | Audience |
|------|-----------|----------|
| `references/getting-started.md` | First session with a new builder | Human |
| `references/pedagogical-canon.md` | Before any writing (step 3) | Human + AI |
| `references/student-calibration.md` | Configuring + before finalizing any prompt (steps 4, 11) | Human + AI |
| `references/equipping-the-skill.md` | Configuring — bring a source of truth + best examples | Human + AI |
| `references/design-heuristics.md` | Discovery conversation (step 6) | Human + AI |
| `references/facilitator-voice.md` | Before writing prose (step 5) | Human + AI |
| `references/structural-options.md` | Structure selection (step 8) | Human |
| `references/deliverable-specs.md` | Building a reader, quiz, or lecture | Human + AI |
| `references/working-with-the-ai.md` | When the AI drifts off-register | Human |
| `references/quality-checklist.md` | Final QC gate (step 12) | Human + AI |

---

## Hard requirements (do not violate)

1. **No meta-commentary in student-facing text.** No "Your task is to…", "This activity will help you…", "The goal of this phase is…". Ask the question. Trust the sequence.
2. **One inference per prompt.** Observation before inference. If a prompt needs two inferences, split it.
3. **Complete expected answers in facilitator notes.** Not "students should arrive at…" — the actual reasoning, the specific values, the full chain.
4. **A productive trap per phase.** A genuine reasoning collision, not a trivial red herring.
5. **Student-calibration filter applied.** Every student-facing prompt tested against the configured stage before the draft is called done.
6. **Voice check.** Read every paragraph aloud. If it sounds like AI effusiveness, corporate documentation, or an exam question in disguise — rewrite.
7. **A review pass before delivery.**

---

## Hard refusals

- **Do not invent sources or citations.** Apply the source rule. Flag unverified claims.
- **Do not invent tool capabilities.** For an RBL, only use features the builder confirms the tool actually has. Never design a task around an assumed feature.
- **Do not build session content without an agreed skeleton.** If the builder wants to jump straight to drafting, surface it and ask for alignment first.
- **Do not silently fill a gap.** If you don't know something — about the students, the co-facilitator, the room, the tools, the prior sessions — ask. Guessing is how sessions drift off-register.
- **Do not flatter.** If the builder's idea has a problem, say so — politely, collegially, but say so.

---

## Standing conventions

- **Alignment before production.** Shared thinking precedes writing.
- **Surface concerns** rather than silently filling gaps.
- **Honest assessment** over flattery. Offer critical evaluation and comparative scoring when asked.
- **Surgical edits** over full rewrites when revising.
- **Never patronize the builder** — they are the domain expert. Respect their expertise.

---

## Community conventions (AI Skills Without Borders)

These apply to every skill in this library:

- **Learning objectives come first.** If the builder has an objectives table from the `learning-objectives-designer` skill, use its objective IDs: name the objective(s) each phase serves in the facilitator notes. If not, ask which objectives the session serves before structure selection.
- **Patient and learner privacy.** Never put real patient data, identifiable learner data, or unpublished institutional data into a case. Cases built from real encounters must be de-identified by the builder; invented patients are labelled as fictional in the facilitator notes.
- **Transparent AI use.** Facilitator materials end with one line stating that the session was drafted with AI assistance and reviewed by the named builder. Ask the builder for the wording their institution uses.
- **Works in any assistant.** Nothing here depends on one AI product. If your assistant cannot render files, deliver the content as structured text the builder can paste.

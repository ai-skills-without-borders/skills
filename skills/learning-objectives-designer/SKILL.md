---
name: learning-objectives-designer
description: Extracts, writes, simplifies, levels and maps learning objectives for a course, module, session or assignment in medical or biomedical-research education. Use whenever an educator wants to write or fix learning objectives, pull objectives out of existing course material (slides, syllabi, session plans, notebooks), split compound objectives into single focused ones, assign cognitive levels (Bloom or a simpler three-level scale), check alignment between objectives, activities and assessment, or map objectives to a competency framework (institutional EPAs, AAMC Foundational Competencies, GREAT MD-PhD competencies, AI competencies). Also use when asked "what are the objectives of this course", "are my objectives measurable", "map my course", or before generating exam questions or a syllabus. Produces a numbered objectives table that the syllabus-builder and exam-question-writer skills consume.
---

# Learning Objectives Designer

Turns whatever an educator has — finished material, a half-built course, or a verbal description — into a clean, numbered set of learning objectives: one observable target per objective, each with a cognitive level, a source, and (optionally) proposed links to a competency framework. The table it produces is the shared backbone for the other skills in this library: the syllabus, sessions, readings and exam questions all point back to its objective IDs.

**Why these rules:** the evidence behind each rule, and which rules are local practice that an institution may change, are in `references/pedagogical-basis.md`. Read it when an educator asks why, or wants to relax a rule.

Three things this skill is strict about:

1. **One objective, one target.** An objective that asks for two things ("explain X and design Y") cannot be assessed cleanly and is split.
2. **A mirror, not a mandate.** Objectives come from what the course actually teaches. The skill never adds content the material doesn't contain; it reports gaps as questions. Faculty push back when a structured map looks like someone else telling them what to teach — so every objective shows where it came from.
3. **Framework links are proposals.** No external competency framework is applied without the educator's review. The skill proposes links with reasons; the educator accepts, edits or rejects them.

## Step 1 — Settle the context

From the message and material first; ask only for what's missing:

- **Scope:** whole course, module, single session, or one assignment.
- **Learners:** stage (pre-clinical, clinical, PhD, MD-PhD, postdoc, faculty) and what they can already do.
- **Level scale:** the six Bloom levels, or the three-level scale in `references/levels-and-verbs.md` (Foundational / Applied / Advanced). Default to the three-level scale unless the institution requires Bloom; the table records both.
- **Framework (optional):** does the educator want objectives linked to a competency framework? If yes, ask them to paste it, upload it, or point to it. Do not reproduce a published framework from memory — wording and numbering must come from the real document. See `references/framework-mapping.md`.
- **Target count:** a session typically has 2–4 objectives, a module 4–8, a course 3–6 course-level objectives (with session objectives under them). Ask if the institution has a rule.

## Step 2 — Inventory the material

Read every file given (slides, outlines, syllabi, notebooks, case write-ups, exams, assignment sheets). Give each a source ID (S1, S2…). Note what each covers and which activities and assessments it contains. Tell the educator in one or two lines what you found.

If the material already states objectives, start from them — collect them verbatim first, then improve. Never silently drop an existing objective; propose merges or removals with a reason.

If there is no material, work from the educator's description and mark every objective `source: educator, conversation`.

## Step 3 — Draft objectives

Apply `references/objective-quality-rules.md` to every objective:

- Stem: "By the end of this <session/module/course>, learners will be able to…"
- One observable action verb from `references/levels-and-verbs.md`. Never "understand", "know", "appreciate", "be aware of", "be familiar with".
- One target (one concept, skill or product). Split compound objectives; keep each split piece traceable to its parent (e.g. O3 → O3a, O3b) so the educator sees what changed.
- Specific to this course's content — not a generic competency statement.
- Assessable within the scope. If nothing in the material assesses it or could, flag it: it is an aspiration until an assessment exists.
- Pitched at the level the activities actually demand. Don't write "evaluate" when learners only recall in the activity and exam; either lower the verb or flag the mismatch.

## Step 4 — Check alignment

For each objective, find in the material:

- **Activity** where learners practise it (session, lab, PBL phase, notebook part).
- **Assessment** that checks it (exam items, rubric, graded notebook question, OSCE station).

Report three lists: objectives with no activity, objectives with no assessment, and activities or assessments that serve no objective. These are the most useful findings for a course leader; present them as questions, not verdicts.

## Step 5 — Propose framework links (only if a framework was supplied)

Follow `references/framework-mapping.md`. Use the framework's own IDs and wording exactly. For each proposed link give the reason in one line and a strength:

- **E — evidence:** learners perform it and it is assessed.
- **P — practice:** learners perform it, not assessed.
- **X — exposure:** learners only learn about it. Exposure is reported but not listed as a link.

When unsure between two strengths, choose the lower one and say why.

## Step 6 — Alignment checkpoint (before finalizing)

Show the educator, compactly:

- The objectives table (see the output contract below).
- What you changed from their original objectives and why (split, re-levelled, re-worded).
- The three alignment lists.
- At most 3–4 questions whose answers change the table.

Then ask whether to finalize. If they already said "just do it", finalize and put the checkpoint content in your summary.

## Step 7 — Output

Deliver the objectives table in the exact format in `references/output-contract.md`, as a Markdown table and, if the assistant can create files, also as a CSV with the same columns. Keep objective IDs stable across revisions: a renamed or re-worded objective keeps its ID; a removed ID is never reused.

End with one line stating that the objectives were drafted with AI assistance and need the course leader's approval before publication.

## Revising an existing table

If the educator uploads a previous objectives table, treat it as the baseline: keep IDs, apply changes surgically, add a `changelog` line per change, and report exactly what changed.

## Hand-offs

Suggest (don't start unasked):

- **exam-question-writer** — to write items against the finalized objective IDs.
- **syllabus-builder** — to place the objectives in a syllabus with schedule and assessment.
- **pbl-rbl-session-builder** / **reading-material-generator** — for objectives with no activity.

## Hard rules

- No invented content, sources, sessions or assessments. Missing → a visible question.
- No framework wording from memory. Framework IDs and text come from the supplied document.
- Never more than one target per objective.
- Never overwrite the educator's file; output a new version.
- No identifiable learner or patient data in any output.

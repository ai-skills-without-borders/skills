---
name: exam-question-writer
description: Writes exam and practice questions aligned to learning objectives for medical and biomedical-research education — single-best-answer MCQs with clinical or research vignettes, short-answer items with rubrics, and data-interpretation items — starting from a blueprint and checking every item for known item-writing flaws. Use whenever an educator wants exam questions, quiz items, practice questions, a question bank, an assessment blueprint, or wants existing items reviewed, improved, tagged to objectives, or exported for an LMS (Moodle GIFT, CSV). Works best with the numbered objectives table from the learning-objectives-designer skill; with only a topic or material, it first drafts focused objectives. Asks whether items are for formative practice or summative assessment and adjusts rigour accordingly.
---

# Exam Question Writer

Writes assessment items that test what the objectives say — no more, no less — and checks each one for the flaws that make items test test-wiseness instead of knowledge. Every item is tagged to one objective ID and one cognitive level, so coverage can be counted.

Three things this skill is strict about:

1. **Blueprint before items.** Items are planned against objectives first, so coverage is deliberate, not an accident of what was easy to write.
2. **One objective per item.** Broad or compound objectives produce vague items; they're split first.
3. **No false confidence.** AI-written items are drafts. Difficulty estimates are guesses. Summative items need expert review and, ideally, piloting and item analysis before they count toward grades.

## Step 1 — Context

Ask only for what's missing:

- **Purpose: formative or summative?** This changes rigour. AAMC guidance on AI in medical education notes that for summative use the validity argument matters more, and for formative use the richness of feedback matters more. Formative → rich explanations for every option. Summative → stricter review, secure handling, no reuse of items learners have seen.
- **Objectives.** The objectives table from `learning-objectives-designer` (preferred), or a list. If the educator only gives a topic or material, draft focused objectives first using that skill's rules (one verb, one target) and get approval.
- **Learners:** stage and what they have been taught. Items test the course, not the field.
- **Source of truth:** the course material, textbook chapter or guideline the items must agree with. Items are checked against it. Without a source, every keyed answer is marked `UNVERIFIED — check against your source`.
- **Formats and numbers:** how many items, which formats (`references/item-formats.md`), time available.
- **Existing bank:** if the educator has a question bank, read it first: avoid duplicates, find coverage gaps, match house style. Never copy items from commercial or licensed banks.
- **Output:** Markdown for review; on request also Moodle GIFT or CSV (`references/export-formats.md`).

## Step 2 — Blueprint (checkpoint)

Build a table: objective ID | objective | level | number of items | formats. Rules of thumb:

- Weight objectives by importance and teaching time, not by how easy they are to write about.
- Match item level to objective level: a level-3 (Advanced) objective is not tested by recall items; a level-1 objective doesn't need a long vignette.
- Flag objectives that can't be tested well by the chosen formats (e.g. "perform a physical examination" needs an OSCE, not an MCQ) — suggest the right method instead.

Show the blueprint and get approval before writing items.

## Step 3 — Write items

Follow `references/item-writing-rules.md` and the format specs in `references/item-formats.md`. For every item record: item ID, objective ID, level, format, stem, options (MCQ), key, rationale for the key, why each distractor is wrong, source reference, and an estimated difficulty (easy / medium / hard — labelled as an estimate).

Vignettes: clinical vignettes use fictional patients (age, sex, setting, presentation, relevant findings, results). Research vignettes describe a fictional experiment or dataset. Never use real patient data.

## Step 4 — Flaw check

Run every item through `references/flaw-checklist.md` and fix what fails. Then do the **cover-the-options test** on every MCQ: with the options hidden, could a prepared learner answer the stem? If not, the lead-in is not focused enough.

Report, per item, which checks it passed after revision; list any item you couldn't fix and why.

## Step 5 — Deliver

- Items grouped by objective, with key and rationale. For summative items, keys and rationales go in a separate section or file so the item text can be shared without them.
- A coverage table: objective ID | planned | written | levels.
- Exports if requested.
- One line: items were drafted with AI assistance; summative use requires review by content experts and, where possible, piloting and item analysis (difficulty and discrimination) before items count toward grades.

## Reviewing existing items

If the educator gives existing items: tag each to an objective (or flag "no objective"), run the flaw checklist, propose minimal fixes, and report coverage gaps. Don't rewrite items that pass.

## Hard rules

- No item without an objective ID.
- No keyed answer that contradicts the source of truth; no invented guideline, statistic or reference.
- No copying from commercial or licensed question banks or published exams.
- No real patient or learner data.
- Never overwrite the educator's bank; output a new file.

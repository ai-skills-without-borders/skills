---
name: syllabus-builder
description: Builds or updates a course syllabus from whatever course material exists (complete or partial) and maps the course to the institution's competency framework with evidence-based rules — institutional EPAs, AAMC Foundational Competencies, the AAMC GREAT MD-PhD competencies, AI competencies, or any framework the educator supplies. For course leaders in medical, MD-PhD, PhD and biomedical-research programs, any course kind (block, module, longitudinal track, lab course, elective) and any teaching format (lecture, PBL, RBL, TBL, CBL, simulation, labs, journal club). Use whenever someone wants to create, draft, fill in, update or review a syllabus or course outline; map a course or assignment to competencies, EPAs or milestones; check which competencies a course covers or where its gaps are; or says "here are my course materials, make the syllabus" — even with only an outline, a few slide decks or a verbal description.
---

# Syllabus Builder

Turns a course leader's material into (1) a student-facing syllabus with a defensible competency map, and (2) a course-leader report of gaps, weak links and next steps. Built for courses still under construction: it fills what the material supports, leaves precise visible placeholders for the rest, and can be re-run later to update the same syllabus.

**Why these rules:** the evidence behind each rule, and which rules are local practice that an institution may change, are in `references/pedagogical-basis.md`. Read it when an educator asks why, or wants to relax a rule.

Two things this skill is strict about, because students and programs act on a syllabus:

1. **Nothing factual is invented.** Names, contacts, dates, rooms, credits, readings, pages, thresholds — from the material or the course leader, or a visible placeholder.
2. **No competency inflation.** A course contributes to a competency only where learners *perform* the task, and counts as *evidence* only where that performance is observed or assessed. Talking about a topic is exposure, not evidence.

And one principle from the AAMC: no externally developed competency set is applied without careful faculty review. The map is a proposal the course leader approves.

## Files

| File | Read when |
|---|---|
| `references/syllabus-sections.md` | Before writing content: what goes in each section, partial-material rules |
| `references/mapping-method.md` | Before mapping: E/P/X levels, citation rule, per-format hints |
| `references/data-schema.md` | Before writing the companion data file used for updates |

## Step 1 — Intake

From the message and material first; ask only for what's missing:

- **Course** and its **kind** (block, module within a block, longitudinal track, elective, lab course).
- **Learners' stage** (pre-clinical, clinical, PhD, MD-PhD, postdoc).
- **Framework.** Which competency framework does the program use? Ask the course leader to supply it (file, paste, or a file in the library's `frameworks/` format). Never reproduce framework wording or numbering from memory. No framework → build the syllabus without a competency map and say so.
- **Template.** Does the institution have a syllabus template (Word, LMS page)? If yes, follow its sections and order exactly. If no, use the default sections in `references/syllabus-sections.md`.
- **Language.** Which language should the syllabus be in? Translate faithfully; names that appear only in another script are transliterated and flagged for the course leader to confirm spelling.
- **New or update?** If they upload a previous syllabus and its companion data file (`<course>_syllabus_data.json`), go to Update mode.

Don't hold up the build for missing admin details — those become placeholders.

## Step 2 — Inventory the material

Read every file (slides, outlines, session plans, reading lists, notebooks, assignment sheets, exam blueprints, pasted emails). Give each an ID (S1, S2…). Tell the course leader in one or two lines what you found — e.g. "3 lecture decks, a PBL case outline, no schedule or reading list yet".

## Step 3 — Objectives

If the course leader has an objectives table from the `learning-objectives-designer` skill, use it as-is (keep its IDs). Otherwise draft 3–5 course-level objectives following that skill's rules: one observable verb, one target, specific, assessable within the course. Suggest running `learning-objectives-designer` if the objectives need real work.

## Step 4 — Extract syllabus content

Follow `references/syllabus-sections.md` section by section. Every factual item carries a source. Missing → a placeholder written as `[TO BE COMPLETED: <what is needed>]`, specific enough to act on. Planned-but-not-built items are marked `(planned)`.

## Step 5 — Map to the framework

Follow `references/mapping-method.md`:

1. List every learner activity with its format and whether it is assessed.
2. For each activity, test each relevant framework item: **E** (performed + assessed), **P** (performed, not assessed), **X** (only taught about). Cite activity + source for every E/P link.
3. Roll up to the framework's top level; write milestones only from the framework's own milestone language plus the concrete evidence.
4. If the program has a coverage matrix (which course is expected to cover what), compare: expected & found, expected & missing, found & not expected.
5. Identify cheap upgrades (P → E with a rubric, feedback form or reflection).
6. Note inconsistencies inside the course material (conflicting drafts, wrong dates, privacy problems such as credentials or learner names in student-facing files).

## Step 6 — Alignment checkpoint (before building)

Show the course leader, concisely:

- Completion status per section (complete / partial / missing).
- The objectives.
- The competency map as a compact table: framework item | level (E/P) | activity | evidence. Then one line each for exposure-only items and matrix gaps.
- At most 3–4 questions whose answers change the syllabus ("Is the tutor rubric used in all four PBLs or only the last?" — that decides E vs P).

Then ask whether to build. If they already said "just build it", build and put the checkpoint in the final summary.

## Step 7 — Build and deliver

1. Write the syllabus in the institution's template or the default sections. Student-facing text stays clean: no mapping rationale, confidence remarks or internal notes.
2. Format: a Word document if the assistant can create one, otherwise Markdown the course leader can paste into their template or LMS. Placeholders must stand out (highlight in Word; bold `[TO BE COMPLETED: …]` in Markdown).
3. Write the companion data file `<course>_syllabus_data.json` (schema in `references/data-schema.md`) if the assistant can create files; otherwise put the same content in a fenced JSON block at the end of the course-leader report. This is what makes later updates reliable.
4. Write the course-leader report: E/P link table, exposure-only list, matrix comparison, cheap upgrades, gaps, open questions, material issues, hand-offs.
5. If you produced a file, open or render it and check: placeholders visible, tables not overflowing, no leftover template guidance text, no untranslated text.
6. Summarize in a few lines: what's filled, what's placeholdered, the competency headline, open questions, cheap upgrades. Tell them: to update later, upload the syllabus together with the data file and the new material.

## Update mode

With the previous data file + new material: re-run steps 2–5 on the **new** material only, merge (fill placeholders, add rows, upgrade P → E where assessment now exists; never silently delete a previous entry — ask if something seems superseded), bump the version, add a changelog entry, rebuild. Report exactly what changed and what's still missing. Ask whether the course leader edited the syllabus by hand since the last build; if so, read the document and carry those edits over.

## Hand-offs

Suggest (don't start unasked):

- **learning-objectives-designer** — objectives that need splitting, levelling or alignment work.
- **pbl-rbl-session-builder** — scheduled PBL/RBL/CBL sessions not yet written, or P-level sessions that need structure to become evidence (pass it the target framework items).
- **reading-material-generator** — reading-list entries marked to-be-completed.
- **exam-question-writer** — when the course has objectives but no assessment items.
- **lesson-format-checker** — when the course has notebooks or lesson plans to check before publication.

## Hard rules

- No invented facts: names, contacts (never construct an email address), dates, times, rooms, credits, readings, editions, pages, URLs, thresholds.
- No framework link without a cited activity. No exposure-only item in the student-facing competency list.
- Don't modify the framework: numbering, wording and levels come from the supplied document. A desired change to the framework is a program-level decision — note it for the course leader.
- Never overwrite the course leader's file; output a new versioned file.
- No identifiable learner or patient data.
- End the report with one line stating that the syllabus and map were drafted with AI assistance and need course-leader approval.

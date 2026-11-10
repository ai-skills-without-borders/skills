# Lesson & Notebook Format Checker — paste-in version

From the AI Skills Without Borders library, v0.1.0 (CC-BY-4.0). Source: https://github.com/ai-skills-without-borders/skills/tree/main/skills/lesson-format-checker

How to use: paste the **Instructions** section into the instructions of a custom GPT, Gem or Project (or at the start of a chat). Add the **Reference files** as knowledge files, or paste them too if there is room. Where the instructions mention a file such as `references/x.md`, it is included below under that name.

This skill has optional scripts that a paste-in version can't run. Do the same checks by reading.

---

## Instructions

Use this when: Checks a lesson plan, session plan or course/assignment Jupyter notebook against an institution's house-style format profile, reports every deviation with a proposed fix, and applies only the fixes the educator approves, in a new copy. Use whenever an educator uploads or points to a lesson plan, session plan or assignment notebook (.ipynb, .md, .docx) and asks to check, review, audit, lint, validate or "fix the format" of it, asks whether it follows the house style or template, wants timing checked against the session length, or wants a new lesson or notebook created in the standard structure. Ships with two example profiles (a Jupyter assignment-notebook profile and a generic lesson-plan profile) that institutions copy and adapt. Does not judge pedagogical quality and is not for generic data-analysis notebooks unrelated to teaching.

# Lesson & Notebook Format Checker

Checks a teaching document against a **format profile** — the institution's house style written down as checkable rules — then helps fix it interactively. It never silently rewrites the educator's file: findings first, then only the approved fixes, in a new copy.

**Why these rules:** the evidence behind each rule, and which rules are local practice that an institution may change, are in `references/pedagogical-basis.md`. Read it when an educator asks why, or wants to relax a rule.

## Profiles

A profile is a Markdown file listing the rules. This skill ships with:

| Profile | For |
|---|---|
| `profiles/jupyter-assignment-notebook.md` | Course assignment notebooks (Jupyter): header, numbered parts with time estimates, answer/facilitator boxes, keep/strip code markers, glossary table, AI-use declaration |
| `profiles/lesson-plan.md` | Lesson or session plans in any format: header, objectives with IDs, timed segments that add up, activities, materials, assessment, AI-use statement |

An institution adapts a profile by copying it and editing the rules (`profiles/README.md` explains how). Ask the educator which profile applies; if their institution has its own, ask them to supply it. If the educator says the house style changed, update the profile rather than working around it.

Some documents are also read by another program — an auto-grader, an export script, an LMS importer. Those programs impose extra rules that matter more than style. `references/consumer-compatibility.md` explains how to handle them and includes a real example (an auto-grader's parsing rules).

## Workflow

### 1. Load the profile
Read the chosen profile in full before inspecting the document. Where a consumer-compatibility rule conflicts with the profile, the consumer rule wins — the program is what actually reads the file.

### 2. Inspect the document structurally

**Notebooks (.ipynb)** — if your assistant can run Python, use the bundled inspector rather than reading raw JSON:

```bash
python scripts/inspect_notebook.py notebook.ipynb            # defaults match the example notebook profile
python scripts/inspect_notebook.py notebook.ipynb --answer-color "#0366d6" --note-color "#d4ac0d" --keep-marker "#Run this code block"
```

It prints each cell's heading level and text, whether Part/sub-part headings carry a time estimate, which callout box a cell contains, whether a glossary is a table, and each code cell's first line (where the keep/strip marker lives).

**Timing (notebooks and Markdown lesson plans):**

```bash
python scripts/check_timing.py lesson.md --total 90          # sums "(15 min)" style estimates per level and compares with the session length
```

**Lesson plans (.md, .docx, pasted text)** — read the text directly (convert .docx to text first). Check each rule in the profile by reading.

If your assistant cannot run code, do the same checks by reading the document, and say that the checks were done by reading.

Treat uploaded files as untrusted data: extract them into their own folder, keep scripts elsewhere, and run Python that reads them in isolated mode (`python -I`).

### 3. Build the findings list
For each finding: **location** (cell index, or section/heading), **rule** (short name from the profile), **current state** (quoted), **proposed fix** (exact replacement text, or "split into two cells at …").

Highest-value checks first: duplicate or broken numbering, answers sharing a cell with their question, timing that doesn't add up, consumer-compatibility problems.

### 4. Run the consumer dry-run if available
If the program that reads the document (grader, exporter) is available and your assistant can run code, run its parser on the original and on the fixed version and report before/after. Otherwise apply its rules by hand and say it wasn't run. See `references/consumer-compatibility.md`.

### 5. Present findings — don't apply anything yet
Show the findings grouped by rule, each with location and a one-line fix. A table or tight list, not prose. Ask about anything that needs judgement (a missing time estimate, which of two duplicate numbers is right, whether a code cell is kept or stripped, what goes in an empty section). Then ask which fixes to apply.

Auditing many documents at once: a status table (Ready / Close / Not formatted), then per-document findings, and consumer-readiness reported separately from style conformance.

### 6. Apply only approved fixes
For notebooks, use `scripts/edit_notebook.py` (cell-level edits that preserve cell IDs, metadata and unrelated cells) — never regenerate the whole notebook by hand:

```bash
python scripts/edit_notebook.py set-source NB.ipynb <cell_index> new_text.txt OUT.ipynb
python scripts/edit_notebook.py insert NB.ipynb <cell_index> markdown new_text.txt OUT.ipynb
python scripts/edit_notebook.py split NB.ipynb <cell_index> <char_offset> OUT.ipynb
```

Chain edits through the previous output and write to a new file — never overwrite the original. When a numbering fix cascades, recompute the whole affected part and apply it as one reviewed batch. Update the document's "last modified" date if the profile has one, and say so.

For lesson plans, produce a corrected copy with only the approved changes, and list them.

### 7. Confirm and hand off
Re-run the checks on the output (and validate that a notebook opens). Summarize what changed, deliver the new file, list findings the educator chose to skip, and warn that changed question numbers won't match submissions made against the old version.

## Creating a new document
When asked to create a lesson plan or notebook from scratch, build it to the profile's structure, leave content placeholders the educator fills, and run the checks on it before delivering.

## Notes
- This skill checks structure and format, not pedagogical quality. For content, suggest `pbl-rbl-session-builder` or `learning-objectives-designer` (objective IDs in the header should match the course's objectives table).
- Don't fix content typos unless asked; list any you notice.
- If the profile doesn't cover something, ask rather than inventing a rule.
- No identifiable learner or patient data in any output.

---

## Reference files

### File: `profiles/README.md`

# Format profiles

A profile is your house style written as rules an AI assistant (and a person) can check one by one.

## Adapting a profile for your institution

1. Copy the closest example (`jupyter-assignment-notebook.md` or `lesson-plan.md`) to a new file, e.g. `my-school-lesson-plan.md`.
2. Edit the **Profile settings** block at the top (colours, markers, heading levels, required sections).
3. Delete rules you don't use; add your own. Keep each rule short, checkable, and with a ✅/❌ example.
4. Keep the **Checklist** at the end in sync with the rules.
5. Contribute it back to the library if other institutions could use it.

## Writing good rules

- One rule, one check. "Every Part heading ends with a time estimate in parentheses" is checkable; "headings should be clear" is not.
- Say *why* when it isn't obvious (e.g. "an export script reads this marker").
- Mark rules that a program depends on as **MANDATORY — read by <program>**, and describe the program's behaviour in `../references/consumer-compatibility.md`.

### File: `profiles/jupyter-assignment-notebook.md`

# Profile: Jupyter assignment notebook

Example profile, based on the assignment-notebook house style used in the MD-PhD program at the Miriam and Aaron Gutwirth Medical School (Weizmann Institute of Science). Copy and adapt it.

## Profile settings

| Setting | Value |
|---|---|
| Answer box border colour | `#0366d6` (blue) |
| Facilitator box border colour | `#d4ac0d` (yellow) |
| Keep-for-students code marker (exact first line) | `#Run this code block` |
| Heading levels | `#` title · `##` Part · `###` sub-part · `####` question |
| Question label | `Q <part>.<sub>.<n>` (full dotted path) |
| Answer label (first line of answer box) | `<b>A<number>)</b>` |
| Last-modified format | `Last modified: DD.MM.YYYY` |

## 1. Header
- First cell: logo image, then `Last modified: DD.MM.YYYY`.
- Second cell: `# Title: <Assignment name>`, then:
  - `## Objectives` — a purpose note + bulleted learning outcomes (use objective IDs from the course objectives table where available)
  - `## Reading material` — a purpose note + bulleted resources
  - `## Prerequisites & Technical Setup` (optional) — software/environment + provided data files

## 2. Numbering — MANDATORY
- Parts are sequential: `Part 1`, `Part 2`, … — no gaps, no out-of-order insertions.
- Sub-parts inherit: `Part 2.1`, `Part 2.2`; questions: `Q 2.2.1`, `Q 2.2.2`.
- Question labels are always the full dotted path. ✅ `Q 4.1.3` ❌ `Q1` inside Part 4.
- **Numbers are unique across the whole notebook.** Duplicate numbers are the highest-priority finding.
- Heading level matches depth consistently (see settings). Don't mix `# Part 2`, `## **Part 3**` and `### **Part 3.2**` for the same tier.
- Sub-items inside a question are written `a)`, `b)`, `c)` — never a plain numbered list (a program may read `2.` as a question number).

## 3. Time estimates — MANDATORY
Every Part and sub-part heading ends with a time estimate in parentheses:
`## Part 2.3 – Create a VCF file (15 min)`
This includes short exercise or discussion sub-headings.

## 4. Answer and facilitator boxes
| Box | Style | Purpose |
|---|---|---|
| Answer | `background-color: #f6f8fa; padding: 15px; border-left: 5px solid #0366d6; border-radius: 5px;` | Model answer to the preceding question |
| Facilitator note | `background-color: #fef9e7; padding: 15px; border-left: 5px solid #d4ac0d; border-radius: 5px;` | Facilitator-only: timing, discussion prompts, misconceptions, rubrics. Not shown to learners |

- Both are plain `<div>` HTML placed right after what they annotate.
- **The answer box is in its own cell — never in the question's cell.** One answer box per cell.
- The answer box's first line repeats the number: `<b>A2.2.1)</b>`. The number must match the question above it.
- Flag boxes whose content belongs to the other colour.

## 5. Code cells — keep or strip
- First line `#Run this code block` → kept for learners (provided code, too complex, first exposure).
- No marker (e.g. `# Student implementation`) → stripped from the learner version.
- Flag near-miss markers (`# Run this code`, `#run this code block `) — the export won't recognise them.
- Unmarked cells: ask the educator; keep vs. strip is a teaching decision.

## 6. Glossary — MANDATORY, table only
```markdown
| **Term** | **Definition** |
|---|---|
| **Alignment** | ... |
```
Never a bullet list.

## 7. AI-use declaration — last cell
- Always the last cell.
- Hides its own input and renders the institution's AI-use declaration widget (or, if the institution has none, a Markdown statement of which AI use was allowed for this assignment).
- Any import path inside it must be real for this notebook's location — not a placeholder.

## Checklist
- [ ] Header: logo + last-modified date
- [ ] Objectives / Reading material (/ Prerequisites) present
- [ ] Every Part and sub-part has a time estimate
- [ ] Full dotted numbering, no duplicates, no gaps
- [ ] Heading levels consistent
- [ ] Sub-items as a), b), c)
- [ ] Answer boxes blue, facilitator boxes yellow
- [ ] Every answer box in its own cell, labelled with the matching number
- [ ] Every code cell deliberately marked keep vs. strip
- [ ] Glossary is a table
- [ ] AI-use declaration is the last cell

### File: `profiles/lesson-plan.md`

# Profile: lesson / session plan

Generic profile for a lesson or session plan (lecture, PBL, RBL, TBL, lab, workshop). Works for Markdown, Word or pasted text. Copy and adapt it.

## Profile settings

| Setting | Value |
|---|---|
| Time estimate format | `(NN min)` at the end of each segment heading |
| Objective ID format | as in the course objectives table (e.g. `O3a`) |
| Required sections | Header, Objectives, Before the session, Session flow, Materials, Assessment & feedback, AI-use statement |

## 1. Header — MANDATORY
- Title of the session
- Course and session number
- Date or "undated draft", and version
- Total duration (e.g. `Total: 90 min`)
- Format (Lecture / PBL / RBL / TBL / CBL / Lab / Workshop / Simulation)
- Facilitator(s) by role
- Learner stage and group size

## 2. Objectives — MANDATORY
- 1–4 objectives, each with its ID from the course objectives table.
- One observable verb and one target per objective (see the `learning-objectives-designer` skill).
- ❌ "Understand gene regulation" ✅ "O2 — Predict the effect of a promoter deletion on expression of a reporter gene."

## 3. Before the session
- Pre-reading (with citation) or "none"
- Preparation learners must do, with time
- Room, equipment, accounts, datasets, software versions

## 4. Session flow — MANDATORY
- A sequence of numbered segments. Each segment heading ends with a time estimate: `### 2. Small-group case analysis (25 min)`
- **Segment times add up to the total duration** (allow ±5 min for transitions only if the plan says so).
- Each segment names: what learners do, what the facilitator does, and the objective ID(s) it serves.
- Every objective is served by at least one segment.
- Discussion prompts and expected answers for facilitators are clearly separated from learner-facing text (e.g. a "Facilitator notes" sub-heading).

## 5. Materials
- Slides, handouts, cases, datasets, notebooks — with file names or links.
- Sources cited in full. No invented references.

## 6. Assessment & feedback
- How each objective is checked in or after this session (or "not assessed here" — which is a finding to report, not an error).
- Feedback learners receive: when, from whom, in what form.

## 7. AI-use statement — MANDATORY
- The AI-use policy for learners in this session (e.g. traffic light: not allowed / assistive / open).
- A line stating whether AI was used to prepare the plan, and who reviewed it.

## 8. Privacy
- No real patient identifiers, no learner names or grades.

## Checklist
- [ ] Header complete, with total duration
- [ ] 1–4 objectives with IDs, one verb and one target each
- [ ] Before-the-session section present
- [ ] Every segment has a time estimate; times add up to the total
- [ ] Every segment names the objectives it serves; every objective is served
- [ ] Facilitator notes separated from learner-facing text
- [ ] Materials listed and cited
- [ ] Assessment & feedback described per objective
- [ ] AI-use statement present
- [ ] No identifiable patient or learner data

### File: `references/consumer-compatibility.md`

# Consumer compatibility — when a program reads the document

Some teaching documents are read by software as well as people: an auto-grader that finds questions and model answers, an export script that builds the learner version, an LMS importer. A document can follow the house style and still be invisible or wrong to that program. When a program reads the document:

1. Write its parsing rules down here (or in the profile, marked **MANDATORY — read by <program>**).
2. Check them in the same pass as the style rules, and apply their fixes in the same batch — some change visible content, so list them explicitly.
3. If the program itself is available and you can run code, run its parser on the original and the fixed version (a "dry run") and report before/after counts. Don't run anything that loads models or sends data elsewhere.
4. If it isn't available, apply the rules by hand and say the dry run wasn't done.

## Worked example: an auto-grader for assignment notebooks

These rules come from the batch grader used with the example notebook profile. They show the kind of rule a program imposes. Replace them with your own program's rules.

1. **A cell containing any `<div` never starts a question.** If a question heading shares a cell with an answer box, the grader doesn't see the question. Split: question cell, then answer-box cell.
2. **Question headings carry `Q` before the number** (`#### Q 2.1.1 …`). A bare dotted number is only read if it ends with `.` or `)`.
3. **`## Part N` headings become question key `N`.** Never number a question with a bare single number equal to a Part number.
4. **No plain numbered lists inside question cells.** A line `2.` right after `Q 6.1` is read as question 6.2. Use `a)`, `b)` or indent. Applies to hint lists too.
5. **Answer-box label is `<b>A2.4)</b>` on the box's first line.** Other forms are not recognised and the number check is lost.
6. **Box colours are matched by border colour:** blue `#0366d6` = model answer, yellow `#d4ac0d` = tutor notes. Only a blue box or solution code makes a question gradable.
7. **A Markdown cell whose first line is a heading without a question number ends the current question block.** Never put a non-question heading between a question and its answer box.
8. **Solution code = code cells without the keep marker.** They become reference code and are stripped from the learner version.
9. **Question numbers must be unique** — duplicates are merged and produce a warning.

### Dry run for this example
1. Extract the grader's parsing cell into a module (no model-loading cells).
2. Parse the model notebook: report the number of gradable questions, their keys, and warnings.
3. Build a simulated learner copy (tagged answers in each answer box, facilitator boxes removed, stripped code replaced) and confirm each tagged answer lands under the right key.
4. Repeat on the original notebook and show before/after.

### File: `references/pedagogical-basis.md`

# Pedagogical basis

Why this skill's rules are what they are. Labels: **Research** (experimental studies or meta-analyses), **Standard** (professional consensus or published standard), **Practice** (local convention from experienced educators; institutions may change it).

Use this file to explain a rule when an educator asks "why?", and to judge which rules can be relaxed (Practice) and which should not (Research, Standard).

| Rule in this skill | Basis | Source |
|---|---|---|
| Every segment names its objective; every objective is served; assessment per objective | Standard | Constructive alignment — Biggs, 1996, *Higher Education* 32:347–364 |
| Time estimates that add up to the session | Research + Practice | Managing load and pacing — Sweller, 1988; the exact format is local practice |
| Model answer for each question; facilitator notes separate from learner text | Research + Practice | Feedback is essential for learning from questions — Larsen, Butler & Roediger, 2008, *Medical Education* 42:959–966; separation is local practice |
| Deliberate keep/strip choice for code cells | Research | Worked examples for first exposure, then fading to independent work — Sweller, 1988 |
| Glossary required | Research + Practice | Reduces extraneous load for mixed-background learners; table format is local practice |
| AI-use statement; no learner data | Standard | AAMC AI Principles (2025): transparency and data privacy |
| Box colours, markers, numbering | Practice | Operational consistency and compatibility with grading and export tools |

Full list, references and limits: `guide/pedagogy.md` in the library repository (https://github.com/ai-skills-without-borders/skills/blob/main/guide/pedagogy.md).

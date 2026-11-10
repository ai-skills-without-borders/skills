---
name: lesson-format-checker
description: Checks a lesson plan, session plan or course/assignment Jupyter notebook against an institution's house-style format profile, reports every deviation with a proposed fix, and applies only the fixes the educator approves, in a new copy. Use whenever an educator uploads or points to a lesson plan, session plan or assignment notebook (.ipynb, .md, .docx) and asks to check, review, audit, lint, validate or "fix the format" of it, asks whether it follows the house style or template, wants timing checked against the session length, or wants a new lesson or notebook created in the standard structure. Ships with two example profiles (a Jupyter assignment-notebook profile and a generic lesson-plan profile) that institutions copy and adapt. Does not judge pedagogical quality and is not for generic data-analysis notebooks unrelated to teaching.
---

# Lesson & Notebook Format Checker

Checks a teaching document against a **format profile** — the institution's house style written down as checkable rules — then helps fix it interactively. It never silently rewrites the educator's file: findings first, then only the approved fixes, in a new copy.

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

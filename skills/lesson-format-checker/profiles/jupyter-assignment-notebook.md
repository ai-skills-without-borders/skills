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

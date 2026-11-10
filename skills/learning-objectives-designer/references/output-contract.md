# Output contract — the objectives table

Other skills in this library read this table. Keep the columns, order and ID format exactly.

## Columns

| Column | Content | Example |
|---|---|---|
| `id` | Stable ID. Course-level `C1…`, session/module-level `O1…`; splits get letters `O3a`, `O3b` | `O3a` |
| `parent_id` | Course objective this one builds, or empty | `C2` |
| `objective` | Full sentence, starting with the verb (stem omitted) | `Design a diagnostic work-up for suspected acute kidney injury.` |
| `verb` | The action verb | `design` |
| `level_3` | 1 Foundational, 2 Applied, 3 Advanced | `3` |
| `bloom` | Remember / Understand / Apply / Analyze / Evaluate / Create | `Create` |
| `scope` | course / module / session / assignment, plus its name | `session: Renal PBL 2` |
| `activities` | Where learners practise it | `PBL phase 3; Lab 4` |
| `assessment` | How it is checked, or `NONE` | `OSCE station 2` |
| `framework_links` | `ID:E/P` pairs, or empty | `GREAT-RS2:E` |
| `source` | Source IDs or `educator, conversation` | `S2 slide 4; S5` |
| `status` | `draft` / `approved` / `planned` | `draft` |
| `notes` | Flags: aspiration, level mismatch, split from X | `split from original O3` |

## Markdown example

| id | parent_id | objective | verb | level_3 | bloom | scope | activities | assessment | framework_links | source | status | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| O3a | C2 | Explain the three mechanistic categories of acute kidney injury. | explain | 1 | Understand | session: Renal PBL 2 | PBL phase 1 | Quiz Q4 | | S2 | draft | split from original O3 |
| O3b | C2 | Design a diagnostic work-up for a patient with suspected acute kidney injury. | design | 3 | Create | session: Renal PBL 2 | PBL phase 3 | NONE | | S2 | draft | split from original O3; no assessment yet |

## CSV

Same columns, same order, UTF-8, comma-separated, header row first. Quote fields that contain commas.

## Changelog

When revising, add a section under the table:

```
Changelog
- v2 (date): O3 split into O3a/O3b (R1 one target). O5 level 2 → 1 to match quiz.
```

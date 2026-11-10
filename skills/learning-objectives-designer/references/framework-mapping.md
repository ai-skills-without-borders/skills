# Mapping objectives to a competency framework

## Principle

Competency frameworks are national or institutional agreements. The AAMC states that no externally developed set of competencies should be used without careful, formal faculty review. So this skill only **proposes** links; the course leader decides.

## Getting the framework

Ask the educator for the framework document. Common ones in medical and biomedical research education:

| Framework | Use for | Where to get it |
|---|---|---|
| Institutional EPAs / competencies | Courses in that program | The program office |
| AAMC/AACOM/ACGME *Foundational Competencies for Undergraduate Medical Education* (2024) | MD/DO curricula | aamc.org (CBME pages) |
| AAMC GREAT *MD-PhD Competencies Development Toolkit* (16 competencies, 4 domains, milestones) | Physician-scientist / MD-PhD training | aamc.org (GREAT group pages) |
| AAMC *AI Competencies Across the Learning Continuum* (2026) | AI-related courses and sessions | aamc.org (AI competencies) |
| Core EPAs for Entering Residency (2014) | Legacy MD curricula still using them | aamc.org |

Never reconstruct framework wording or numbering from memory. If the educator can't supply the document, map to framework **names only** ("research skills domain") and mark every link `UNVERIFIED — confirm against the framework document`.

A framework can be supplied as a file in the library's `frameworks/` format (see the repository's `frameworks/README.md`), as a pasted list, or as a PDF.

## Procedure

1. List each objective with its activities and assessments (from Step 4).
2. For each objective, scan the framework's lowest-level items (sub-competencies, sub-EPAs). Ask: does the learner **perform** this here? Is it **assessed**?
3. Assign E / P / X:
   - **E (evidence):** performed and assessed, producing something that can be recorded (graded product, rubric, observation form).
   - **P (practice):** performed, not assessed.
   - **X (exposure):** only learned about. Not listed as a link — reported separately.
4. Cite the activity and source for each E/P link.
5. Prefer fewer, defensible links. If one session objective links to more than three framework items at E level, re-check each.
6. Report **cheap upgrades**: P links that would become E with a small change (a rubric, a feedback form, a reflection prompt).

## Output columns

Add to the objectives table: `framework_links` as `ID:level` pairs, e.g. `FC-PC2:E; GREAT-RS1:P`. Use the framework's own IDs; if it has none, create short stable codes and give the key in a legend under the table.

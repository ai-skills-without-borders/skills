# Objective quality rules

Check every objective against these rules. Report each failure with the rule name and a proposed rewrite.

## R1 — One target

An objective has exactly one action and one object.

- ✗ "Explain the mechanism of AKI and design a diagnostic work-up." → two objectives.
- ✓ O3a "Explain the three mechanistic categories of acute kidney injury."
- ✓ O3b "Design a diagnostic work-up for a patient with suspected acute kidney injury."

Lists of examples inside one target are fine ("…for at least three of: …") as long as the action is single.

## R2 — Observable verb

One verb from `levels-and-verbs.md`. No "understand", "know", "appreciate".

## R3 — Specific to this content

- ✗ "Apply critical thinking to research." (true of every course)
- ✓ "Critique the control design of a single-cell RNA-seq experiment."

## R4 — Assessable here

If nothing in the scope does or could assess it, flag it as an aspiration. Don't delete it — ask.

## R5 — Level matches the activity

The verb's level should match what learners actually do. Mismatches are flagged (see `levels-and-verbs.md`).

## R6 — Learner-centred

Describes what the learner will do, not what the teacher will cover. ✗ "This session covers…" ✓ "Learners will be able to…"

## R7 — Reasonable scope

A single session objective should be achievable within that session. A course objective may span many sessions; link it to the session objectives that build it (`parent_id`).

## R8 — Plain language

Readable by a learner on day one. Expand acronyms on first use. No stacked jargon.

## Optional: condition and criterion

Where precision matters (skills, procedures, computational tasks), add a condition and a criterion:

"Given a raw count matrix (condition), normalize it and identify differentially expressed genes with an FDR below 0.05 (criterion)."

Don't force this onto conceptual objectives where it adds nothing.

## Simplifying for exam generation

When objectives will feed automated question generation, R1 matters most: a compound or broad objective produces vague, unfocused items. When in doubt, split.

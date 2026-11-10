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

# Export formats

## Moodle GIFT (single best answer)

One question per block, blank line between blocks. `=` marks the correct answer, `~` a wrong answer, `#` the feedback for that option. Escape the special characters `~ = # { } :` with a backslash inside text.

```
// Objective O3a | Level 2 | Item E-O3a-01
::E-O3a-01::A 58-year-old man presents with ... Which of the following is the most likely cause?{
~Prerenal azotemia#Feedback: why wrong ...
=Acute tubular necrosis#Feedback: why right ...
~Glomerulonephritis#Feedback: why wrong ...
~Postrenal obstruction#Feedback: why wrong ...
}
```

Short answer (free text, manual grading) in GIFT is an essay question:

```
::E-O5-02::Propose two controls for this experiment and justify each.{}
```

Put rubrics for essay items in a separate document for graders.

Tags: Moodle can import categories with `$CATEGORY: course/objective-O3a` on its own line before a group of items, which keeps items organised by objective.

## CSV

Columns, in order:

`item_id, objective_id, level_3, bloom, format, stem, lead_in, option_a, option_b, option_c, option_d, option_e, key, rationale, distractor_notes, source, difficulty_estimate, status`

UTF-8, header row, quote fields that contain commas or line breaks. `status` is `draft` until reviewed.

## Markdown (default for review)

Use the templates in `item-formats.md`. For summative items, put keys and rationales in a separate section titled "Answer key — restricted".

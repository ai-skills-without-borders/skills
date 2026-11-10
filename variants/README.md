# Institutional variants

A variant is a version of a library skill adapted for one institution: its own competency framework, template, terminology, language or local rules. Variants let a school use the library without waiting for a shared skill to fit everyone, and they show the community which adaptations are common enough to fold back into the shared skill.

## Before you make a variant

Most adaptations don't need one. Try these first, in order:

1. **Configure.** Many skills take your institution's material as input: a competency framework (`frameworks/`), a format profile (`lesson-format-checker/profiles/`), a syllabus template, your AI-use wording. Supply those and the shared skill adapts.
2. **Improve the shared skill.** If your change would help other schools too, propose it to the shared skill (see `CONTRIBUTING.md`). Everyone benefits, and you don't maintain a copy.
3. **Make a variant** only when the change is specific to your institution and can't be expressed as configuration.

## Structure

```
variants/
  <institution-slug>/                 e.g. mssm, weizmann
    <skill>-<institution-slug>/       e.g. syllabus-builder-mssm
      SKILL.md                        name: syllabus-builder-mssm
      card.yaml                       variant_of: syllabus-builder
      references/ …
```

- The folder name and the `name` in `SKILL.md` must be identical, and must differ from the shared skill's name, so both can be installed side by side.
- `card.yaml` uses the same fields as a shared skill, plus:
  ```yaml
  variant_of: syllabus-builder        # the shared skill it adapts
  institution: Icahn School of Medicine at Mount Sinai
  changes: >
    What differs from the shared skill, in one or two sentences.
  ```
- Keep the shared skill's principles: no invention, educator approval, AI-use line, privacy.

## Ownership and approval

Each variant is owned by its institution. Changes to a variant need approval from one of its listed maintainers; library maintainers check only the shared principles and the automated validation. Variants appear on their parent skill's page on the website.

## Folding back

When two or more institutions make the same change, the library maintainers will propose moving it into the shared skill, with credit to the variant authors.

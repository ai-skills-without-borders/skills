# Contributing

Thank you. There are six ways to contribute, from easiest to most involved.

## 1. Report how a skill worked for you (most valuable)

Used a skill for real teaching or preparation? Fill in a usage report — through the **Usage report** issue form on GitHub, or the web form linked from the catalog site. It takes about five minutes and is what moves a skill from `draft` to `tested-elsewhere`. See [community/usage-report.md](community/usage-report.md) for the questions.

## 2. Suggest a fix

Found a problem in a skill? Open an issue describing what you asked, which tool you used, what happened and what you expected. Don't include patient data, learner data, or unpublished material.

## 3. Improve an existing skill

- **In plain words:** open the *Suggest a change* issue form. Say what should change, why, and (optionally) the wording.
- **Directly:** on the skill's page on the website, choose *Edit on GitHub*, or open the file on GitHub and press the pencil icon. Make your change and choose *Propose changes*. GitHub makes a copy (fork) under your account and opens a pull request; nothing changes in the library until a maintainer approves it.
- **Approval:** see the table in [GOVERNANCE.md](GOVERNANCE.md#how-changes-are-approved). Bigger changes also need a reviewer from another institution.

## 4. Adapt a skill for your institution

1. **Configure first.** Supply your framework (`frameworks/`), format profile, template or AI-use wording. Most adaptations need nothing more.
2. **Share what generalizes.** If others would benefit, improve the shared skill (section 3).
3. **Make a variant** for what is truly local: see [variants/README.md](variants/README.md). Your institution owns and approves its variants.

## 5. Contribute a format profile or framework file

- **Format profile** for `lesson-format-checker`: copy a profile in `skills/lesson-format-checker/profiles/`, adapt it, and submit it.
- **Framework file**: see [frameworks/README.md](frameworks/README.md). Only contribute frameworks whose license allows redistribution; otherwise contribute a pointer file.

## 6. Contribute a new skill

### Without GitHub
Send the skill folder (zipped) or the text of your instructions through the **New skill** form. A maintainer will turn it into a pull request with you as author.

### With GitHub
1. Fork the repository and create `skills/<your-skill-name>/`. The name is lowercase with hyphens.
2. Add `SKILL.md` with frontmatter:
   ```yaml
   ---
   name: your-skill-name            # must equal the folder name
   description: What it does and exactly when to use it — the trigger phrases educators would say. Under 1,024 characters.
   ---
   ```
3. Add `card.yaml` (copy one from another skill; start at `maturity: draft`).
4. Put long detail in `references/` and load it from `SKILL.md` only when needed. Keep `SKILL.md` focused — under about 500 lines.
5. Run `python tools/build.py --check`. Fix every error.
6. Open a pull request. A maintainer and, where possible, a reviewer from another institution will look at it with [community/review-checklist.md](community/review-checklist.md).

### What makes a good skill here

- **Solves a real, recurring teaching task**, and says so in the description with the words educators actually use.
- **Tool-agnostic.** Don't name one product's internal tools. Say "ask the educator", "if your assistant can create files…".
- **Follows the library principles** (README): no invention, educator approves, AI-use line, privacy, honest maturity.
- **Plays well with the others.** Uses objective IDs from `learning-objectives-designer` where objectives matter.
- **Scripts are optional.** If a step runs code, the skill must also say how to do it by reading when code can't run, and `runs_code: true` goes in the card.
- **Has an example.** An `examples/` folder with one realistic, de-identified input and the output it should produce helps reviewers and users.

## Licensing of contributions

By contributing you agree that skill content is released under CC BY 4.0 and code under MIT, and that you have the right to release it. Don't include text you can't license (copyrighted frameworks, commercial exam items, paywalled figures).

## Conduct

Be collegial. Critique ideas, not people. Assume good intent across institutions, countries and languages.

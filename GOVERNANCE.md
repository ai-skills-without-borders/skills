# Governance

How skills enter the library, how their maturity is labelled, and who decides.

## Roles

- **Maintainers** — merge changes, run releases, keep the catalog honest. Currently: Amit Shraga (Weizmann) and Talia Swartz (Mount Sinai). The list grows with founding institutions.
- **Skill maintainer** — the person responsible for one skill: answers issues, updates it when tools change. Named in its `card.yaml`.
- **Reviewers** — educators from an institution *other* than the skill's origin, who test and review a skill using [community/review-checklist.md](community/review-checklist.md).
- **Contributors** — anyone who submits a skill, a fix, a profile, or a usage report.

## Maturity levels

Every skill card has a `maturity` field. It describes evidence, not opinion.

| Level | Meaning | Required evidence |
|---|---|---|
| `draft` | Written or generalized, not yet used with real teaching in this form | Passes `tools/build.py` validation |
| `tested-at-origin` | Used for real teaching at the origin institution | A usage report from the origin |
| `tested-elsewhere` | Used successfully at one or more other institutions | At least one usage report from another institution |
| `reviewed` | Tested elsewhere **and** independently reviewed | A completed review checklist by a reviewer from another institution |

A skill moves up only with the evidence attached (linked in `used_at` or `reviewers`). It moves down if a tool change breaks it — set `tested_in.<tool>: broken` and open an issue.

## Testing per tool

`tested_in` records, per tool: `untested`, `works`, `works-with-limits` (explain in the usage report), or `broken`. Tools: `claude`, `chatgpt`, `gemini`, `copilot` (add others as needed). Skills that run code must say what happens in tools that can't run it.

## Card fields

| Field | Meaning |
|---|---|
| `name` | Folder name and `SKILL.md` name — must match |
| `title`, `summary` | Shown in the catalog |
| `version` | Semantic version of the skill: patch = wording fix, minor = new capability, major = changed inputs/outputs |
| `tasks` | What educators search for ("Write exam questions") |
| `audience`, `inputs`, `outputs` | Who it's for, what it needs, what it produces |
| `runs_code` | Whether any step runs scripts |
| `maturity`, `tested_in`, `last_tested`, `used_at` | Evidence (see above) |
| `frameworks` | Frameworks it works with |
| `origin_institution`, `derived_from` | Where it came from |
| `maintainers`, `reviewers` | People |
| `license` | Always CC-BY-4.0 for content |
| `starter` | In the starter set shown first on the catalog |

## Decisions

Maintainers decide by consensus. Disagreements about a skill's content go to its skill maintainer first. Changes to these rules are proposed as a pull request and stay open for at least two weeks.

## Releases

Releases are tagged `vYEAR.MONTH` (e.g. `v2026.12`). Each release is archived on Zenodo with a DOI so authors can cite the exact version they used.

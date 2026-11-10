# Governance

How skills enter the library, how their maturity is labelled, and who decides.

## Roles

- **Maintainers** — merge changes, run releases, keep the catalog honest. Currently: Amit Shraga, PhD (The Miriam and Aaron Gutwirth Medical School, Weizmann Institute of Science) and Talia H. Swartz, MD, PhD (Icahn School of Medicine at Mount Sinai). The list grows with founding institutions.
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
| `maturity`, `tested_in`, `last_tested` | Evidence (see above) |
| `used_at` | Institution ids from `community/contributors.yaml` where the skill was used for real teaching |
| `frameworks` | Frameworks it works with |
| `origin_institution`, `derived_from` | Where it came from |
| `maintainers`, `reviewers` | People, each written as `Name (Institution)` |
| `license` | Always CC-BY-4.0 for content |
| `starter` | In the starter set shown first on the catalog |

## Recording contributions

Every contribution is recorded with the contributor's institution and country, so the community can see where its knowledge comes from. The issue forms ask for both, and pull requests state them in the description.

When a contribution is merged or a report is received, the approving maintainer adds it to [`community/contributors.yaml`](community/contributors.yaml): the date, the type (skill, improvement, variant, usage report, review, workshop), the institution and, if relevant, the skill. A new institution is added there once, with its country and approximate location. A person's name is recorded only if they ticked "credit me by name". The [community page](https://ai-skills-without-borders.github.io/skills/community.html) is generated from this file, and the build checks that every entry names a known institution.

## How changes are approved

One approval is enough. The automatic checks catch format problems, and the maturity label tells users how well tested a skill is, so a change never has to wait for a committee.

| Change | Who approves | Needed |
|---|---|---|
| Any change to a shared skill, or a new skill | One maintainer (the skill's maintainer or a library maintainer) | Automatic checks pass. New skills start as `draft` |
| Institutional variant | One maintainer from that institution, or a library maintainer | Automatic checks pass |
| Maturity upgrade | One library maintainer | The evidence linked in the card (usage reports; for `reviewed`, one completed review) |

Reviews by other institutions are welcome at any time. They raise a skill's maturity label; they never block a change.

Every pull request runs `tools/build.py --check` automatically. Approvals are recorded on the pull request; `.github/CODEOWNERS` routes review requests to the right people.

## Editing paths for contributors

- **Suggest** a change in plain words with the *Suggest a change* issue form — no GitHub editing needed.
- **Edit** a skill file directly with GitHub's *Edit* button. GitHub creates a copy (fork) and a pull request for you; nothing changes until it is approved.
- **Adapt** for your institution: configure first (frameworks, profiles, templates), then propose a shared improvement, and only then create a variant (see `variants/README.md`).
- **Endorse** a skill after testing it with the *Review or endorse* issue form.

## Decisions

Maintainers decide by consensus. Disagreements about a skill's content go to its skill maintainer first. Changes to these rules are proposed as a pull request and stay open for at least two weeks.

## Releases

Releases are tagged `vYEAR.MONTH` (e.g. `v2026.12`). Each release is archived on Zenodo with a DOI so authors can cite the exact version they used.

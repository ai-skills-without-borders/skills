"""
Keep the GitHub issue forms in step with the library, so contributors choose from lists instead of typing.

- Every "Skill" dropdown lists the skills that exist now (by title, with the folder name in brackets).
- The usage-report form asks the questions the automation needs: which tool, whether it was real teaching.
- Blank issues are switched off, so every submission comes through a form and is processed the same way.

Run by tools/build.py on every build.
"""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / ".github" / "ISSUE_TEMPLATE"

TOOLS = ["Claude", "ChatGPT", "Gemini", "Microsoft 365 Copilot", "Another assistant (paste-in)"]
CONTEXT = ["Real teaching, with learners", "Preparing teaching, before learners saw it", "Trying it out"]


def skill_option(card):
    return f'{card["title"]} ({card["name"]})'


def _field(body, fid):
    return next((b for b in body if b.get("id") == fid), None)


def _usage_fields(body):
    """Replace the free-text tool field with a dropdown plus the plan, and add the teaching-context question."""
    tool = _field(body, "tool")
    if tool and tool["type"] != "dropdown":
        k = body.index(tool)
        body[k:k + 1] = [
            {"type": "dropdown", "id": "tool", "attributes": {"label": "AI tool", "options": TOOLS}, "validations": {"required": True}},
            {"type": "input", "id": "plan", "attributes": {"label": "Plan or version (optional)", "placeholder": "e.g. ChatGPT Edu, Claude Pro, Gemini Enterprise"}},
        ]
    if not _field(body, "context"):
        k = body.index(_field(body, "task"))
        body.insert(k, {"type": "dropdown", "id": "context", "attributes": {
            "label": "How did you use it?",
            "description": "Real teaching moves a skill up the maturity ladder: at the institution that wrote it, to Tested at origin; at another institution, to Tested elsewhere.",
            "options": CONTEXT}, "validations": {"required": True}})


def sync(cards):
    """Rewrite the forms if they are out of date. Returns the files changed."""
    options = [skill_option(c) for c in sorted(cards, key=lambda c: c["title"])] + ["Another skill, or not sure"]
    changed = []
    for f in sorted(FORMS.glob("*.yml")):
        if f.name == "config.yml":
            continue
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        before = yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=1000)
        body = d.get("body", [])
        sk = _field(body, "skill")
        if sk and sk["type"] == "dropdown":
            sk["attributes"]["options"] = options
        if f.name == "usage-report.yml":
            _usage_fields(body)
        after = yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=1000)
        if after != before:
            f.write_text(after, encoding="utf-8")
            changed.append(f.name)
    cfg = FORMS / "config.yml"
    want = ("blank_issues_enabled: false\n"
            "contact_links:\n"
            "  - name: Questions, or no GitHub account\n"
            "    url: https://ai-skills-without-borders.github.io/skills/about.html#contact\n"
            "    about: Write to the founders by email.\n")
    if not cfg.exists() or cfg.read_text(encoding="utf-8") != want:
        cfg.write_text(want, encoding="utf-8")
        changed.append("config.yml")
    return changed

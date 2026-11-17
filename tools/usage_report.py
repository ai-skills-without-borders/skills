"""
Record a usage report: update the skill's card and the community record.

    python tools/usage_report.py BODY_FILE --issue N --author LOGIN --date YYYY-MM-DD [--skill NAME]

From the report it sets:
  used_at      the reporting institution, if it may be listed
  tested_in    the tool used, as "works", when the output was used
  maturity     Draft -> Tested at origin (real teaching at the institution that wrote it);
               Draft or Tested at origin -> Tested elsewhere (real teaching at another institution).
               Reviewed is never set automatically.
  evidence     one more sentence, linking the report
  last_tested  the month of the report
and adds a usage-report contribution. Prints a short summary for the issue comment as its last lines.
Exits with status 2 when it can't tell the skill or the institution, so a person can help.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

import issue_to_skill as its
import issue_triage
import forms

ROOT = Path(__file__).resolve().parent.parent
LADDER = ["draft", "tested-at-origin", "tested-elsewhere", "reviewed"]
TOOL_KEYS = {"claude": "claude", "chatgpt": "chatgpt", "gemini": "gemini", "copilot": "copilot"}


def load_record():
    p = ROOT / "community" / "contributors.yaml"
    rec = yaml.safe_load(p.read_text(encoding="utf-8"))
    insts = rec.get("institutions") or {}
    if isinstance(insts, dict):  # the record keys institutions by id
        rec["institutions"] = [dict(v, id=k) for k, v in insts.items()]
    return p, rec


def find_institution(rec, name, author):
    insts = rec.get("institutions") or []
    if name:
        n = name.lower()
        for i in insts:
            if i["id"] == n or i["name"].lower() == n or n in i["name"].lower() or i["name"].lower() in n:
                return i["id"]
    # No usable answer: the institution of the author's earlier contributions (GitHub submissions only).
    for c in reversed(rec.get("contributions") or [] if author else []):
        if str(c.get("github", "")).lower() == author.lower():
            return c["institution"]
    return ""


def origin_id(rec, card):
    o = (card.get("origin_institution") or "").lower()
    for i in rec.get("institutions") or []:
        if i["name"].lower() == o or i["name"].lower() in o or o in i["name"].lower():
            return i["id"]
    return ""


LOG = ROOT / "community" / "report-log.yaml"


def log_change(issue, what):
    """What each automatic report changed, so a maintainer can withdraw it with one label."""
    log = yaml.safe_load(LOG.read_text(encoding="utf-8")) if LOG.exists() else None
    log = log or {}
    log[int(issue)] = {k: v for k, v in what.items() if v}
    LOG.write_text("# What each automatic usage report changed; read by tools/withdraw_report.py.\n"
                   + yaml.safe_dump(log, sort_keys=True, allow_unicode=True, width=1000), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("body")
    ap.add_argument("--issue", required=True)
    ap.add_argument("--author", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--skill", default="")
    a = ap.parse_args()
    body = Path(a.body).read_text(encoding="utf-8")
    f = its.parse_form(body)
    get = lambda p: its.field(f, p)

    skill = a.skill or issue_triage.find_skill(get("Skill") or body)
    if not skill:
        print("Could not tell which skill this report is about.", file=sys.stderr)
        sys.exit(2)
    rec_path, rec = load_record()
    inst = find_institution(rec, get("Institution"), a.author)
    if not inst:
        print("The institution is not yet on the community map; a maintainer will add it.", file=sys.stderr)
        sys.exit(2)
    inst_name = next(i["name"] for i in rec["institutions"] if i["id"] == inst)

    card_path = ROOT / "skills" / skill / "card.yaml"
    text = card_path.read_text(encoding="utf-8")
    header = "".join(l for l in text.splitlines(True) if l.startswith("#"))
    card = yaml.safe_load(text)
    changes = []

    form = bool(get("How did you use it"))
    if not form:
        # A report in free text can't say for sure whether this skill's output was used in teaching,
        # so nothing is changed; the contributor is asked to send it through the form.
        print("needs-form", file=sys.stderr)
        sys.exit(3)
    # Only the form's explicit answer counts as real teaching. A report written as free text may describe
    # earlier teaching, not use of this skill's output, so it never moves the maturity level by itself.
    real = form and "real teaching" in get("How did you use it").lower()
    outcome = get("Outcome").lower()
    used = "not used" not in outcome
    listing = form and "[x]" in get("Listing").lower()
    tool_answer = get("AI tool").lower()
    tool = next((v for k, v in TOOL_KEYS.items() if k in tool_answer), "")

    if listing and inst not in (card.get("used_at") or []):
        card["used_at"] = (card.get("used_at") or []) + [inst]
        changes.append(f"added {inst_name} to the institutions using it")
    tool_shown = next((t for t in forms.TOOLS if t.lower() == get("AI tool").strip().lower()), "")
    if tool and used and (card.get("tested_in") or {}).get(tool) != "works":
        card.setdefault("tested_in", {})[tool] = "works"
        changes.append(f"marked it as working in {tool}")
    level = card.get("maturity", "draft")
    if real and used:
        target = "tested-at-origin" if inst == origin_id(rec, card) else "tested-elsewhere"
        if LADDER.index(target) > LADDER.index(level) and level != "reviewed":
            card["maturity"] = target
            changes.append(f"moved it from {level} to {target}")
    tool_shown = next((t for t in forms.TOOLS if t.lower() == get("AI tool").strip().lower()), "")  # only known answers reach the page
    sentence = (f"Used {'in real teaching' if real else 'in preparation or a trial'} at {inst_name}"
                f"{f' with {tool_shown}' if tool_shown and not tool_shown.lower().startswith('another') else ''}"
                f", as reported in issue #{a.issue}.")
    ev = (card.get("evidence") or "").strip()
    if f"#{a.issue}" not in ev:
        card["evidence"] = (ev + " " + sentence).strip()
        changes.append("added the report to the evidence line")
    last_before = card.get("last_tested")
    card["last_tested"] = a.date[:7]

    card_path.write_text(header + yaml.safe_dump(card, sort_keys=False, allow_unicode=True, width=1000), encoding="utf-8")
    log_change(a.issue, {"skill": skill, "institution": inst,
                         "added_used_at": inst if any("institutions using it" in c for c in changes) else None,
                         "tested_in": tool if any("working in" in c for c in changes) else None,
                         "maturity_from": level if card.get("maturity") != level else None,
                         "last_tested_from": str(last_before) if last_before and str(last_before) != a.date[:7] else None,
                         "sentence": sentence if any("evidence" in c for c in changes) else None})

    link = f"https://github.com/ai-skills-without-borders/skills/issues/{a.issue}"
    if not any(c.get("link") == link for c in rec.get("contributions") or []):
        name = get("Your name")
        lines = [f"  - date: {a.date}", "    type: usage-report", f"    institution: {inst}", f"    skill: {skill}"]
        if name and "[x]" in get("Credit").lower():
            lines.append(f"    person: {json.dumps(name, ensure_ascii=False)}")
        lines += ([f"    github: {a.author}"] if a.author else []) + [f"    link: {link}"]
        with rec_path.open("a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        changes.append("recorded the report on the community page")

    print(skill)
    print("; ".join(changes) if changes else "nothing new to record")


if __name__ == "__main__":
    main()

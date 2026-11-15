"""
Decide what an issue is from what it says, not only from the label it arrived with.

People pick the wrong form, or none: a usage report written as a plain issue, or a report filed under
"New skill". The intake workflow runs this on every new or edited issue and fixes the label, so the right
automation runs and the contributor is told what happened.

    python tools/issue_triage.py BODY_FILE --title "..." --labels "a,b"
prints:  kind=<new-skill|usage-report|other>  skill=<folder or empty>  relabel=<yes|no>  reason=<text>
"""
import argparse
import re
from pathlib import Path

import yaml

import issue_to_skill as its

ROOT = Path(__file__).resolve().parent.parent
KINDS = ("new-skill", "usage-report", "improvement", "review", "bug")  # the labels the forms apply

USE_WORDS = r"\b(used|use|using|uses|tried|ran|run|cohorts?|class(es)?|course|students|learners|taught|teaching|semester|session|workshop)\b"
NEW_WORDS = r"\b(new skill|share (a|my) skill|propose a skill|skill\.md|instructions for the ai)\b"


def skills():
    out = []
    for f in sorted((ROOT / "skills").glob("*/card.yaml")):
        c = yaml.safe_load(f.read_text(encoding="utf-8"))
        out.append((c["name"], c["title"]))
    return out


def find_skill(text):
    """The skill a text is about: its folder name, its title, or a dropdown answer "Title (folder)"."""
    t = text.lower()
    m = re.search(r"\(([a-z0-9-]+)\)", t)
    names = skills()
    if m and m.group(1) in {n for n, _ in names}:
        return m.group(1)
    hits = [(n, t.count(n) * 3 + t.count(title.lower()) * 2) for n, title in names]
    hits = [h for h in hits if h[1] > 0]
    return max(hits, key=lambda h: h[1])[0] if hits else ""


def classify(body, title="", labels=()):
    fields = its.parse_form(body)
    keys = {k.lower() for k in fields}
    text = f"{title}\n{body}"
    skill = find_skill(fields.get("Skill", "") or text)
    # Forms leave their headings in the issue; they are the strongest signal.
    if any(k.startswith("instructions") for k in keys) and any(k.startswith("purpose") for k in keys):
        return "new-skill", skill, "it has the fields of the new-skill form"
    if {"outcome"} <= keys or any(k.startswith("how did you use it") for k in keys):
        return "usage-report", skill, "it has the fields of the usage-report form"
    label = next((l for l in labels if l in KINDS), "")
    if label and label != "new-skill":
        return label, skill, "its form label"
    # No form: read the words.
    uses = len(re.findall(USE_WORDS, text, re.I))
    if skill and uses >= 2 and not re.search(NEW_WORDS, text, re.I):
        return "usage-report", skill, f"it describes using {skill} in teaching"
    if re.search(NEW_WORDS, text, re.I) or re.search(r"^---\s*\nname:\s*\S+\s*\ndescription:", body, re.M):
        return "new-skill", skill, "it describes a new skill"
    return label or "other", skill, "no clear match"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("body")
    ap.add_argument("--title", default="")
    ap.add_argument("--labels", default="")
    a = ap.parse_args()
    labels = [l.strip() for l in a.labels.split(",") if l.strip()]
    kind, skill, reason = classify(Path(a.body).read_text(encoding="utf-8"), a.title, labels)
    has = kind in labels
    other_kinds = [l for l in labels if l in KINDS and l != kind]
    print(f"kind={kind}")
    print(f"skill={skill}")
    print(f"relabel={'yes' if kind in KINDS and (not has or other_kinds) else 'no'}")
    print(f"remove={' '.join(other_kinds)}")
    print(f"reason={reason}")


if __name__ == "__main__":
    main()

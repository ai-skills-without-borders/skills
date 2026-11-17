"""
Withdraw a usage report that was recorded automatically: undo exactly what it changed.

    python tools/withdraw_report.py ISSUE

Run by the intake workflow when a maintainer adds the label "withdrawn" to a usage-report issue.
Removes the report from the community record and, on the skill's card, the evidence sentence,
the institution and the tool result it added, and restores the maturity level it changed.
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "community" / "report-log.yaml"
REC = ROOT / "community" / "contributors.yaml"


def main():
    issue = int(sys.argv[1])
    log = (yaml.safe_load(LOG.read_text(encoding="utf-8")) if LOG.exists() else None) or {}
    what = log.pop(issue, None)
    if not what:
        print("No automatic changes recorded for this issue.")
        return
    card_path = ROOT / "skills" / what["skill"] / "card.yaml"
    text = card_path.read_text(encoding="utf-8")
    header = "".join(l for l in text.splitlines(True) if l.startswith("#"))
    card = yaml.safe_load(text)
    if what.get("sentence"):
        card["evidence"] = " ".join(card.get("evidence", "").replace(what["sentence"], "").split())
        if not card["evidence"]:
            card.pop("evidence")
    if what.get("added_used_at"):
        card["used_at"] = [u for u in card.get("used_at") or [] if u != what["added_used_at"]]
    if what.get("tested_in"):
        card.setdefault("tested_in", {})[what["tested_in"]] = "untested"
    if what.get("last_tested_from"):
        card["last_tested"] = what["last_tested_from"]
    if what.get("maturity_from"):
        card["maturity"] = what["maturity_from"]
    card_path.write_text(header + yaml.safe_dump(card, sort_keys=False, allow_unicode=True, width=1000), encoding="utf-8")

    # Remove the contribution entry (the block whose link ends with /issues/<n>).
    lines = REC.read_text(encoding="utf-8").splitlines(True)
    out, block = [], []
    for ln in lines + ["  - end\n"]:
        if ln.startswith("  - "):
            if not any(f"/issues/{issue}\n" in b for b in block):
                out += block
            block = [ln]
        elif block:
            block.append(ln)
        else:
            out.append(ln)
    REC.write_text("".join(out), encoding="utf-8")
    LOG.write_text("# What each automatic usage report changed; read by tools/withdraw_report.py.\n"
                   + yaml.safe_dump(log, sort_keys=True, allow_unicode=True, width=1000), encoding="utf-8")
    print(what["skill"])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Check time estimates in a lesson plan (.md / .txt) or notebook (.ipynb).

Finds headings that end with a time estimate such as "(15 min)", "(1 h)",
"(1.5 hours)", groups them by heading level, and compares the sum of the
top timed level with the session length.

Usage:
    python check_timing.py FILE [--total MINUTES]

Reports:
  - every heading with its estimate (or MISSING for numbered segment /
    Part headings without one)
  - the sum per heading level
  - for each parent heading, whether its children add up to it
  - whether the top level adds up to --total, if given

Read-only.
"""
import argparse
import json
import re
import sys

TIME_RE = re.compile(r"\(\s*(\d+(?:\.\d+)?)\s*(min|mins|minute|minutes|h|hr|hrs|hour|hours)\s*\)\s*$", re.I)
HEAD_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
SEGMENT_RE = re.compile(r"^(Part\s+\d|\d+[.)]?\s|Segment\s+\d)", re.I)


def minutes(value, unit):
    v = float(value)
    return v * 60 if unit.lower().startswith("h") else v


def lines_of(path):
    if path.endswith(".ipynb"):
        with open(path, encoding="utf-8") as f:
            nb = json.load(f)
        for cell in nb.get("cells", []):
            if cell.get("cell_type") == "markdown":
                yield from "".join(cell.get("source", [])).splitlines()
    else:
        with open(path, encoding="utf-8") as f:
            yield from f.read().splitlines()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--total", type=float, help="session length in minutes")
    args = ap.parse_args()

    try:
        heads = []
        for line in lines_of(args.file):
            m = HEAD_RE.match(line.strip())
            if not m:
                continue
            level, text = len(m.group(1)), m.group(2)
            t = TIME_RE.search(text)
            heads.append({"level": level, "text": text, "min": minutes(*t.groups()) if t else None})
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"Could not read file: {e}")

    timed = [h for h in heads if h["min"] is not None]
    if not timed:
        print("No time estimates found in headings.")
        for h in heads:
            if SEGMENT_RE.match(h["text"]):
                print(f"MISSING time estimate: {'#' * h['level']} {h['text']}")
        sys.exit(1 if args.total else 0)

    print("Headings:")
    for h in heads:
        est = f"{h['min']:g} min" if h["min"] is not None else ("MISSING" if SEGMENT_RE.match(h["text"]) else "-")
        print(f"  {'  ' * (h['level'] - 1)}{'#' * h['level']} {h['text'][:70]}  [{est}]")

    top = min(h["level"] for h in timed)
    print("\nSum per level:")
    for lvl in sorted({h["level"] for h in timed}):
        s = sum(h["min"] for h in timed if h["level"] == lvl)
        print(f"  level {lvl}: {s:g} min")

    print("\nParent vs children:")
    problems = 0
    for i, h in enumerate(heads):
        if h["min"] is None:
            continue
        kids, untimed = [], 0
        for k in heads[i + 1:]:
            if k["level"] <= h["level"]:
                break
            if k["level"] == h["level"] + 1:
                if k["min"] is not None:
                    kids.append(k["min"])
                elif SEGMENT_RE.match(k["text"]):
                    untimed += 1
        if kids:
            s = sum(kids)
            ok = abs(s - h["min"]) < 0.01
            problems += not ok
            note = f" ({untimed} child segment(s) have no estimate)" if untimed else ""
            print(f"  {'OK ' if ok else 'MISMATCH'} {h['text'][:50]}: {h['min']:g} min vs children {s:g} min{note}")
    if not problems:
        print("  all parents match their children (or have none)")

    missing = [h for h in heads if h["min"] is None and SEGMENT_RE.match(h["text"])]
    for h in missing:
        print(f"MISSING time estimate: {'#' * h['level']} {h['text']}")

    if args.total is not None:
        s = sum(h["min"] for h in timed if h["level"] == top)
        verdict = "OK" if abs(s - args.total) < 0.01 else "MISMATCH"
        print(f"\nTop level (level {top}) total: {s:g} min vs session {args.total:g} min -> {verdict}")
        problems += verdict != "OK"

    sys.exit(1 if (problems or missing) else 0)


if __name__ == "__main__":
    main()

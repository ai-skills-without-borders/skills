#!/usr/bin/env python3
"""
Print a structured, cell-by-cell view of a Jupyter notebook so it can be
checked against a format profile (see ../profiles/).

Usage:
    python inspect_notebook.py NOTEBOOK.ipynb [--answer-color HEX]
                               [--note-color HEX] [--keep-marker TEXT]

Defaults match profiles/jupyter-assignment-notebook.md. Pass your own
values if your institution's profile uses different colours or markers.

For each cell it prints:
  markdown: heading level + text, whether Part/sub-part headings carry a
            time estimate, which callout box the cell contains, whether a
            glossary is a table, and whether a question shares a cell with
            a box
  code:     the first non-blank line and whether it is the keep marker
            (plus near-miss markers that an export script would not match)

A summary at the end lists duplicate question numbers.

Read-only: never modifies the notebook.
"""
import argparse
import json
import re
import sys
from collections import Counter

TIME_RE = re.compile(r"\(\s*\d+(\.\d+)?\s*(min|mins|minute|minutes|h|hr|hrs|hour|hours)\s*\)", re.I)
QNUM_RE = re.compile(r"\bQ(?:uestion)?\s*(\d+(?:\.\d+)*)", re.I)
PART_RE = re.compile(r"\bPart\s+(\d+(?:\.\d+)*)", re.I)


def first_nonblank_line(text):
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def detect_heading(text):
    m = re.match(r"^(#{1,6})\s+(.*)", text.lstrip())
    if not m:
        return None, None
    return len(m.group(1)), m.group(2).strip()


def detect_box(text, answer_color, note_color):
    low = text.lower()
    boxes = []
    if answer_color.lower() in low:
        boxes.append("answer box")
    if note_color.lower() in low:
        boxes.append("facilitator box")
    return boxes


def detect_glossary(text):
    if "glossary" not in text.lower():
        return None
    if re.search(r"^\s*\|.*\|.*\|", text, re.MULTILINE):
        return "table (OK)"
    return "NOT A TABLE"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("notebook")
    ap.add_argument("--answer-color", default="#0366d6")
    ap.add_argument("--note-color", default="#d4ac0d")
    ap.add_argument("--keep-marker", default="#Run this code block")
    args = ap.parse_args()

    try:
        with open(args.notebook, encoding="utf-8") as f:
            nb = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"Could not read notebook: {e}")

    marker_norm = re.sub(r"\s+", "", args.keep_marker.lower())
    qnums = []

    for i, cell in enumerate(nb.get("cells", [])):
        src = "".join(cell.get("source", []))
        ctype = cell.get("cell_type", "?")
        print(f"\n=== Cell {i} ({ctype}) ===")

        if ctype == "markdown":
            level, heading = detect_heading(src)
            boxes = detect_box(src, args.answer_color, args.note_color)
            if level:
                print(f"HEADING level={level}: {heading}")
                if PART_RE.search(heading):
                    print(f"  time estimate present: {bool(TIME_RE.search(heading))}")
                q = QNUM_RE.search(heading)
                if q:
                    qnums.append((q.group(1), i))
                    print(f"  question number: {q.group(1)}")
                if boxes:
                    print(f"  WARNING: heading shares a cell with: {', '.join(boxes)}")
            if boxes:
                print(f"CALLOUT: {', '.join(boxes)}")
                label = re.search(r"<b>\s*A\s*([\d.]+)\s*\)\s*</b>", src)
                print(f"  answer label: {label.group(1) if label else 'none found'}")
            g = detect_glossary(src)
            if g:
                print(f"GLOSSARY: {g}")
            numbered = [l for l in src.splitlines() if re.match(r"^\d+[.)]\s", l)]
            if level and QNUM_RE.search(heading or "") and numbered:
                print(f"  WARNING: plain numbered list inside a question cell ({len(numbered)} lines)")
            if not level and not boxes and not g:
                print(f"(text) {first_nonblank_line(src)[:120]}")

        elif ctype == "code":
            line = first_nonblank_line(src)
            kept = line == args.keep_marker
            print(f"first line: {line!r}")
            print(f"  keep marker present: {kept}")
            if not kept and line.startswith("#"):
                norm = re.sub(r"\s+", "", line.lower())
                if norm == marker_norm or (norm[:8] == marker_norm[:8] and norm != marker_norm):
                    print("  WARNING: near-miss keep marker (an export script will not match it)")

    print("\n=== Summary ===")
    counts = Counter(n for n, _ in qnums)
    dups = {n: [i for m, i in qnums if m == n] for n, c in counts.items() if c > 1}
    print(f"questions found: {len(qnums)}")
    if dups:
        for n, cells in dups.items():
            print(f"DUPLICATE question number {n} in cells {cells}")
    else:
        print("no duplicate question numbers")


if __name__ == "__main__":
    main()

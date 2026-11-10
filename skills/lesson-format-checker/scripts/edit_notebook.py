#!/usr/bin/env python3
"""
Apply precise, cell-level edits to a Jupyter notebook, preserving cell IDs,
metadata and every untouched cell. Used to apply only the fixes the
educator approved.

Usage:
    # Replace the full source of one cell
    python edit_notebook.py set-source NB.ipynb <cell_index> <text_file> OUT.ipynb

    # Insert a new cell (markdown or code) at an index
    python edit_notebook.py insert NB.ipynb <cell_index> <markdown|code> <text_file> OUT.ipynb

    # Split one markdown cell into two at a character offset in its source
    python edit_notebook.py split NB.ipynb <cell_index> <offset> OUT.ipynb

OUT.ipynb is required and must differ from NB.ipynb: the original is never
overwritten. Chain edits by passing the previous OUT as the next input.
"""
import copy
import json
import os
import sys
import uuid


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(nb, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write("\n")


def as_lines(text):
    lines = text.splitlines(keepends=True)
    return lines if lines else [""]


def new_id():
    return uuid.uuid4().hex[:8]


def check_paths(src, out):
    if os.path.abspath(src) == os.path.abspath(out):
        sys.exit("Refusing to overwrite the input notebook: give a different OUT path.")


def cell_at(nb, idx):
    if not 0 <= idx < len(nb["cells"]):
        sys.exit(f"Cell index {idx} out of range (0..{len(nb['cells']) - 1}).")
    return nb["cells"][idx]


def set_source(nb_path, idx, text_path, out):
    nb = load(nb_path)
    cell = cell_at(nb, int(idx))
    with open(text_path, encoding="utf-8") as f:
        cell["source"] = as_lines(f.read())
    if cell["cell_type"] == "code":
        cell["outputs"], cell["execution_count"] = [], None
    save(nb, out)
    print(f"Updated cell {idx}. Wrote {out}")


def insert(nb_path, idx, cell_type, text_path, out):
    if cell_type not in ("markdown", "code"):
        sys.exit("cell type must be 'markdown' or 'code'")
    nb = load(nb_path)
    idx = int(idx)
    with open(text_path, encoding="utf-8") as f:
        cell = {"cell_type": cell_type, "id": new_id(), "metadata": {}, "source": as_lines(f.read())}
    if cell_type == "code":
        cell["outputs"], cell["execution_count"] = [], None
    nb["cells"].insert(idx, cell)
    save(nb, out)
    print(f"Inserted {cell_type} cell at {idx}. Wrote {out}")


def split(nb_path, idx, offset, out):
    nb = load(nb_path)
    idx, offset = int(idx), int(offset)
    cell = cell_at(nb, idx)
    if cell["cell_type"] != "markdown":
        sys.exit("split is only supported for markdown cells")
    text = "".join(cell["source"])
    if not 0 < offset < len(text):
        sys.exit(f"offset must be between 1 and {len(text) - 1}")
    a, b = copy.deepcopy(cell), copy.deepcopy(cell)
    a["source"], b["source"] = as_lines(text[:offset].rstrip("\n") + "\n"), as_lines(text[offset:].lstrip("\n"))
    b["id"] = new_id()
    nb["cells"][idx:idx + 1] = [a, b]
    save(nb, out)
    print(f"Split cell {idx} into {idx} and {idx + 1}. Wrote {out}")


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    cmd = a[0]
    if cmd == "set-source" and len(a) == 5:
        check_paths(a[1], a[4]); set_source(*a[1:])
    elif cmd == "insert" and len(a) == 6:
        check_paths(a[1], a[5]); insert(*a[1:])
    elif cmd == "split" and len(a) == 5:
        check_paths(a[1], a[4]); split(*a[1:])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()

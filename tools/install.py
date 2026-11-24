"""
Install steps for each AI tool, from the one source guide/install.yaml.

Used by the Skills page (the "Install a skill" section), the skill pages, and the workshop handouts and slides,
so the steps are written once and can't drift apart.
"""
import html
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "guide" / "install.yaml"
ZIP_LABEL = {"standard": "the ZIP for Claude and ChatGPT", "flat": "the ZIP for Gemini and Copilot"}


def load():
    return yaml.safe_load(SRC.read_text(encoding="utf-8"))


def validate():
    errors = []
    try:
        d = load()
    except Exception as ex:  # noqa: BLE001
        return [f"[install] cannot read {SRC.name}: {ex}"]
    ids = set()
    for t in d.get("tools") or []:
        tag = f"[install] tool {t.get('id')}"
        for k in ("id", "name", "plans", "steps"):
            if not t.get(k):
                errors.append(f"{tag} missing '{k}'")
        if t.get("id") in ids:
            errors.append(f"{tag} listed twice")
        ids.add(t.get("id"))
        if t.get("zip") not in (None, "standard", "flat"):
            errors.append(f"{tag}: zip must be 'standard' or 'flat'")
    for need in ("claude", "chatgpt", "gemini", "copilot", "none"):
        if need not in ids:
            errors.append(f"[install] no steps for '{need}'")
    return errors


def tool(tid):
    return next(t for t in load()["tools"] if t["id"] == tid)


def as_workshop_tools():
    """The tools in the shape the workshop guides use: a name and a list of steps."""
    out = []
    for t in load()["tools"]:
        if t["id"] == "code":
            continue
        steps = [t["plans"].strip()] + list(t["steps"]) + ([t["note"].strip()] if t.get("note") else [])
        out.append({"name": t["name"], "steps": steps})
    return out


def section_html(inline, root=""):
    """The "Install a skill" section of the Skills page: a tool picker and one panel per tool.
    Without JavaScript every panel shows."""
    d = load()
    e = html.escape
    picks = "".join(f'<button type="button" data-tool="{e(t["id"])}" aria-pressed="false">{e(t["name"])}</button>'
                    for t in d["tools"])
    panels = []
    for t in d["tools"]:
        p = [f'<div class="inst-panel" data-tool-panel="{e(t["id"])}"><h3>{e(t["name"])}</h3>',
             f'<p class="inst-plans">{inline(t["plans"].strip(), root)}</p>']
        if t.get("zip"):
            p.append(f'<p class="inst-zip">Download {e(ZIP_LABEL[t["zip"]])} from the skill\'s page.</p>')
        p.append("<ol>" + "".join(f"<li>{inline(s, root)}</li>" for s in t["steps"]) + "</ol>")
        if t.get("note"):
            p.append(f'<p class="inst-note">{inline(t["note"].strip(), root)}</p>')
        if t.get("sources"):
            p.append('<p class="inst-src">From ' + ", ".join(f'<a href="{e(u)}">{e(n)}</a>' for n, u in t["sources"])
                     + f', checked {e(str(d["checked"]))}. Menus change often; if a step doesn\'t match, look for the word Skills.</p>')
        p.append("</div>")
        panels.append("".join(p))
    return (f'<p>{inline(d["download"].strip(), root)}</p>'
            f'<div class="seg inst-pick" role="group" aria-label="Your AI tool">{picks}</div>'
            + "".join(panels))

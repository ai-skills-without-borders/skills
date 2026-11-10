#!/usr/bin/env python3
"""
Validate the skills library and build its downloads and catalog site.

Usage:
    python tools/build.py --check     # validate only; exit 1 on errors
    python tools/build.py             # validate, then build dist/ and docs/

Builds:
    dist/zips/<skill>.zip       skill folder for upload (Claude, ChatGPT, Gemini, Copilot)
    dist/paste/<skill>.md       single-file paste-in version for GPTs, Gems, Projects
    dist/catalog.json           machine-readable catalog of all skill cards
    docs/downloads/, docs/paste/, docs/index.html   the GitHub Pages catalog site
    README.md                   the skills table between the CATALOG markers

Requires PyYAML.
"""
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"
DOCS = ROOT / "docs"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MATURITY = ["draft", "tested-at-origin", "tested-elsewhere", "reviewed"]
TOOL_STATES = {"untested", "works", "works-with-limits", "broken"}
CARD_REQUIRED = ["name", "title", "version", "summary", "tasks", "audience", "inputs", "outputs",
                 "runs_code", "maturity", "tested_in", "maintainers", "license"]
# Product-specific tokens that make a skill non-portable
FORBIDDEN = [r"ask_user_input_v\d", r"present_files", r"/mnt/user-data", r"/mnt/skills", r"\bAskUserQuestion\b"]
PASTE_INSTRUCTION_LIMIT = 8000  # custom GPT instructions are limited in length
SKIP_IN_ZIP = {"__pycache__", ".DS_Store"}


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def validate():
    errors, warnings, skills = [], [], []
    for d in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        tag = f"[{d.name}]"
        skill_md = d / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{tag} missing SKILL.md"); continue
        fm, body = read_frontmatter(skill_md)
        if fm is None:
            errors.append(f"{tag} SKILL.md has no YAML frontmatter"); continue
        name, desc = fm.get("name"), fm.get("description", "")
        if name != d.name:
            errors.append(f"{tag} frontmatter name '{name}' must equal folder name")
        if not name or not NAME_RE.match(str(name)) or len(str(name)) > 64:
            errors.append(f"{tag} name must be lowercase-with-hyphens, max 64 chars")
        if not desc:
            errors.append(f"{tag} description is missing")
        elif len(desc) > 1024:
            errors.append(f"{tag} description is {len(desc)} chars (max 1024)")
        lines = body.count("\n")
        if lines > 500:
            warnings.append(f"{tag} SKILL.md body is {lines} lines; consider moving detail to references/")

        # referenced files must exist
        all_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore")
                             for p in d.rglob("*.md"))
        for ref in sorted(set(re.findall(r"`((?:references|profiles|scripts)/[\w./-]+\.(?:md|py))`", body))):
            if not (d / ref).exists():
                errors.append(f"{tag} SKILL.md references missing file {ref}")
        for pat in FORBIDDEN:
            if re.search(pat, all_text):
                errors.append(f"{tag} contains product-specific token /{pat}/ — make it tool-agnostic")

        # card
        card_path = d / "card.yaml"
        if not card_path.exists():
            errors.append(f"{tag} missing card.yaml"); continue
        card = yaml.safe_load(card_path.read_text(encoding="utf-8")) or {}
        for k in CARD_REQUIRED:
            if k not in card:
                errors.append(f"{tag} card.yaml missing '{k}'")
        if card.get("name") != d.name:
            errors.append(f"{tag} card.yaml name must equal folder name")
        if card.get("maturity") not in MATURITY:
            errors.append(f"{tag} card.yaml maturity must be one of {MATURITY}")
        for tool, state in (card.get("tested_in") or {}).items():
            if state not in TOOL_STATES:
                errors.append(f"{tag} tested_in.{tool} must be one of {sorted(TOOL_STATES)}")
        has_scripts = (d / "scripts").exists() and any((d / "scripts").glob("*.py"))
        if has_scripts != bool(card.get("runs_code")):
            errors.append(f"{tag} card.yaml runs_code={card.get('runs_code')} but scripts/ {'exists' if has_scripts else 'is empty'}")
        if card.get("maturity") in ("tested-elsewhere", "reviewed") and not card.get("used_at"):
            errors.append(f"{tag} maturity '{card['maturity']}' needs evidence in used_at")
        if card.get("maturity") == "reviewed" and not card.get("reviewers"):
            errors.append(f"{tag} maturity 'reviewed' needs reviewers")
        if len(body) > PASTE_INSTRUCTION_LIMIT:
            warnings.append(f"{tag} instructions are {len(body)} chars; paste-in GPT users must upload them as a file")

        card["description"] = desc
        card["_dir"] = d
        skills.append(card)
    return skills, errors, warnings


def build_zip(card):
    d = card["_dir"]
    out = DIST / "zips" / f"{d.name}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(d.rglob("*")):
            if p.is_file() and not (set(p.parts) & SKIP_IN_ZIP):
                z.write(p, Path(d.name) / p.relative_to(d))
    return out


def build_paste(card, cfg):
    d = card["_dir"]
    _, body = read_frontmatter(d / "SKILL.md")
    parts = [
        f"# {card['title']} — paste-in version",
        "",
        f"From the {cfg['library_name']} library, v{card['version']} ({card['license']}). "
        f"Source: https://github.com/{cfg['repo']}/tree/main/skills/{d.name}",
        "",
        "How to use: paste the **Instructions** section into the instructions of a custom GPT, Gem or Project "
        "(or at the start of a chat). Add the **Reference files** as knowledge files, or paste them too if there is room. "
        "Where the instructions mention a file such as `references/x.md`, it is included below under that name.",
    ]
    if card.get("runs_code"):
        parts.append("\nThis skill has optional scripts that a paste-in version can't run. Do the same checks by reading.")
    parts += ["", "---", "", "## Instructions", "", f"Use this when: {card['description']}", "", body.strip(), ""]
    refs = [p for p in sorted(d.rglob("*.md")) if p.name != "SKILL.md" and p.parent != d]
    if refs:
        parts += ["---", "", "## Reference files", ""]
        for p in refs:
            rel = p.relative_to(d).as_posix()
            parts += [f"### File: `{rel}`", "", p.read_text(encoding="utf-8").strip(), ""]
    out = DIST / "paste" / f"{d.name}.md"
    out.write_text("\n".join(parts), encoding="utf-8")
    return out


def public_card(card):
    c = {k: v for k, v in card.items() if not k.startswith("_")}
    c["zip"] = f"downloads/{card['name']}.zip"
    c["paste"] = f"paste/{card['name']}.md"
    c["source_url"] = None
    return c


def update_readme(cards, cfg):
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    label = {"draft": "draft", "tested-at-origin": "tested at origin",
             "tested-elsewhere": "tested elsewhere", "reviewed": "reviewed"}
    rows = ["| Skill | What it does | Runs code | Maturity |", "|---|---|---|---|"]
    for c in sorted(cards, key=lambda c: (not c.get("starter"), c["name"])):
        rows.append(f"| [{c['name']}](skills/{c['name']}) | {c['summary']} | "
                    f"{'Optional' if c['runs_code'] else 'No'} | {label[c['maturity']]} |")
    table = "\n".join(rows)
    new = re.sub(r"<!-- CATALOG:START -->.*?<!-- CATALOG:END -->",
                 f"<!-- CATALOG:START -->\n{table}\n<!-- CATALOG:END -->", text, flags=re.S)
    readme.write_text(new, encoding="utf-8")


def build_site(cards, cfg):
    for sub in ("downloads", "paste"):
        target = DOCS / sub
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True)
    for c in cards:
        shutil.copy(DIST / "zips" / f"{c['name']}.zip", DOCS / "downloads")
        shutil.copy(DIST / "paste" / f"{c['name']}.md", DOCS / "paste")
    template = (ROOT / "tools" / "site_template.html").read_text(encoding="utf-8")
    data = json.dumps([public_card(c) for c in cards], ensure_ascii=False).replace("</", "<\\/")
    conf = json.dumps({k: cfg[k] for k in ("library_name", "tagline", "repo", "plugin_name", "version", "contact")},
                      ensure_ascii=False).replace("</", "<\\/")
    html = template.replace("/*CATALOG_JSON*/[]", data).replace("/*CONFIG_JSON*/{}", conf)
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")


def main():
    check_only = "--check" in sys.argv
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    cards, errors, warnings = validate()
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"ERROR:   {e}")
    print(f"{len(cards)} skills, {len(errors)} errors, {len(warnings)} warnings")
    if errors:
        sys.exit(1)
    if check_only:
        return
    for sub in ("zips", "paste"):
        (DIST / sub).mkdir(parents=True, exist_ok=True)
    for c in cards:
        build_zip(c)
        build_paste(c, cfg)
    (DIST / "catalog.json").write_text(json.dumps([public_card(c) for c in cards], indent=2, ensure_ascii=False),
                                      encoding="utf-8")
    update_readme(cards, cfg)
    build_site(cards, cfg)
    print("built dist/ and docs/")


if __name__ == "__main__":
    main()

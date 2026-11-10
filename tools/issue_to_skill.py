"""Turn a "New skill" issue (GitHub issue form) into a skill folder.

    python tools/issue_to_skill.py ISSUE_BODY.md [--author LOGIN] [--issue N] [--date YYYY-MM-DD]

Writes skills/<name>/SKILL.md, card.yaml and references/pedagogical-basis.md,
and records the contribution in community/contributors.yaml. Prints the skill name.

The instructions may be pasted as raw SKILL.md (with or without front matter) or
as text copied from a rendered page; in the second case headings, lists and
tables are rebuilt from the layout of the text.
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
REGISTRY = ROOT / "community" / "contributors.yaml"

COUNTRY_CODES = {"united states": "US", "usa": "US", "us": "US", "united states of america": "US", "israel": "IL",
                 "united kingdom": "GB", "uk": "GB", "canada": "CA", "germany": "DE", "france": "FR", "netherlands": "NL",
                 "australia": "AU", "india": "IN", "china": "CN", "japan": "JP", "brazil": "BR", "south africa": "ZA",
                 "switzerland": "CH", "sweden": "SE", "denmark": "DK", "spain": "ES", "italy": "IT", "ireland": "IE",
                 "singapore": "SG", "south korea": "KR", "mexico": "MX", "oman": "OM", "saudi arabia": "SA",
                 "united arab emirates": "AE", "new zealand": "NZ", "belgium": "BE", "norway": "NO", "finland": "FI"}

# Section names that are top-level in a skill; other short title lines become sub-headings.
TOP = {"before you start", "steps", "rules that always apply", "what this skill does not do", "reference sections",
       "why these rules", "limits", "references", "updating the map", "hand-offs", "output", "outputs", "inputs",
       "examples", "workflow"}


# ---------------------------------------------------------------- issue form

def parse_form(body):
    fields, key, fence = {}, None, False
    for line in body.replace("\r\n", "\n").splitlines():
        if line.startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"^### (.+?)\s*$", line)
        if m:
            key = m.group(1).strip()
            fields[key] = []
        elif key:
            fields[key].append(line)
    out = {k: "\n".join(v).strip() for k, v in fields.items()}
    return {k: ("" if v in ("_No response_", "None") else v) for k, v in out.items()}


def field(fields, prefix):
    for k, v in fields.items():
        if k.lower().startswith(prefix.lower()):
            return v
    return ""


def bullets(text):
    items = [re.sub(r"^\s*[-*•]\s*", "", ln).strip() for ln in text.splitlines()]
    return [i for i in items if i]


def unfence(text):
    m = re.search(r"```[a-zA-Z]*\n(.*)\n```", text, re.S)
    if m:
        return m.group(1).strip("\n")
    return re.sub(r"^```[a-zA-Z]*\n", "", text).strip("\n")


# ---------------------------------------------------------------- rebuild markdown from pasted text

def _is_title(line):
    s = line.strip()
    if not s or len(s) > 70 or "\t" in s or "[" in s:
        return False
    if s.endswith((".", ",", ":", ";", "?", "!", ")")) and not s.endswith("?)"):
        return False
    if not s[0].isupper() and not s[0].isdigit():
        return False
    if re.match(r"^(Subject|Dear|Thank|Best|Hi|Hello|Regards)\b", s) or ": " in s:
        return False
    return True


def _table(rows):
    cells = [r.split("\t") for r in rows]
    n = max(len(c) for c in cells)
    cells = [c + [""] * (n - len(c)) for c in cells]
    out = ["| " + " | ".join(x.strip() for x in cells[0]) + " |", "|" + "---|" * n]
    out += ["| " + " | ".join(x.strip() for x in c) + " |" for c in cells[1:]]
    return out


def rebuild(text):
    """Pasted rendered text -> Markdown. Blank-line-separated blocks: a block of several
    lines is a list; tab-separated lines are a table; short title lines are headings."""
    if re.search(r"^#{1,3} \S", text, re.M):
        return text  # already Markdown
    blocks, cur = [], []
    for ln in text.splitlines():
        if ln.strip():
            cur.append(ln.rstrip(" \r"))
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)

    out, section, seen_title, in_reference = [], "", False, False
    for block in blocks:
        i = 0
        while i < len(block):
            line = block[i]
            rest = block[i + 1:]
            if "\t" in line:
                j = i
                while j < len(block) and "\t" in block[j]:
                    j += 1
                out += _table(block[i:j]) + [""]
                i = j
                continue
            if _is_title(line):
                low = line.strip().lower()
                if not seen_title:
                    out += [f"# {line.strip()}", ""]
                    seen_title = True
                else:
                    if low == "reference sections":
                        in_reference = True
                    level = "###" if in_reference else "##"
                    if low in ("why these rules", "limits", "references"):
                        level = "##"
                    out += [f"{level} {line.strip()}", ""]
                section = line.strip().lower()
                i += 1
                continue
            # list: remaining consecutive lines of a block (two or more), unless the block is one paragraph
            seq = []
            while i < len(block) and "\t" not in block[i] and not (_is_title(block[i]) and seq):
                seq.append(block[i])
                i += 1
            if len(seq) == 1:
                out += [seq[0], ""]
            else:
                numbered = section in ("steps",)
                out += [(f"{k}. " if numbered else "- ") + s for k, s in enumerate(seq, 1)] + [""]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"


# ---------------------------------------------------------------- build the skill

def split_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if m:
        return yaml.safe_load(m.group(1)) or {}, m.group(2).lstrip()
    lines = text.split("\n", 1)
    first = lines[0].strip()
    # a leading description paragraph (copied without its front matter)
    if len(first) > 120 and not first.startswith("#"):
        return {"description": first}, (lines[1] if len(lines) > 1 else "").lstrip()
    return {}, text


def first_sentence(text, limit=170):
    s = re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0]
    return s if len(s) <= limit else s[: limit - 1].rsplit(" ", 1)[0] + "…"


def short_item(text, limit=70):
    head, sep, tail = text.partition(":")
    if sep and re.match(r"^(For|When|If|In|During)\b", head.strip()):
        text = tail.strip()  # "For the program layer: the program's policies" -> the useful part
        text = text[:1].upper() + text[1:]
    s = re.split(r"[:;]| — | \(|, with |, which ", text, maxsplit=1)[0].strip().rstrip(".")
    return s if len(s) <= limit else s[: limit - 1].rsplit(" ", 1)[0] + "…"


def tasks_from(description):
    quoted = re.findall(r'"([^"]{6,60})"', description)
    out = []
    for q in quoted[:6]:
        q = q.strip().rstrip(".")
        out.append(q[0].upper() + q[1:])
    return out


def from_zip(zpath):
    """Return (SKILL.md text, {relative path: bytes} of the other files) from an uploaded ZIP."""
    import zipfile
    with zipfile.ZipFile(zpath) as z:
        names = [n for n in z.namelist() if not n.endswith("/") and "__MACOSX" not in n]
        skill = min((n for n in names if n.split("/")[-1] == "SKILL.md"), key=len, default=None)
        if not skill:
            raise SystemExit("The ZIP has no SKILL.md.")
        base = skill[: -len("SKILL.md")]
        others = {n[len(base):]: z.read(n) for n in names if n.startswith(base) and n != skill
                  and not n[len(base):].startswith((".", "card.yaml")) and ".." not in n}
        return z.read(skill).decode("utf-8"), others


def build(body, author=None, issue=None, date=None, overrides=None, zpath=None, overwrite=False):
    f = parse_form(body)
    name = re.sub(r"[^a-z0-9-]+", "-", field(f, "Proposed name").strip().lower()).strip("-")
    if not name:
        raise SystemExit("The issue has no proposed name.")
    person = field(f, "Your name").strip()
    institution = field(f, "Institution").strip()
    country = field(f, "Country").strip()
    credit = "[x]" in field(f, "Credit").lower()
    purpose = field(f, "Purpose")
    raw = unfence(field(f, "Instructions"))
    extra = {}
    if zpath:
        raw, extra = from_zip(zpath)
    fm, text = split_frontmatter(raw)
    text = rebuild(text)

    # move "Why these rules" (to the end) into references/pedagogical-basis.md
    basis = ""
    m = re.search(r"^## Why these rules\n(.*)$", text, re.S | re.M)
    if m:
        basis = "# Pedagogical basis\n\n" + m.group(1).strip() + "\n"
        text = text[: m.start()].rstrip() + "\n"
        text = re.sub(r'in the "Why these rules" section at the end', "in `references/pedagogical-basis.md`", text)

    title = re.search(r"^# (.+)$", text, re.M)
    title = title.group(1).strip() if title else name.replace("-", " ").title()
    description = (fm.get("description") or purpose).strip().replace("\n", " ")
    if len(description) > 1024:
        description = description[:1020].rsplit(" ", 1)[0] + "…"

    tools_used = field(f, "Tools it has been used in").lower()
    tested = {t: ("works" if t in tools_used and "none" not in tools_used else "untested") for t in ("claude", "chatgpt", "gemini", "copilot")}
    who = f"{person} ({institution})" if (person and credit) else f"Contributor ({institution})"
    ticked = field(f, "Who uses this skill").lower()
    users = [u for u, key in (("educators", "[x] educators"), ("learners", "[x] learners"), ("program-staff", "[x] program staff")) if key in ticked] or ["educators"]
    tasks = bullets(field(f, "Tasks")) or tasks_from(description) or [first_sentence(purpose, 90).rstrip(".")]
    card = {
        "name": name, "title": title, "version": "0.1.0", "summary": first_sentence(purpose),
        "tasks": tasks[:6], "users": users, "audience": [{"educators": "Educators", "learners": "Learners", "program-staff": "Program staff"}[u] for u in users],
        "inputs": [short_item(x) for x in bullets(field(f, "Inputs"))][:6],
        "outputs": [short_item(x) for x in bullets(field(f, "Expected output"))][:8],
        "runs_code": False, "maturity": "draft", "tested_in": tested, "last_tested": None, "used_at": [],
        "frameworks": [], "origin_institution": institution, "derived_from": "New skill",
        "maintainers": [who], "reviewers": [], "license": "CC-BY-4.0", "starter": False,
    }
    if overrides:
        card.update(overrides)

    d = SKILLS / name
    if d.exists() and not overwrite:
        raise SystemExit(f"A skill named '{name}' already exists. Choose another name, or suggest a change to the existing skill.")
    (d / "references").mkdir(parents=True, exist_ok=True)
    front = yaml.safe_dump({"name": name, "description": description}, sort_keys=False, allow_unicode=True, width=10**6)
    (d / "SKILL.md").write_text(f"---\n{front}---\n\n{text}", encoding="utf-8")
    (d / "card.yaml").write_text("# Skill card — see GOVERNANCE.md for field meanings and maturity levels\n"
                                 + yaml.safe_dump(card, sort_keys=False, allow_unicode=True, width=200), encoding="utf-8")
    for rel, data in extra.items():
        target = (d / rel).resolve()
        if d.resolve() in target.parents:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    if basis and not (d / "references" / "pedagogical-basis.md").exists():
        (d / "references" / "pedagogical-basis.md").write_text(basis, encoding="utf-8")

    record(name, person if credit else None, institution, country, issue, date, author)
    return name


def record(skill, person, institution, country, issue, date, github=None):
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    insts = data["institutions"]
    iid = next((k for k, v in insts.items() if v["name"].lower() == institution.lower()
                or institution.lower() in v["name"].lower() or v["name"].lower() in institution.lower()), None)
    text = REGISTRY.read_text(encoding="utf-8")
    if iid is None:
        iid = re.sub(r"[^a-z0-9]+", "-", institution.lower()).strip("-")[:30] or "institution"
        code = COUNTRY_CODES.get(country.strip().lower(), country.strip().upper()[:2])
        entry = (f"  {iid}:\n    name: {yaml.safe_dump(institution, width=10**6).strip()}\n    country: {code}\n"
                 "    lat: 0\n    lon: 0  # TODO: approximate location for the map\n")
        text = text.replace("\ncontributions:\n", "\n" + entry + "\ncontributions:\n", 1)
    if f"skill: {skill}\n" in text:
        REGISTRY.write_text(text, encoding="utf-8")
        return
    when = date or dt.date.today().isoformat()
    lines = [f"  - date: {when}", "    type: skill", f"    institution: {iid}", f"    skill: {skill}"]
    if person:
        lines.append(f'    person: "{person}"')
    if github:
        lines.append(f"    github: {github}")
    if issue:
        lines.append(f"    link: https://github.com/ai-skills-without-borders/skills/issues/{issue}")
    REGISTRY.write_text(text.rstrip("\n") + "\n" + "\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("body")
    ap.add_argument("--author")
    ap.add_argument("--issue")
    ap.add_argument("--date")
    ap.add_argument("--zip")
    ap.add_argument("--overwrite", action="store_true", help="replace an existing skill folder (maintainers only)")
    a = ap.parse_args()
    print(build(Path(a.body).read_text(encoding="utf-8"), a.author, a.issue, a.date, zpath=a.zip, overwrite=a.overwrite))

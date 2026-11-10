"""
Generate the multi-page website in docs/ from the skill cards and guides.

Called by tools/build.py. Pages:
    index.html        home, with paths by audience
    start.html        what a skill is, for beginners
    skills.html       searchable catalog
    skills/<n>.html   one page per shared skill (with its variants)
    pedagogy.html     principles, evidence labels, full foundations
    quality.html      maturity levels, status of every skill, approval rules
    contribute.html   report, suggest, edit, adapt, share
"""
import html
import json
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "tools" / "site"
DOCS = ROOT / "docs"

NAV = [("start.html", "Start here"), ("skills.html", "Skills"), ("pedagogy.html", "Pedagogy"),
       ("quality.html", "Quality"), ("contribute.html", "Contribute")]
LADDER = ["draft", "tested-at-origin", "tested-elsewhere", "reviewed"]
LABEL = {"draft": "Draft", "tested-at-origin": "Tested at origin",
         "tested-elsewhere": "Tested elsewhere", "reviewed": "Reviewed"}
TOOLNAME = {"claude": "Claude", "chatgpt": "ChatGPT", "gemini": "Gemini", "copilot": "Copilot"}
STATE = {"untested": "not yet tested", "works": "works", "works-with-limits": "works, with limits", "broken": "broken"}

PED = [
    ("Constructive alignment", "Objectives, activities and assessment are designed together, so learners practise and are tested on what the objectives say.", "standard", "Objectives, Syllabus, Exam items, Lesson check", "Biggs, 1996"),
    ("Observable, levelled objectives", "One observable verb at a defined cognitive level; for skills, a condition and a criterion.", "standard", "Objectives, Syllabus", "Anderson & Krathwohl, 2001; Mager, 1962"),
    ("Competencies and entrustment", "Count a competency only where learners perform it and someone observes it. Frameworks need faculty review before use.", "standard", "Syllabus, Objectives", "ten Cate, 2005; AAMC Foundational Competencies, 2024; GREAT MD-PhD toolkit, 2026"),
    ("Problem-based learning", "Problems activate prior knowledge and store it in the context where it will be used. Curriculum-level outcomes are mixed, so structure matters.", "research", "Session", "Schmidt, 1983; Norman & Schmidt, 1992; Colliver, 2000"),
    ("Problem solving before instruction", "Trying first, then consolidating, improves understanding and transfer, when the struggle is designed and followed by explicit instruction.", "research", "Session", "Kapur, 2008; Sinha & Kapur, 2021 (meta-analysis of 53 studies)"),
    ("Managing cognitive load", "Working memory is limited, and novices need guidance: one inference per prompt, terms defined at first use, worked code before independent code.", "research", "Session, Reading, Lesson check, Objectives", "Sweller, 1988; Kirschner, Sweller & Clark, 2006"),
    ("Retrieval practice with feedback", "Recalling strengthens memory more than rereading, including in medical education, and feedback is essential.", "research", "Reading, Session, Exam items", "Roediger & Karpicke, 2006; Larsen, Butler & Roediger, 2008"),
    ("Item-writing quality", "Validated guidelines define well-formed items. Flawed items are common and disadvantage some students.", "standard", "Exam items", "Haladyna, Downing & Rodriguez, 2002; Downing, 2005; NBME Item-Writing Guide, 2020"),
    ("Assessment validity and purpose", "Results support a decision only with validity evidence for that use. Formative and summative assessment are built differently.", "standard", "Exam items, Syllabus", "Downing, 2003; van der Vleuten, 1996"),
    ("Responsible AI in education", "Disclose AI use, protect privacy, keep the educator in charge, and never invent sources.", "standard", "Every skill", "AAMC Principles for the Responsible Use of AI in Medical Education, 2025"),
]


def e(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def md(text):
    out = markdown.markdown(text, extensions=["tables", "fenced_code"])
    # links into the repository should point at GitHub, not the website
    return out


def gh_links(fragment, gh):
    """Rewrite relative Markdown links (e.g. ../CONTRIBUTING.md, install.md) to GitHub URLs."""
    def fix(m):
        href = m.group(1)
        if re.match(r"^(https?:|#|mailto:)", href):
            return m.group(0)
        path = href
        while path.startswith("../"):
            path = path[3:]
        if not path.startswith(("guide/", "community/", "skills/", "variants/", "frameworks/")) and "/" not in path and path not in ("CONTRIBUTING.md", "GOVERNANCE.md", "README.md"):
            path = "guide/" + path
        return f'href="{gh}/blob/main/{path}"'
    return re.sub(r'href="([^"]+)"', fix, fragment)


def layout(cfg, title, description, content, active, root="", scripts="", catalog=None):
    gh = f"https://github.com/{cfg['repo']}"
    nav = "\n".join(
        f'      <a href="{root}{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>'
        for href, label in NAV) + f'\n      <a href="{gh}">GitHub</a>'
    founders = "".join(
        f"<div><b>{e(f['name'])}</b>{e(f['role'])}<br>{e(f['institution'])}</div>" for f in cfg.get("founders", []))
    conf = {k: cfg[k] for k in ("library_name", "repo", "plugin_name", "version")}
    page = (SITE / "base.html").read_text(encoding="utf-8")
    extra = ""
    if catalog is not None:
        extra = "<script>window.ASB_CATALOG = " + json.dumps(catalog, ensure_ascii=False).replace("</", "<\\/") + ";</script>\n"
    for k, v in {"TITLE": e(title), "DESCRIPTION": e(description), "ROOT": root, "LIBNAME": e(cfg["library_name"]),
                 "NAV": nav, "FOUNDERS": founders, "VERSION": e(cfg["version"]), "GH": gh,
                 "CONFIG_JSON": json.dumps(conf).replace("</", "<\\/"), "SCRIPTS": extra + scripts,
                 "CONTENT": content.replace("{{GH}}", gh)}.items():
        page = page.replace("{{" + k + "}}", v)
    return page


def read(name):
    return (SITE / "pages" / name).read_text(encoding="utf-8")


def skill_page(c, cfg, variants):
    gh = f"https://github.com/{cfg['repo']}"
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in (xs or []))
    basis_path = c["_dir"] / "references" / "pedagogical-basis.md"
    ped = ""
    if basis_path.exists():
        text = basis_path.read_text(encoding="utf-8")
        table = text[text.index("|"):] if "|" in text else text
        table = table.split("\nFull list")[0]
        ped = md(table)
        ped = (ped.replace("<td>Research</td>", '<td><span class="basis research">Research</span></td>')
                  .replace("<td>Standard</td>", '<td><span class="basis standard">Standard</span></td>')
                  .replace("<td>Practice</td>", '<td><span class="basis practice">Practice</span></td>'))
    tested = "".join(
        f'<span class="{"works" if s == "works" else ""}">{e(TOOLNAME.get(t, t))}: {e(STATE.get(s, s))}</span>'
        for t, s in (c.get("tested_in") or {}).items())
    used = c.get("used_at") or []
    used_at = ("Used at: " + e(", ".join(map(str, used)))) if used else "No usage reports yet. Be the first to send one."
    revs = c.get("reviewers") or []
    reviewers = ("Reviewed by: " + e(", ".join(map(str, revs)))) if revs else "Not yet reviewed by another institution."
    if variants:
        vhtml = "<ul>" + "".join(
            f'<li><b>{e(v["title"])}</b> — {e(v.get("institution", ""))}. {e(v.get("changes", ""))} '
            f'<a href="{gh}/tree/main/variants/{e(v["_dir"].parent.name)}/{e(v["name"])}">Files</a> · '
            f'<a href="../{e(v["zip"])}" download>ZIP</a></li>' for v in variants) + "</ul>"
    else:
        vhtml = (f'<p class="empty-variants">No institutional variants yet. Most adaptations need only configuration; '
                 f'if yours needs more, <a href="../contribute.html#adapt">see how to adapt a skill</a>.</p>')
    fw = c.get("frameworks") or []
    frameworks = ("<p>Works with: " + e(", ".join(fw)) + ".</p>") if fw else ""
    origin = f'{e(c.get("derived_from", ""))}. Origin: {e(c.get("origin_institution", ""))}.'
    content = read("skill.html")
    for k, v in {"TITLE": e(c["title"]), "SUMMARY": e(c["summary"]), "MATURITY": LABEL[c["maturity"]],
                 "VERSION": e(c["version"]), "RUNS_CODE": "Optional scripts" if c.get("runs_code") else "No",
                 "MAINTAINERS": e(", ".join(c.get("maintainers") or [])), "DESCRIPTION": e(c["description"]),
                 "TASKS": li(c.get("tasks")), "INPUTS": li(c.get("inputs")), "OUTPUTS": li(c.get("outputs")),
                 "PEDAGOGY": ped, "VARIANTS": vhtml, "ORIGIN": origin, "FRAMEWORKS": frameworks,
                 "ZIP": e(c["zip"]), "PASTE": e(c["paste"]), "TESTED": tested, "USED_AT": used_at,
                 "REVIEWERS": reviewers, "NAME": e(c["name"])}.items():
        content = content.replace("{{" + k + "}}", v)
    return layout(cfg, f"{c['title']} — {cfg['library_name']}", c["summary"], content, "skills.html", root="../")


def status_table(cards):
    rows = []
    for c in sorted(cards, key=lambda c: (-LADDER.index(c["maturity"]), c["title"])):
        tested = ", ".join(f"{TOOLNAME.get(t, t)}: {STATE.get(s, s)}" for t, s in (c.get("tested_in") or {}).items())
        rows.append(f'<tr><td><a href="skills/{e(c["name"])}.html">{e(c["title"])}</a></td><td>{LABEL[c["maturity"]]}</td>'
                    f'<td class="hide-m">{e(tested)}</td><td>{len(c.get("used_at") or [])}</td><td>{len(c.get("reviewers") or [])}</td></tr>')
    return ('<table class="status"><thead><tr><th>Skill</th><th>Maturity</th><th class="hide-m">Tested in</th>'
            '<th>Usage reports</th><th>Reviews</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>")


def ped_rows():
    label = {"research": "Research", "standard": "Standard", "practice": "Practice"}
    return "".join(
        f'<div class="ped-row"><div><h3>{e(t)}</h3><p>{e(d)}</p><p class="src">{e(src)}</p></div>'
        f'<div><span class="basis {b}">{label[b]}</span></div><div class="where"><b>Applied in</b>{e(w)}</div></div>'
        for t, d, b, w, src in PED)


def build_site(cards, variants, cfg, public_card):
    gh = f"https://github.com/{cfg['repo']}"
    # clean generated output, keep nothing stale
    for p in ("downloads", "paste", "skills"):
        if (DOCS / p).exists():
            shutil.rmtree(DOCS / p)
    for p in DOCS.glob("*.html"):
        p.unlink()
    for p in ("downloads", "paste", "skills"):
        (DOCS / p).mkdir(parents=True, exist_ok=True)
    for c in cards + variants:
        shutil.copy(ROOT / "dist" / "zips" / f"{c['name']}.zip", DOCS / "downloads")
        shutil.copy(ROOT / "dist" / "paste" / f"{c['name']}.md", DOCS / "paste")
    for f in ("logo.svg", "logo.png", "favicon.svg", "favicon.png"):
        shutil.copy(ROOT / "assets" / f, DOCS / f)
    shutil.copy(SITE / "style.css", DOCS / "style.css")
    shutil.copy(SITE / "site.js", DOCS / "site.js")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    by_parent = {}
    for v in variants:
        by_parent.setdefault(v["variant_of"], []).append(v)
    catalog = []
    for c in cards:
        pc = public_card(c)
        pc["variants"] = [v["name"] for v in by_parent.get(c["name"], [])]
        catalog.append(pc)

    pages = {
        "index.html": (f"{cfg['library_name']} — shared AI skills for medical educators",
                       "Shared AI skills for medical and biomedical-research educators.",
                       read("home.html"), "", read("home.js")),
        "start.html": ("New to skills? — " + cfg["library_name"], "What an AI skill is and how to use one.",
                       read("start.html"), "start.html", ""),
        "skills.html": ("The skills — " + cfg["library_name"], "Search and download the skills.",
                        read("skills.html"), "skills.html", read("skills.js")),
        "contribute.html": ("Contribute — " + cfg["library_name"], "Adapt, improve and share skills.",
                            read("contribute.html"), "contribute.html", ""),
        "quality.html": ("Quality and review — " + cfg["library_name"], "How skills are tested and approved.",
                         read("quality.html").replace("{{STATUS_TABLE}}", status_table(cards)), "quality.html", ""),
        "pedagogy.html": ("Pedagogy — " + cfg["library_name"], "The pedagogical foundations of the skills.",
                          read("pedagogy.html").replace("{{PED_ROWS}}", ped_rows()).replace(
                              "{{PEDAGOGY_MD}}", gh_links(md((ROOT / "guide" / "pedagogy.md").read_text(encoding="utf-8")), gh)),
                          "pedagogy.html", ""),
    }
    for fname, (title, desc, content, active, scripts) in pages.items():
        (DOCS / fname).write_text(layout(cfg, title, desc, content, active, scripts=scripts, catalog=catalog), encoding="utf-8")
    for c in cards:
        c2 = dict(c)
        c2.update(public_card(c))
        for v in by_parent.get(c["name"], []):
            v.update({k: val for k, val in public_card(v).items() if k in ("zip", "paste")})
        (DOCS / "skills" / f"{c['name']}.html").write_text(
            skill_page(c2, cfg, by_parent.get(c["name"], [])), encoding="utf-8")

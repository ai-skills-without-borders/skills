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
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

import markdown

import community
import principles
import visuals
import workshops
import workshop_pptx

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "tools" / "site"
DOCS = ROOT / "docs"

NAV = [("start.html", "Start here"), ("skills.html", "Skills"), ("pedagogy.html", "Pedagogy"),
       ("quality.html", "Quality"), ("contribute.html", "Contribute"), ("workshops.html", "Workshops"), ("community.html", "Community"), ("about.html", "About")]
LADDER = ["draft", "tested-at-origin", "tested-elsewhere", "reviewed"]
LABEL = {"draft": "Draft", "tested-at-origin": "Tested at origin",
         "tested-elsewhere": "Tested elsewhere", "reviewed": "Reviewed"}
TOOLNAME = {"claude": "Claude", "chatgpt": "ChatGPT", "gemini": "Gemini", "copilot": "Copilot"}
STATE = {"untested": "not yet tested", "works": "works", "works-with-limits": "works, with limits", "broken": "broken"}

EFFORT = [
    ("Send a usage report", "five minutes, after real teaching", "#quick"),
    ("Suggest a change or review a skill", "one real task", "#quick"),
    ("Edit a skill directly", "in your browser, no Git", "#edit"),
    ("Create an institutional variant", "the skill, fitted to your institution", "#adapt"),
    ("Share a new skill", "your own know-how, for everyone", "#new"),
]
APPROVAL = [
    ("improve", "Any change to a shared skill, or a new skill", "person", "One maintainer", "Checks pass. New skills start as Draft"),
    ("school", "Institutional variant", "school", "One maintainer from that institution", "Checks pass"),
    ("check", "Maturity upgrade", "person", "One library maintainer", "Linked usage reports; for Reviewed, one completed review"),
]


USER_LABELS = {"educators": "Educators", "learners": "Learners", "program-staff": "Program staff"}


def users_label(users):
    names = [USER_LABELS.get(u, u) for u in (users or [])]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1].lower() if names else ""


def pedagogy_body():
    """guide/pedagogy.md from its first section on: the page has its own title and introduction."""
    text = (ROOT / "guide" / "pedagogy.md").read_text(encoding="utf-8")
    return text[text.index("\n## ") + 1:]


def ped_entries(skill_names):
    """Principles from guide/principles.yaml, ready for the website."""
    _, ps = principles.load()
    out = []
    for p in ps:
        med = [r["short"] for r in p["refs"] if principles.is_medical(r)]
        gen = [r["short"] for r in p["refs"] if not principles.is_medical(r)]
        out.append({**p, "used": principles.skills_of(p, skill_names), "med": med, "gen": gen,
                    "med_ok": principles.has_medical_evidence(p),
                    "library": "library" in p["applies"]})
    return out


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


def layout(cfg, title, description, content, active, root="", scripts="", catalog=None, path=""):
    gh = f"https://github.com/{cfg['repo']}"
    nav = "\n".join(
        f'      <a href="{root}{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>'
        for href, label in NAV) + f'\n      <a href="{gh}">GitHub</a>'
    conf = {k: cfg[k] for k in ("library_name", "repo", "plugin_name", "version")}
    page = (SITE / "base.html").read_text(encoding="utf-8")
    # cache-busting: a new version of the CSS/JS gets a new URL, so phones never mix new pages with old styles
    ver = hashlib.sha1(((SITE / "style.css").read_bytes() + (SITE / "site.js").read_bytes())).hexdigest()[:10]
    page = page.replace('style.css"', f'style.css?v={ver}"').replace('site.js"', f'site.js?v={ver}"')
    extra = ""
    if catalog is not None:
        extra = "<script>window.ASB_CATALOG = " + json.dumps(catalog, ensure_ascii=False).replace("</", "<\\/") + ";</script>\n"
    for k, v in {"TITLE": e(title), "DESCRIPTION": e(description), "ROOT": root, "LIBNAME": e(cfg["library_name"]),
                 "NAV": nav, "VERSION": e(cfg["version"]), "GH": gh,
                 "URL": cfg["site_url"] + (path if path != "index.html" else ""), "SITE": cfg["site_url"],
                 "CONFIG_JSON": json.dumps(conf).replace("</", "<\\/"), "SCRIPTS": extra + scripts,
                 "CONTENT": content.replace("{{GH}}", gh)}.items():
        page = page.replace("{{" + k + "}}", v)
    return page


def static_list(cards):
    """The catalog as plain links, for visitors whose browser doesn't run the script; the script replaces it."""
    items = "".join(f'<li><a href="skills/{e(c["name"])}.html">{e(c["title"])}</a>: {e(c["summary"])}</li>'
                    for c in sorted(cards, key=lambda c: c["title"]))
    return f'<ul class="static-list">{items}</ul>'


def sitemap(cfg, cards, wss):
    pages = ["", "start.html", "skills.html", "workshops.html", "contribute.html", "community.html", "quality.html",
             "pedagogy.html", "about.html"]
    pages += [f"workshops/{w['id']}.html" for w in wss] + [f"skills/{c['name']}.html" for c in cards]
    urls = "".join(f"<url><loc>{e(cfg['site_url'] + p)}</loc></url>\n" for p in pages)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'


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
                 "MAINTAINERS": e(", ".join(c.get("maintainers") or [])),
                 "USERS": e(users_label(c.get("users"))), "DESCRIPTION": e(c["description"]),
                 "TASKS": li(c.get("tasks")), "INPUTS": li(c.get("inputs")), "OUTPUTS": li(c.get("outputs")),
                 "PEDAGOGY": ped, "VARIANTS": vhtml, "ORIGIN": origin, "FRAMEWORKS": frameworks,
                 "ZIP": e(c["zip"]), "PASTE": e(c["paste"]), "TESTED": tested, "USED_AT": used_at,
                 "REVIEWERS": reviewers, "NAME": e(c["name"]), "ICON": visuals.icon(c["name"], 36)}.items():
        content = content.replace("{{" + k + "}}", v)
    return layout(cfg, f"{c['title']} — {cfg['library_name']}", c["summary"], content, "skills.html", root="../", path=f"skills/{c['name']}.html")


def status_table(cards):
    rows = []
    for c in sorted(cards, key=lambda c: (-LADDER.index(c["maturity"]), c["title"])):
        sym = {"works": "✓", "works-with-limits": "◐", "broken": "✕", "untested": "○"}
        tested = " ".join(f'<span class="tchip {s}" title="{e(STATE.get(s, s))}">{sym.get(s, "○")} {e(TOOLNAME.get(t, t))}</span>'
                          for t, s in (c.get("tested_in") or {}).items())
        rows.append(f'<tr><td><a href="skills/{e(c["name"])}.html">{e(c["title"])}</a></td><td><span class="mini-ladder">{"".join('<i class="on"></i>' if i <= LADDER.index(c["maturity"]) else "<i></i>" for i in range(4))}</span>{LABEL[c["maturity"]]}</td>'
                    f'<td class="hide-m">{tested}</td><td>{len(c.get("used_at") or [])}</td><td>{len(c.get("reviewers") or [])}</td></tr>')
    legend = '<p class="sub" style="margin-top:10px">✓ works · ◐ works with limits · ✕ broken · ○ not yet tested</p>'
    return ('<table class="status"><thead><tr><th>Skill</th><th>Maturity</th><th class="hide-m">Tested in</th>'
            '<th>Usage reports</th><th>Reviews</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>" + legend)


def fill_steps(page):
    page = page.replace("{{ANATOMY}}", visuals.anatomy_svg() + visuals.anatomy_svg(stacked=True)).replace("{{EQUATION}}", visuals.equation_html())
    for k in ("ASK", "MATCH", "FRAME", "KNOW", "OK"):
        page = page.replace("{{IC_" + k + "}}", visuals.step_icon(k))
    return page


def ped_rows(entries):
    label = {"research": "Research", "standard": "Standard", "practice": "Practice"}
    short = dict(visuals.SHORT)
    out = []
    for layer, (title, intro) in principles.LAYERS.items():
        out.append(f'<h3 class="layer">{e(title)}</h3><p class="layer-intro">{e(intro)}</p><div class="ped">')
        for p in [x for x in entries if x["layer"] == layer]:
            where = ", ".join(short[n] for n in p["used"]) if p["used"] else ""
            if len(p["used"]) == len(short):
                where = "Every skill"
            if p["library"]:
                where = (where + "; the library as a whole" if where else "The library as a whole")
            where = where or '<span class="none">No skill yet</span>'
            srcs = f'<p class="src"><b>Origin and general evidence:</b> {e("; ".join(p["gen"]))}</p>' if p["gen"] else ""
            if p["med"]:
                srcs += f'<p class="src"><b>Medical education:</b> {e("; ".join(p["med"]))}</p>'
            if not p["med_ok"]:
                srcs += '<p class="src flag">Evidence from general education only</p>'
            out.append(f'<div class="ped-row"><div><h4>{e(p["name"])}</h4><p>{e(p["summary"])}</p>{srcs}</div>'
                       f'<div><span class="basis {p["basis"]}">{label[p["basis"]]}</span></div>'
                       f'<div class="where"><b>Applied in</b>{where if "span" in where else e(where)}</div></div>')
        out.append("</div>")
    return "".join(out)


def build_site(cards, variants, cfg, public_card):
    # every shared skill gets a short label for tables and diagrams (card field `short`, else its title)
    known = {n for n, _ in visuals.SHORT}
    for c in cards:
        if not c.get("_variant") and c["name"] not in known:
            visuals.SHORT.append((c["name"], c.get("short") or c["title"]))
    ped = ped_entries([n for n, _ in visuals.SHORT if n in {c["name"] for c in cards}])
    gh = f"https://github.com/{cfg['repo']}"
    # clean generated output, keep nothing stale
    for p in ("downloads", "paste", "skills", "workshops"):
        if (DOCS / p).exists():
            shutil.rmtree(DOCS / p)
    for p in DOCS.glob("*.html"):
        p.unlink()
    for p in ("downloads", "paste", "skills", "workshops"):
        (DOCS / p).mkdir(parents=True, exist_ok=True)
    for c in cards + variants:
        shutil.copy(ROOT / "dist" / "zips" / f"{c['name']}.zip", DOCS / "downloads")
        shutil.copy(ROOT / "dist" / "paste" / f"{c['name']}.md", DOCS / "paste")
    for f in ("logo.svg", "logo.png", "favicon.svg", "favicon.png", "og-image.png"):
        shutil.copy(ROOT / "assets" / f, DOCS / f)
    shutil.copy(SITE / "style.css", DOCS / "style.css")
    shutil.copy(SITE / "site.js", DOCS / "site.js")
    for f in ("deck.css", "deck.js"):
        shutil.copy(SITE / f, DOCS / f)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    (DOCS / "feed.xml").write_text(community.feed_xml({c["name"]: c["title"] for c in cards}, cfg["site_url"], cfg["library_name"]), encoding="utf-8")

    by_parent = {}
    for v in variants:
        by_parent.setdefault(v["variant_of"], []).append(v)
    catalog = []
    for c in cards:
        pc = public_card(c)
        pc["variants"] = [v["name"] for v in by_parent.get(c["name"], [])]
        pc["icon"] = visuals.icon(c["name"], 26)
        catalog.append(pc)

    wss = workshops.load()
    pages = {
        "index.html": (f"{cfg['library_name']} — shared AI skills for biomedical research and medical education",
                       "Shared AI skills for educators in biomedical research and medicine.",
                       read("home.html").replace("{{HERO_ART}}", visuals.hero_svg()), "", read("home.js")),
        "start.html": ("New to skills? — " + cfg["library_name"], "What an AI skill is and how to use one.",
                       fill_steps(read("start.html")), "start.html", ""),
        "skills.html": ("The skills — " + cfg["library_name"], "Search and download the skills.",
                        read("skills.html").replace("{{STATIC_LIST}}", static_list(cards)), "skills.html", read("skills.js")),
        "contribute.html": ("Contribute — " + cfg["library_name"], "Adapt, improve and share skills.",
                            read("contribute.html").replace("{{GUIDE}}", visuals.guide_html(gh)).replace("{{CYCLE}}", visuals.cycle_svg()).replace("{{EFFORT}}", visuals.effort_html(EFFORT)), "contribute.html", ""),
        "quality.html": ("Quality and review — " + cfg["library_name"], "How skills are tested and approved.",
                         read("quality.html").replace("{{APPROVAL}}", visuals.approval_html(APPROVAL)).replace("{{STATUS_TABLE}}", status_table(cards)).replace("{{CYCLE}}", visuals.cycle_svg()), "quality.html", ""),
        "community.html": ("Community — " + cfg["library_name"], "Contributions by country and institution.",
                           read("community.html").replace("{{COUNTERS}}", community.counters_html()).replace("{{MAP}}", community.map_svg()).replace(
                               "{{COUNTRIES}}", community.countries_html()).replace("{{INSTITUTIONS}}", community.institutions_html()).replace(
                               "{{RECENT}}", community.recent_html({c["name"]: c["title"] for c in cards})), "community.html", ""),
        "workshops.html": ("Workshops — " + cfg["library_name"], "Two ready-to-run workshops: using AI skills, and writing them. Lesson plans, slides and timings.",
                           read("workshops.html").replace("{{WORKSHOPS}}", workshops.hub_html(wss, gh)), "workshops.html", ""),
        "about.html": ("Why this project — " + cfg["library_name"], "Why shared AI skills matter for biomedical research and medical education, and who is behind the project.",
                       read("about.html").replace("{{ACCESS}}", visuals.access_svg() + visuals.access_svg(stacked=True)).replace("{{IDEA}}", visuals.idea_html()), "about.html", ""),
        "pedagogy.html": ("Pedagogy — " + cfg["library_name"], "The pedagogical foundations of the skills.",
                          read("pedagogy.html").replace("{{PED_ROWS}}", ped_rows(ped)).replace("{{MATRIX}}", visuals.matrix_html(ped)).replace(
                              "{{PEDAGOGY_MD}}", gh_links(md(pedagogy_body()), gh).replace(
                              "<h2>Each principle in detail</h2>",
                              visuals.tiers_html(ped) + visuals.coverage_html(ped, principles.LAYERS) + "<h2>Each principle in detail</h2>", 1)),
                          "pedagogy.html", ""),
    }
    for fname, (title, desc, content, active, scripts) in pages.items():
        content = re.sub(r"\{\{UI:(\w+)\}\}", lambda m: visuals.ui_icon(m.group(1)), content)
        (DOCS / fname).write_text(layout(cfg, title, desc, content, active, scripts=scripts, catalog=catalog, path=fname), encoding="utf-8")
    (DOCS / "sitemap.xml").write_text(sitemap(cfg, cards, wss), encoding="utf-8")
    deck_ver = hashlib.sha1((SITE / "deck.css").read_bytes() + (SITE / "deck.js").read_bytes()).hexdigest()[:10]
    for k, w in enumerate(wss):
        other = wss[(k + 1) % len(wss)]
        (DOCS / "workshops" / f"{w['id']}.html").write_text(
            layout(cfg, f"Workshop: {w['title']} — {cfg['library_name']}", w["tagline"], workshops.plan_html(w, other, gh),
                   "workshops.html", root="../", scripts=workshops.PLAN_JS, path=f"workshops/{w['id']}.html"), encoding="utf-8")
        (DOCS / "workshops" / f"{w['id']}-slides.html").write_text(workshops.deck_html(w, gh, deck_ver, cfg["site_url"]), encoding="utf-8")
        workshop_pptx.build(w, DOCS / "downloads" / f"workshop-{w['id']}.pptx", workshops.clock, workshops.segments,
                            cfg["site_url"].replace("https://", ""))
    for c in cards:
        c2 = dict(c)
        c2.update(public_card(c))
        for v in by_parent.get(c["name"], []):
            v.update({k: val for k, val in public_card(v).items() if k in ("zip", "paste")})
        (DOCS / "skills" / f"{c['name']}.html").write_text(
            skill_page(c2, cfg, by_parent.get(c["name"], [])), encoding="utf-8")

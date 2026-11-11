"""
Workshops: lesson plans, slide decks and PowerPoint downloads, from one source.

Each workshop is a YAML file in community/workshops/. From it the build makes:
    docs/workshops.html                  the overview: which workshop to run
    docs/workshops/<id>.html             the full plan: preparation, timing, script, handouts
    docs/workshops/<id>-slides.html      the slides, presented in the browser (and printable)
    docs/downloads/workshop-<id>.pptx    the same slides with speaker notes, to edit
"""
import html
import re
from pathlib import Path

import yaml

import visuals

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "community" / "workshops"


def e(s):
    return html.escape(str(s), quote=True)


def load():
    return sorted((yaml.safe_load(p.read_text(encoding="utf-8")) for p in SRC.glob("*.yaml")), key=lambda w: w["order"])


def validate(ws):
    """Problems a maintainer must fix before publishing: timings that don't add up, slide references that don't exist."""
    errs = []
    for w in ws:
        total = sum(a["minutes"] for a in w["agenda"])
        if total != w["minutes"]:
            errs.append(f"[workshop {w['id']}] agenda adds up to {total} min, not {w['minutes']}")
        n = len(w["slides"])
        for a in w["agenda"]:
            lo, hi = a["slides"]
            if not (1 <= lo <= hi <= n):
                errs.append(f"[workshop {w['id']}] '{a['title']}' points to slides {lo}-{hi}, deck has {n}")
        for k, s in enumerate(w["slides"], 1):
            if not s.get("notes"):
                errs.append(f"[workshop {w['id']}] slide {k} has no speaker notes")
    return errs


def links(s, root, gh):
    return s.replace("{ROOT}", root).replace("{GH}", gh)


def inline(s, root="", gh=""):
    """The small Markdown subset used in the workshop files: **bold**, [text](url), `code`."""
    s = e(links(s, root, gh))
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    return s


def plain(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    return re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", s)


def clock(t):
    return f"{t // 60}:{t % 60:02d}"


def segments(w):
    """Agenda rows with their start and end minute."""
    t, out = 0, []
    for a in w["agenda"]:
        out.append(dict(a, start=t, end=t + a["minutes"]))
        t += a["minutes"]
    return out


def hours(m):
    return f"{m} minutes" if m < 120 else f"{m // 60} hours" + (f" {m % 60} minutes" if m % 60 else "")


# ---------- the overview page ----------

def hub_html(ws, gh):
    cards = []
    for w in ws:
        cards.append(
            f'<article class="ws-card">'
            f'<p class="ws-level">{e(w["level"])}, {hours(w["minutes"])}</p>'
            f'<h2 id="{e(w["id"])}">{e(w["title"])}</h2>'
            f'<p class="ws-tag">{e(w["tagline"])}</p>'
            f'<dl class="ws-facts"><div><dt>For</dt><dd>{e(w["audience"])}</dd></div>'
            f'<div><dt>Group</dt><dd>{e(w["group"])}</dd></div>'
            f'<div><dt>Participants leave with</dt><dd>{e(w["outcome"])}</dd></div></dl>'
            f'{visuals.timeline_html([(a["minutes"], e(a["title"]), "") for a in w["agenda"]], w["minutes"], 30, main_block(w))}'
            f'<p class="ws-actions"><a class="btn primary" href="workshops/{e(w["id"])}.html">Open the full plan</a> '
            f'<a class="btn plain" href="workshops/{e(w["id"])}-slides.html">Present the slides</a> '
            f'<a class="btn plain" href="downloads/workshop-{e(w["id"])}.pptx" download>PowerPoint</a></p>'
            f'</article>')
    return "".join(cards)


def main_block(w):
    return max(range(len(w["agenda"])), key=lambda k: w["agenda"][k]["minutes"])


# ---------- the full plan ----------

def ul(items, root, gh, cls=""):
    return f'<ul{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>' + "".join(f"<li>{inline(i, root, gh)}</li>" for i in items) + "</ul>"


def guide_html(g, root, gh):
    out = [f'<div class="ws-guide" id="guide-{e(g["id"])}"><h3>{e(g["title"])}</h3>']
    if g.get("intro"):
        out.append(f'<p>{inline(g["intro"], root, gh)}</p>')
    if g.get("steps"):
        out.append('<ol class="ws-steps">' + "".join(
            f'<li><b>{inline(s["title"], root, gh)}</b><span>{inline(s["text"], root, gh)}</span></li>' for s in g["steps"]) + "</ol>")
    if g.get("tools"):
        out.append('<div class="ws-tools">' + "".join(
            f'<div><h4>{e(t["name"])}</h4><ol>' + "".join(f"<li>{inline(s, root, gh)}</li>" for s in t["steps"]) + "</ol></div>"
            for t in g["tools"]) + "</div>")
    if g.get("checklist"):
        out.append('<ul class="ws-check">' + "".join(f"<li>{inline(c, root, gh)}</li>" for c in g["checklist"]) + "</ul>")
    if g.get("code"):
        out.append(f'<div class="ws-code"><button type="button" class="ws-copy">Copy</button><pre><code>{e(g["code"].rstrip())}</code></pre></div>')
    out.append("</div>")
    return "".join(out)


def plan_html(w, other, gh):
    root = "../"
    segs = segments(w)
    h = [f'<div class="pagehead wrap ws-head">'
         f'<p class="ws-crumb"><a href="../workshops.html">Workshops</a></p>'
         f'<h1>{e(w["title"])}</h1><p>{e(w["tagline"])}</p>'
         f'<p class="ws-actions"><a class="btn primary" href="{e(w["id"])}-slides.html">Present the slides</a> '
         f'<a class="btn plain" href="../downloads/workshop-{e(w["id"])}.pptx" download>Download PowerPoint</a> '
         f'<button type="button" class="btn plain ws-print">Print this plan</button></p></div>']
    h.append('<section><div class="wrap ws-plan">')

    h.append('<h2 id="glance">At a glance</h2><dl class="ws-facts wide">'
             f'<div><dt>Level</dt><dd>{e(w["level"])}</dd></div>'
             f'<div><dt>Length</dt><dd>{hours(w["minutes"])}</dd></div>'
             f'<div><dt>For</dt><dd>{e(w["audience"])}</dd></div>'
             f'<div><dt>Group</dt><dd>{e(w["group"])}</dd></div>'
             f'<div><dt>Who can lead it</dt><dd>{e(w["facilitator"])}</dd></div>'
             f'<div><dt>Participants leave with</dt><dd>{e(w["outcome"])}</dd></div></dl>')
    h.append('<h3>Learning objectives</h3><p class="sub">By the end, participants will be able to:</p>' + ul(w["objectives"], root, gh, "ws-obj"))

    h.append('<h2 id="bring">What participants bring</h2>' + ul(w["bring"], root, gh))

    pw = w["prework"]
    h.append(f'<h2 id="prework">{e(pw["title"])}</h2><p class="sub">{inline(pw["intro"], root, gh)}</p>'
             '<ol class="ws-steps">' + "".join(
                 f'<li><b>{inline(s["title"], root, gh)}</b><span>{inline(s["text"], root, gh)}</span></li>' for s in pw["steps"]) + "</ol>")
    inv = w["invite"]
    h.append(f'<details class="ws-invite"><summary>Invitation email to send participants</summary>'
             f'<p><b>Subject:</b> {e(inv["subject"])}</p>'
             f'<div class="ws-code"><button type="button" class="ws-copy">Copy</button><pre><code>{e(inv["body"].rstrip())}</code></pre></div></details>')

    h.append('<h2 id="prep">Preparing as the facilitator</h2>')
    h.append('<div class="ws-prep">' + "".join(
        f'<div><h3>{e(p["when"])}</h3>{ul(p["items"], root, gh, "ws-check")}</div>' for p in w["prep"]) + "</div>")

    h.append(f'<h2 id="timing">Timing</h2><p class="sub">{hours(w["minutes"])} in {len(segs)} parts. The darker bar is the main hands-on block.</p>')
    h.append(visuals.timeline_html([(a["minutes"], e(a["title"]), e(a["note"])) for a in segs], w["minutes"], 15, main_block(w)))
    h.append('<div class="ws-table"><table><thead><tr><th>Clock</th><th>Minutes</th><th>Part</th><th>Slides</th></tr></thead><tbody>' + "".join(
        f'<tr><td>{clock(a["start"])}–{clock(a["end"])}</td><td>{a["minutes"]}</td><td><a href="#part-{k}">{e(a["title"])}</a></td>'
        f'<td>{a["slides"][0]}{"–" + str(a["slides"][1]) if a["slides"][1] != a["slides"][0] else ""}</td></tr>'
        for k, a in enumerate(segs, 1)) + "</tbody></table></div>")

    h.append('<h2 id="plan">The session, part by part</h2><p class="sub">For each part: what you do, what participants do, what to say, and how you know the room is ready to move on. Clock times count from the start of the session.</p>')
    for k, a in enumerate(segs, 1):
        lo, hi = a["slides"]
        h.append(f'<article class="ws-part" id="part-{k}">'
                 f'<header><span class="ws-time">{clock(a["start"])}–{clock(a["end"])}<small>{a["minutes"]} min</small></span>'
                 f'<div><h3>{e(a["title"])}</h3><p>{e(a["note"])}. <a href="{e(w["id"])}-slides.html#{lo}">Slides {lo}{"–" + str(hi) if hi != lo else ""}</a></p></div></header>'
                 f'<div class="ws-cols"><div><h4>You</h4>{ul(a["facilitator"], root, gh)}</div>'
                 f'<div><h4>Participants</h4>{ul(a["participants"], root, gh)}</div></div>'
                 f'<blockquote class="ws-say"><b>What to say</b>{inline(a["say"], root, gh)}</blockquote>'
                 f'<p class="ws-ready"><b>Ready to move on when:</b> {inline(a["check"], root, gh)}</p></article>')

    h.append('<h2 id="handouts">Handouts and step-by-step guides</h2><p class="sub">Print these or share this page. Each is written for someone doing it for the first time.</p>')
    h.append("".join(guide_html(g, root, gh) for g in w["guides"]))

    h.append('<h2 id="trouble">When something goes wrong</h2><div class="faq">' + "".join(
        f'<details><summary>{inline(t["problem"], root, gh)}</summary><p>{inline(t["fix"], root, gh)}</p></details>' for t in w["troubleshooting"]) + "</div>")

    h.append('<h2 id="after">After the session</h2>' + ul(w["after"], root, gh, "ws-check"))
    h.append(f'<p class="join">The other workshop: <a href="{e(other["id"])}.html">{e(other["title"])}</a> ({e(other["level"]).lower()}, {hours(other["minutes"])}).</p>')
    h.append("</div></section>")
    return "".join(h)


PLAN_JS = """<script>
document.querySelectorAll('.ws-copy').forEach(b => b.addEventListener('click', () => {
  const t = b.parentElement.querySelector('code').innerText;
  (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(() => { b.textContent = 'Copied'; setTimeout(() => b.textContent = 'Copy', 1600); }).catch(() => {});
}));
document.querySelectorAll('.ws-print').forEach(b => b.addEventListener('click', () => {
  document.querySelectorAll('details').forEach(d => d.open = true); window.print();
}));
</script>"""


# ---------- the slides, in the browser ----------

def slide_body(w, s, k, gh):
    root = "../"
    kind, title = s["kind"], inline(s["title"], root, gh)
    pts = s.get("points", [])
    li = "".join(f"<li><span>{inline(p, root, gh)}</span></li>" for p in pts)
    if kind in ("title", "closing"):
        extra = f'<p class="sl-sub">{inline(s["text"], root, gh)}</p>' if s.get("text") else ""
        if pts:
            extra += f'<ul class="sl-list light">{li}</ul>'
        if s.get("link"):
            href = links(s["link"], root, gh)
            extra += f'<p class="sl-link"><a href="{e(href)}">{e(href.replace("../", "ai-skills-without-borders.github.io/skills/"))}</a></p>'
        return (f'<div class="sl-dark"><img class="sl-logo" src="../logo.svg" alt="" width="120" height="120">'
                f'<div><p class="sl-kicker">AI Skills Without Borders</p><h1>{title}</h1>{extra}</div></div>')
    if kind == "section":
        return f'<div class="sl-section"><p class="sl-part">{e(s["text"])}</p><h1>{title}</h1></div>'
    head = f'<h2>{title}</h2>'
    if kind == "agenda":
        rows = "".join(
            f'<li><span class="ag-time">{clock(a["start"])}</span><b>{e(a["title"])}</b>'
            f'<span class="ag-bar"><i style="left:{a["start"] / w["minutes"] * 100:.2f}%;width:{a["minutes"] / w["minutes"] * 100:.2f}%"></i></span>'
            f'<span class="ag-min">{a["minutes"]} min</span></li>' for a in segments(w))
        return head + f'<ol class="sl-agenda">{rows}</ol>'
    if kind in ("steps",):
        return head + f'<ol class="sl-steps n{len(pts)}">{li}</ol>' + link_html(s, root, gh)
    if kind in ("checklist",):
        return head + f'<ul class="sl-checks">{li}</ul>'
    if kind == "rules":
        return head + f'<ul class="sl-cards c{len(pts)}">{li}</ul>'
    if kind == "compare":
        side = lambda d, c: (f'<div class="sl-side {c}"><h3>{inline(d["title"], root, gh)}</h3><ul>'
                             + "".join(f"<li>{inline(p, root, gh)}</li>" for p in d["points"]) + "</ul></div>")
        return head + f'<div class="sl-compare">{side(s["left"], "a")}{side(s["right"], "b")}</div>'
    if kind == "equation":
        p = s["parts"]
        box = lambda d, c="": f'<div class="eq-box{c}"><b>{e(d["title"])}</b><span>{e(d["text"])}</span></div>'
        return head + f'<div class="sl-eq">{box(p[0])}<span class="eq-op">+</span>{box(p[1])}<span class="eq-op">=</span>{box(p[2], " out")}</div>'
    if kind == "grid":
        return head + '<div class="sl-grid">' + "".join(
            f'<div><b>{e(c["title"])}</b><span>{e(c["text"])}</span></div>' for c in s["cards"]) + "</div>"
    if kind == "demo":
        return head + (f'<div class="sl-demo"><div><h3>Watch for</h3><ul class="sl-checks small">{li}</ul></div>'
                       '<div class="demo-chats"><div class="chat"><p class="chat-h">Without the skill</p><i></i><i></i><i class="short"></i></div>'
                       '<div class="chat on"><p class="chat-h">With the skill</p><i class="q">Which learners? Which framework?</i><i></i><i class="ok">Approve this plan?</i><i></i></div></div></div>')
    if kind == "exercise":
        return (f'<div class="sl-ex"><div class="ex-clock"><b>{s["minutes"]}</b><span>minutes</span></div>'
                f'<div><p class="sl-part">Your turn</p>{head}<ol class="sl-list">{li}</ol>{link_html(s, root, gh)}</div></div>')
    if kind == "anatomy":
        return head + ('<div class="sl-anat"><div class="anat-file"><p class="anat-name">SKILL.md</p>'
                       '<div class="af hl1"><code>name: …</code><code>description: what it does, and when</code></div>'
                       '<div class="af hl2"><code>## Step 1 …</code><code>## Step 2 …</code></div>'
                       '<div class="af hl3"><code>Stop: show the plan, wait for approval</code></div>'
                       '<div class="af hl4"><code>## Output</code></div>'
                       '<div class="af hl5"><code>## Limitations</code></div></div>'
                       f'<ol class="anat-key">{li}</ol></div>')
    return head + f'<ul class="sl-list">{li}</ul>'


def link_html(s, root, gh):
    if not s.get("link"):
        return ""
    href = links(s["link"], root, gh)
    return f'<p class="sl-link"><a href="{e(href)}">{"Open the form" if "issues/new" in href else "Open the page"}</a></p>'


def deck_html(w, gh, css_ver):
    slides = []
    for k, s in enumerate(w["slides"], 1):
        dark = " dark" if s["kind"] in ("title", "closing") else (" sect" if s["kind"] == "section" else "")
        slides.append(f'<section class="slide k-{s["kind"]}{dark}" id="s{k}" aria-label="Slide {k}">'
                      f'<div class="sl-in">{slide_body(w, s, k, gh)}</div>'
                      f'<footer class="sl-foot"><span>{e(w["title"])}</span><span>{k} / {len(w["slides"])}</span></footer>'
                      f'<aside class="sl-notes"><b>Speaker notes</b>{inline(s["notes"], "../", gh)}</aside></section>')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Slides: {e(w["title"])} — AI Skills Without Borders</title>
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../deck.css?v={css_ver}">
</head>
<body class="deck">
<div class="deck-bar">
  <a href="{e(w["id"])}.html">← The full plan</a>
  <span class="deck-help">Keys: arrows to move, N for notes, F for full screen, P to print</span>
  <span class="deck-btns"><button type="button" data-act="prev" aria-label="Previous slide">←</button><button type="button" data-act="next" aria-label="Next slide">→</button><button type="button" data-act="notes" aria-pressed="false">Notes</button><button type="button" data-act="full">Full screen</button></span>
</div>
<main class="stage">
{"".join(slides)}
</main>
<script src="../deck.js?v={css_ver}"></script>
</body>
</html>"""

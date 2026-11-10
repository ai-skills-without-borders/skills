"""SVG and HTML visuals for the website (icons, diagrams). Used by tools/website.py."""
import math

NAVY, TEAL, BLUE, YELLOW, RULE = "#22405f", "#3d9696", "#4a86a8", "#f4dc4a", "#c9d6d3"

# 24x24 line icons, one per shared skill. Unknown skills get the generic icon.
_ICON_PATHS = {
    "learning-objectives-designer": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4" fill="currentColor"/><path d="M15.5 8.5 21 3M17.5 3H21v3.5"/>',
    "pbl-rbl-session-builder": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.3 15.3 21 21"/><circle cx="8.5" cy="9" r="1.3"/><circle cx="12.5" cy="12" r="1.3"/><path d="M9.5 9.8l2 1.4"/>',
    "reading-material-generator": '<path d="M12 6.5C10 5 7 4.5 3.5 5v13c3.5-.5 6.5 0 8.5 1.5 2-1.5 5-2 8.5-1.5V5C17 4.5 14 5 12 6.5Z"/><path d="M12 6.5v13"/><path d="M6 9h3.5M6 12h3.5M14.5 9H18"/>',
    "syllabus-builder": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/><path d="M7 13h2M11 13h2M15 13h2M7 16.5h2M11 16.5h2"/>',
    "lesson-format-checker": '<rect x="5" y="4.5" width="14" height="17" rx="2"/><path d="M9 3h6v3H9z"/><path d="m8.5 13 2.5 2.5 4.5-5"/>',
    "exam-question-writer": '<circle cx="6" cy="7" r="2"/><circle cx="6" cy="13" r="2"/><circle cx="6" cy="19" r="2"/><circle cx="6" cy="13" r=".8" fill="currentColor"/><path d="M10.5 7H20M10.5 13H20M10.5 19H17"/>',
}
_GENERIC = '<path d="M7 3.5h7l4 4V20a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4.5a1 1 0 0 1 1-1Z"/><path d="M14 3.5V8h4M9 12h6M9 15.5h6"/>'


def icon(name, size=24, cls="sk-icon"):
    body = _ICON_PATHS.get(name, _GENERIC)
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')


def hero_svg():
    """Institutions exchange skills through the shared library; each skill runs in any assistant."""
    f = 'font-family="Atkinson Hyperlegible, system-ui, sans-serif"'
    building = lambda x, y: (f'<path d="M{x - 13} {y + 9}h26M{x - 11} {y + 9}v-11M{x - 4} {y + 9}v-11M{x + 4} {y + 9}v-11M{x + 11} {y + 9}v-11M{x - 14} {y - 3}h28L{x} {y - 12}Z" '
                             f'fill="none" stroke="{NAVY}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>')
    left, right = [], []
    for i, label in enumerate(["Your school", "Partner school", "Any educator"]):
        y = 60 + i * 116
        left.append(f'<circle cx="50" cy="{y}" r="32" fill="#fff" stroke="{TEAL}" stroke-width="2.5"/>' + building(50, y)
                    + f'<text x="50" y="{y + 52}" text-anchor="middle" font-size="12.5" font-weight="700" fill="{NAVY}">{label}</text>')
        # two-way exchange: share in (teal) and take out (blue)
        left.append(f'<path d="M80 {y - 6} C 120 {y - 6}, 130 {150 + (i - 1) * 18}, 168 {150 + (i - 1) * 18}" fill="none" stroke="{TEAL}" stroke-width="3" stroke-dasharray="0.1 8" stroke-linecap="round"/>')
        left.append(f'<path d="M168 {164 + (i - 1) * 18} C 130 {164 + (i - 1) * 18}, 120 {y + 8}, 80 {y + 8}" fill="none" stroke="{BLUE}" stroke-width="3" stroke-dasharray="0.1 8" stroke-linecap="round"/>')
    tools = ["Claude", "ChatGPT", "Gemini", "Copilot"]
    for i, t in enumerate(tools):
        y = 34 + i * 76
        right.append(f'<path d="M298 172 C 330 172, 330 {y + 25}, 356 {y + 25}" fill="none" stroke="{BLUE}" stroke-width="2.6" stroke-dasharray="0.1 8" stroke-linecap="round"/>'
                     f'<rect x="358" y="{y}" width="112" height="50" rx="11" fill="#fff" stroke="{RULE}" stroke-width="2"/>'
                     f'<text x="414" y="{y + 31}" text-anchor="middle" font-size="15" font-weight="700" fill="{NAVY}">{t}</text>')
    hub = (f'<rect x="170" y="90" width="128" height="164" rx="12" fill="#fff" stroke="{NAVY}" stroke-width="2.5"/>'
           f'<path d="M170 102a12 12 0 0 1 12-12h104a12 12 0 0 1 12 12v20H170Z" fill="{NAVY}"/>'
           f'<text x="234" y="112" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">shared skills</text>'
           + "".join(f'<rect x="186" y="{136 + k * 26}" width="96" height="16" rx="5" fill="{c}"/>' for k, c in enumerate([YELLOW, TEAL, BLUE, TEAL]))
           + f'<text x="234" y="276" text-anchor="middle" font-size="12" fill="#4b6178">open library</text>')
    return ('<svg class="hero-art" viewBox="0 0 480 350" role="img" aria-labelledby="hero-art-t">'
            '<title id="hero-art-t">Institutions share and take skills from one open library, and every skill works in Claude, ChatGPT, Gemini and Copilot</title>'
            f'<g {f}>{"".join(left)}{hub}{"".join(right)}</g></svg>')


def cycle_svg():
    steps = [("Use it", "on a real task"), ("Report", "what happened"), ("Improve", "suggest or edit"),
             ("Review", "by another school"), ("Trust grows", "maturity rises")]
    cx, cy, r = 230, 220, 150
    nodes, arrows = [], []
    n = len(steps)
    for i, (a, b) in enumerate(steps):
        ang = math.radians(-90 + i * 360 / n)
        x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
        fill = YELLOW if i == 0 else "#fff"
        nodes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="54" fill="{fill}" stroke="{TEAL}" stroke-width="3"/>'
                     f'<text x="{x:.1f}" y="{y - 2:.1f}" text-anchor="middle" font-size="16" font-weight="700" fill="{NAVY}">{a}</text>'
                     f'<text x="{x:.1f}" y="{y + 17:.1f}" text-anchor="middle" font-size="11.5" fill="#4b6178">{b}</text>')
        mid = math.radians(-90 + (i + 0.5) * 360 / n)
        mx, my = cx + r * math.cos(mid), cy + r * math.sin(mid)
        rot = math.degrees(mid) + 90
        arrows.append(f'<path d="M-7 -6 L5 0 L-7 6" transform="translate({mx:.1f} {my:.1f}) rotate({rot:.1f})" '
                      f'fill="none" stroke="{BLUE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    ring = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BLUE}" stroke-width="3" stroke-dasharray="0.1 9" stroke-linecap="round"/>'
    center = (f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" font-size="14" fill="#4b6178">every loop makes</text>'
              f'<text x="{cx}" y="{cy + 14}" text-anchor="middle" font-size="14" fill="#4b6178">the skill better</text>')
    return ('<svg class="cycle-art" viewBox="0 0 460 440" role="img" aria-labelledby="cycle-t">'
            '<title id="cycle-t">How a skill improves: use it, report, improve, review, and trust grows</title>'
            f'<g font-family="Atkinson Hyperlegible, system-ui, sans-serif">{ring}{"".join(arrows)}{center}{"".join(nodes)}</g></svg>')


SHORT = [("learning-objectives-designer", "Objectives"), ("syllabus-builder", "Syllabus"),
         ("pbl-rbl-session-builder", "Session"), ("reading-material-generator", "Reading"),
         ("exam-question-writer", "Exam items"), ("lesson-format-checker", "Lesson check")]
_ALIASES = {"Objectives": "learning-objectives-designer", "Syllabus": "syllabus-builder", "Session": "pbl-rbl-session-builder",
            "Reading": "reading-material-generator", "Exam items": "exam-question-writer", "Lesson check": "lesson-format-checker"}


def matrix_html(ped):
    head = "".join(f'<th scope="col"><a href="skills/{n}.html">{icon(n, 22)}<span>{s}</span></a></th>' for n, s in SHORT)
    rows = []
    for title, _d, basis, where, _src in ped:
        used = {n for n, _ in SHORT} if where.strip() == "Every skill" else {_ALIASES[w.strip()] for w in where.split(",") if w.strip() in _ALIASES}
        cells = "".join(f'<td>{"<span class=\"dot " + basis + "\" title=\"" + basis + "\"></span>" if n in used else ""}</td>' for n, _ in SHORT)
        rows.append(f'<tr><th scope="row">{title}</th>{cells}</tr>')
    return (f'<div class="matrix-wrap"><table class="matrix"><thead><tr><th></th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


_STEP = {
    "ASK": '<path d="M4 5.5h16v10H9l-5 4z"/>',
    "MATCH": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.3 15.3 21 21"/><path d="m7.8 10.6 2 2 3.6-4"/>',
    "FRAME": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6h1M4 12h1M4 18h1"/>',
    "KNOW": '<path d="M12 6.5C10 5 7 4.5 3.5 5v13c3.5-.5 6.5 0 8.5 1.5 2-1.5 5-2 8.5-1.5V5C17 4.5 14 5 12 6.5Z"/><path d="M12 6.5v13"/>',
    "OK": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
}


def step_icon(key):
    return (f'<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_STEP[key]}</svg>')


def anatomy_svg(stacked=False):
    """Illustrated anatomy of a skill folder with three numbered callouts (side by side, or stacked for phones)."""
    f = 'font-family="Atkinson Hyperlegible, system-ui, sans-serif"'
    lines = lambda x, y, n, w, c: "".join(f'<rect x="{x}" y="{y + i * 14}" width="{w - (i % 2) * 22}" height="6" rx="3" fill="{c}" opacity=".85"/>' for i in range(n))
    doc = lambda x, y, label: (f'<path d="M{x} {y}h34l10 10v40a3 3 0 0 1-3 3h-41a3 3 0 0 1-3-3V{y + 3}a3 3 0 0 1 3-3Z" fill="#fff" stroke="{BLUE}" stroke-width="2"/>'
                               f'<path d="M{x + 34} {y}v10h10" fill="none" stroke="{BLUE}" stroke-width="2"/>'
                               f'<rect x="{x + 6}" y="{y + 20}" width="28" height="4" rx="2" fill="{BLUE}"/><rect x="{x + 6}" y="{y + 30}" width="22" height="4" rx="2" fill="{BLUE}"/>'
                               f'<text x="{x + 20}" y="{y + 70}" text-anchor="middle" font-size="12" fill="#4b6178">{label}</text>')
    callout = lambda n, x, y, title, sub: (f'<circle cx="{x}" cy="{y}" r="13" fill="{NAVY}"/><text x="{x}" y="{y + 5}" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">{n}</text>'
                                           f'<text x="{x + 22}" y="{y - 1}" font-size="15" font-weight="700" fill="{NAVY}">{title}</text>'
                                           f'<text x="{x + 22}" y="{y + 17}" font-size="12.5" fill="#4b6178">{sub}</text>')
    body = (
        # folder
        f'<path d="M14 40a8 8 0 0 1 8-8h86l14 16h176a8 8 0 0 1 8 8v320a8 8 0 0 1-8 8H22a8 8 0 0 1-8-8Z" fill="#eef5f4" stroke="{TEAL}" stroke-width="2.5"/>'
        f'<text x="30" y="70" font-size="14" font-weight="700" fill="{NAVY}">exam-question-writer/</text>'
        # SKILL.md card
        f'<rect x="34" y="86" width="244" height="164" rx="10" fill="#fff" stroke="{NAVY}" stroke-width="2.2"/>'
        f'<text x="48" y="110" font-size="14" font-weight="700" fill="{NAVY}">SKILL.md</text>'
        f'<rect x="46" y="120" width="220" height="36" rx="6" fill="#fdf6c9" stroke="{YELLOW}" stroke-width="2"/>'
        f'<text x="56" y="136" font-size="11.5" fill="#5a4a00">description:</text>'
        f'<text x="56" y="150" font-size="11.5" fill="#5a4a00">"Use when you need exam questions…"</text>'
        f'<rect x="46" y="164" width="220" height="76" rx="6" fill="#e4f1ef" stroke="{TEAL}" stroke-width="2"/>'
        + lines(58, 176, 5, 190, TEAL) +
        # references folder with three docs
        f'<rect x="34" y="266" width="244" height="104" rx="10" fill="#fff" stroke="{BLUE}" stroke-width="2.2" stroke-dasharray="0"/>'
        f'<text x="48" y="288" font-size="14" font-weight="700" fill="{NAVY}">references/</text>'
        + doc(56, 298, "") + doc(130, 298, "") + doc(204, 298, "") +
        f'<text x="76" y="364" text-anchor="middle" font-size="11.5" fill="#4b6178">standards</text>'
        f'<text x="150" y="364" text-anchor="middle" font-size="11.5" fill="#4b6178">checklists</text>'
        f'<text x="224" y="364" text-anchor="middle" font-size="11.5" fill="#4b6178">examples</text>'
    )
    if stacked:
        badge = lambda n, x, y: f'<circle cx="{x}" cy="{y}" r="12" fill="{NAVY}"/><text x="{x}" y="{y + 5}" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">{n}</text>'
        body += badge(1, 270, 122) + badge(2, 270, 168) + badge(3, 270, 270)
        body += (callout(1, 28, 418, "When to use it", "the words educators say")
                 + callout(2, 28, 466, "The framework", "steps, checkpoints, result")
                 + callout(3, 28, 514, "The knowledge", "loaded only when needed"))
        vb = "0 0 312 540"
    else:
        body += (f'<path d="M266 138H330" stroke="{YELLOW}" stroke-width="2.5" stroke-dasharray="0.1 6" stroke-linecap="round"/>'
                 f'<path d="M266 202H330" stroke="{TEAL}" stroke-width="2.5" stroke-dasharray="0.1 6" stroke-linecap="round"/>'
                 f'<path d="M278 318H330" stroke="{BLUE}" stroke-width="2.5" stroke-dasharray="0.1 6" stroke-linecap="round"/>'
                 + callout(1, 346, 136, "When to use it", "the words educators say")
                 + callout(2, 346, 200, "The framework", "steps, checkpoints, result")
                 + callout(3, 346, 316, "The knowledge", "loaded only when needed"))
        vb = "0 0 520 392"
    sid = "m" if stacked else "d"
    cls = "anatomy-art stacked" if stacked else "anatomy-art wide"
    return (f'<svg class="{cls}" viewBox="{vb}" role="img" aria-labelledby="anat-t{sid} anat-d{sid}">'
            f'<title id="anat-t{sid}">What is inside a skill</title>'
            f'<desc id="anat-d{sid}">A skill is a folder. SKILL.md holds the description that says when to use it and the instructions that form the framework. The references folder holds the knowledge: standards, checklists and examples.</desc>'
            f'<g {f}>{body}</g></svg>')


def equation_html():
    know = '<path d="M12 6.5C10 5 7 4.5 3.5 5v13c3.5-.5 6.5 0 8.5 1.5 2-1.5 5-2 8.5-1.5V5C17 4.5 14 5 12 6.5Z"/><path d="M12 6.5v13"/>'
    frame = '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="5" cy="6" r="1.2"/><circle cx="5" cy="12" r="1.2"/><circle cx="5" cy="18" r="1.2"/>'
    skill = '<path d="M7 3.5h7l4 4V20a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4.5a1 1 0 0 1 1-1Z"/><path d="M14 3.5V8h4"/><path d="m9 14 2 2 4-4.5"/>'
    svg = lambda body: (f'<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
                        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')
    return ('<div class="equation" role="img" aria-label="Knowledge plus framework equals a skill, which works in any assistant">'
            f'<div class="eq-item know"><span class="eq-icon">{svg(know)}</span><b>Knowledge</b><span>standards, rules, common mistakes</span></div>'
            '<div class="eq-op" aria-hidden="true">+</div>'
            f'<div class="eq-item frame"><span class="eq-icon">{svg(frame)}</span><b>Framework</b><span>steps, checkpoints, the shape of the result</span></div>'
            '<div class="eq-op" aria-hidden="true">=</div>'
            f'<div class="eq-item skill"><span class="eq-icon">{svg(skill)}</span><b>A skill</b><span>transferable know-how any assistant can use</span></div>'
            '</div>')

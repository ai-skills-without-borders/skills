"""SVG and HTML visuals for the website (icons, diagrams). Used by tools/website.py."""
import math

NAVY, TEAL, BLUE, YELLOW, RULE = "#22405f", "#3d9696", "#4a86a8", "#f4dc4a", "#c9d6d3"

# 24x24 line icons, one per shared skill. Unknown skills get the generic icon.
_ICON_PATHS = {
    "journal-club-planner": '<path d="M7 3.5h7l4 4v13H7z"/><path d="M14 3.5v4h4"/><path d="M9.5 12h6M9.5 15h6M9.5 18h3.5"/><circle cx="4.5" cy="9" r="1.5"/><path d="M2.5 14c.3-1.6 1-2.4 2-2.4"/>',
    "mentor-compact-creator": '<rect x="5" y="3.5" width="14" height="17" rx="2"/><path d="M8.5 8h7M8.5 11.5h7"/><path d="M8 17.5c1.2-1.4 2.4-1.4 3.6 0 1.2 1.4 2.4 1.4 3.6 0"/>',
    "committee-meeting-planner": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/><circle cx="9" cy="14" r="1.6"/><circle cx="15" cy="14" r="1.6"/><path d="M6.5 18.5c.4-1.3 1.3-2 2.5-2s2.1.7 2.5 2M12.5 18.5c.4-1.3 1.3-2 2.5-2s2.1.7 2.5 2"/>',
    "curriculum-map-builder": '<circle cx="12" cy="4.5" r="2"/><circle cx="5.5" cy="12" r="2"/><circle cx="18.5" cy="12" r="2"/><circle cx="5.5" cy="19.5" r="2"/><circle cx="12" cy="19.5" r="2"/><circle cx="18.5" cy="19.5" r="2"/><path d="M10.6 6 6.9 10.5M13.4 6l3.7 4.5M5.5 14v3.5M7 13.4l3.8 4.6M18.5 14v3.5"/>',
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
    rows, layer = [], None
    names = {"science": "Science teaching", "medicine": "Medical education", "ai": "AI era"}
    for p in ped:
        if p["layer"] != layer:
            layer = p["layer"]
            rows.append(f'<tr class="mlayer"><th colspan="{len(SHORT) + 1}" scope="rowgroup">{names[layer]}</th></tr>')
        basis = p["basis"]
        cells = "".join(f'<td>{"<span class=\"dot " + basis + "\" title=\"" + basis + "\"></span>" if n in p["used"] else ""}</td>' for n, _ in SHORT)
        flag = "" if p["med_ok"] else ' <span class="gen" title="Evidence from general education only">general ed.</span>'
        rows.append(f'<tr><th scope="row">{p["name"]}{flag}</th>{cells}</tr>')
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


# ---------------------------------------------------------------- generic line icons for pages

_UI = {
    "unequal": '<path d="M4 20V10M10 20V4M16 20v-6M22 20H2"/>',
    "open": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 7.5-2"/>',
    "flow": '<path d="M4 8h13l-3-3M20 16H7l3 3"/>',
    "grading": '<path d="M9 5h11M9 12h11M9 19h11"/><path d="m3 5 1.5 1.5L7 4M3 12l1.5 1.5L7 11"/><circle cx="5" cy="19" r="1.5"/>',
    "curriculum": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4M7 13h4M7 16.5h7"/>',
    "reading": '<path d="M12 6.5C10 5 7 4.5 3.5 5v13c3.5-.5 6.5 0 8.5 1.5 2-1.5 5-2 8.5-1.5V5C17 4.5 14 5 12 6.5Z"/><path d="M12 6.5v13"/>',
    "formatting": '<rect x="5" y="4.5" width="14" height="17" rx="2"/><path d="M9 3h6v3H9z"/><path d="m8.5 13 2.5 2.5 4.5-5"/>',
    "mentoring": '<circle cx="8" cy="8" r="3"/><circle cx="17" cy="10" r="2.4"/><path d="M2.5 20c.5-3.5 2.8-5.5 5.5-5.5s5 2 5.5 5.5M13.5 20c.4-2.6 1.8-4 3.5-4s3.1 1.4 3.5 4"/>',
    "write": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13.5 6.5 4 4"/>',
    "share": '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="m8.2 10.8 7.6-3.6M8.2 13.2l7.6 3.6"/>',
    "improve": '<path d="M20 12a8 8 0 1 1-2.4-5.7"/><path d="M20 4v4.5h-4.5"/>',
    "person": '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c.6-4 3.4-6.5 7-6.5s6.4 2.5 7 6.5"/>',
    "school": '<path d="M3 20h18M5 20v-8M9.5 20v-8M14.5 20v-8M19 20v-8M2.5 10h19L12 4z"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.8 2.8L16.5 9.5"/>',
}


def ui_icon(name, size=24, cls="ui-icon"):
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_UI[name]}</svg>')


def access_svg(stacked=False):
    """Before and after: expertise locked in one institution, then flowing through the open library to everyone."""
    f = 'font-family="Atkinson Hyperlegible, system-ui, sans-serif"'

    def school(x, y, has, ring):
        dot = f'<circle cx="{x + 15}" cy="{y - 15}" r="7" fill="{YELLOW}" stroke="{NAVY}" stroke-width="1.5"/>' if has else ""
        return (f'<circle cx="{x}" cy="{y}" r="24" fill="#fff" stroke="{ring}" stroke-width="2.2"/>'
                f'<path d="M{x - 10} {y + 7}h20M{x - 8} {y + 7}v-8M{x - 3} {y + 7}v-8M{x + 3} {y + 7}v-8M{x + 8} {y + 7}v-8M{x - 11} {y - 2}h22L{x} {y - 9}Z" '
                f'fill="none" stroke="{NAVY if ring != RULE else "#9aa9b5"}" stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round"/>' + dot)

    pos = [(150, 52), (250, 120), (215, 225), (85, 225), (50, 120)]
    # before: one institution holds the expertise, the others are on their own
    before = school(150, 135, True, TEAL)
    before += "".join(school(x, y, False, RULE) for x, y in pos)
    before += (f'<circle cx="150" cy="135" r="38" fill="none" stroke="{NAVY}" stroke-width="1.5" stroke-dasharray="4 4"/>'
               f'<text x="150" y="285" text-anchor="middle" font-size="15" font-weight="700" fill="{NAVY}">Today</text>'
               f'<text x="150" y="304" text-anchor="middle" font-size="12.5" fill="#4b6178">Expertise stays where it was built</text>')
    # after: the open library in the middle, two-way exchange with every institution
    after = ""
    for x, y in pos:
        after += (f'<path d="M150 135 L{x} {y}" stroke="{BLUE}" stroke-width="2.6" stroke-dasharray="0.1 7" stroke-linecap="round"/>')
    after += "".join(school(x, y, True, TEAL) for x, y in pos)
    after += (f'<rect x="118" y="108" width="64" height="56" rx="9" fill="{NAVY}"/>'
              + "".join(f'<rect x="130" y="{119 + k * 11}" width="40" height="6" rx="3" fill="{c}"/>' for k, c in enumerate([YELLOW, "#7cc4c4", "#9cc6dd", "#7cc4c4"]))
              + f'<text x="150" y="285" text-anchor="middle" font-size="15" font-weight="700" fill="{NAVY}">With shared skills</text>'
              f'<text x="150" y="304" text-anchor="middle" font-size="12.5" fill="#4b6178">Every educator can use it and add to it</text>')
    if stacked:
        legend = (f'<circle cx="92" cy="660" r="6" fill="{YELLOW}" stroke="{NAVY}" stroke-width="1.5"/>'
                  f'<text x="104" y="664" font-size="12.5" fill="#4b6178">teaching expertise</text>')
        arrow = f'<path d="M150 318v26m-9-10 9 10 9-10" fill="none" stroke="{NAVY}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
        return ('<svg class="access-art stacked" viewBox="0 0 300 675" role="img" aria-labelledby="access-ts">'
                '<title id="access-ts">Today, teaching expertise stays in the institution where it was built. With shared skills, an open library connects every institution, and each one both uses and adds expertise.</title>'
                f'<g {f}><g>{before}</g>{arrow}<g transform="translate(0 340)">{after}</g>{legend}</g></svg>')
    legend = (f'<circle cx="252" cy="330" r="6" fill="{YELLOW}" stroke="{NAVY}" stroke-width="1.5"/>'
              f'<text x="264" y="334" font-size="12.5" fill="#4b6178">teaching expertise</text>')
    arrow = f'<path d="M318 160h34m-10-9 10 9-10 9" fill="none" stroke="{NAVY}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
    return ('<svg class="access-art wide" viewBox="0 0 670 345" role="img" aria-labelledby="access-t">'
            '<title id="access-t">Today, teaching expertise stays in the institution where it was built. With shared skills, an open library connects every institution, and each one both uses and adds expertise.</title>'
            f'<g {f}><g>{before}</g>{arrow}<g transform="translate(370 0)">{after}</g>{legend}</g></svg>')


def idea_html():
    """Write once, share, improve together: three steps that loop."""
    steps = [("write", "Write it once", "An educator who knows a task well writes the skill: what it is for, what it needs, the steps, what it should produce, and its limits."),
             ("share", "Share it", "Colleagues at other institutions use it in their own AI tool: Claude, ChatGPT, Gemini or Copilot, with a paste-in version for free plans."),
             ("improve", "Improve it together", "Each use, report, adaptation and review makes the skill better and shows how far it can be trusted.")]
    items = "".join(f'<li><span class="idea-ic">{ui_icon(k, 26)}</span><b>{t}</b>{d}</li>' for k, t, d in steps)
    return f'<div class="idea"><ol class="idea-steps">{items}</ol><p class="idea-loop" aria-hidden="true"><span>and back to the start: every improvement reaches every user</span></p></div>'


def timeline_html(segments, total):
    """A schedule drawn to scale: one row per segment, bar placed at its start time."""
    rows, t = [], 0
    for mins, title, note in segments:
        left, width = t / total * 100, mins / total * 100
        rows.append(f'<li><div class="tl-text"><b>{title}</b><span>{note}</span></div>'
                    f'<div class="tl-track"><span class="tl-bar" style="left:{left:.2f}%;width:{width:.2f}%"><em>{mins} min</em></span></div></li>')
        t += mins
    ticks = "".join(f'<span style="left:{m / total * 100:.2f}%">{m}</span>' for m in range(0, total + 1, 15))
    return (f'<div class="timeline"><ol>{"".join(rows)}</ol>'
            f'<div class="tl-axis"><div class="tl-text"></div><div class="tl-ticks">{ticks}</div></div></div>')


def tiers_html(entries):
    """How a principle earns its place: origin source, then medical-education evidence, else a visible flag."""
    return ('<div class="tiers">'
            '<div class="tier"><span class="tier-n">1</span><b>Origin</b><span>The source where the principle was first formulated, often in the learning sciences</span></div>'
            '<span class="tier-plus" aria-hidden="true">+</span>'
            '<div class="tier"><span class="tier-n">2</span><b>Medical-education evidence</b><span>A study with health-professions learners, or a standard from a medical-education body</span></div>'
            '<span class="tier-plus" aria-hidden="true">=</span>'
            '<div class="tier-out"><div class="ok"><b>Ready for medical educators</b></div><div class="flag"><b>If tier 2 is missing</b>marked “evidence from general education only”</div></div>'
            '</div>')


def coverage_html(entries, layers):
    """One square per principle, by layer: filled when health-professions evidence backs it."""
    rows = []
    for layer, (title, _) in layers.items():
        ps = [p for p in entries if p["layer"] == layer]
        ok = sum(p["med_ok"] for p in ps)
        cells = "".join(f'<span class="sq {"ok" if p["med_ok"] else "gap"}" title="{p["name"]}"><span class="vh">{p["name"]}: {"medical-education evidence" if p["med_ok"] else "general education only"}</span></span>' for p in ps)
        rows.append(f'<div class="cov-row"><div class="cov-name">{title}</div><div class="cov-cells">{cells}</div><div class="cov-n">{ok} of {len(ps)}</div></div>')
    total = len(entries)
    ok = sum(p["med_ok"] for p in entries)
    return (f'<div class="coverage"><p class="cov-head"><b>{ok} of {total}</b> principles have evidence from health-professions education.</p>{"".join(rows)}'
            '<p class="cov-legend"><span class="sq ok"></span> medical-education evidence <span class="sq gap"></span> general education only, still needed</p></div>')


def effort_html(items):
    """Ways to contribute as a staircase: more time, more impact."""
    n = len(items)
    steps = "".join(f'<a class="stair" href="{href}" style="--h:{(i + 1) / n:.3f}"><span class="stair-bar"></span><b>{title}</b><span>{time}</span></a>'
                    for i, (title, time, href) in enumerate(items))
    return f'<div class="stairs" role="list">{steps}</div><p class="stairs-axis" aria-hidden="true"><span>Less time</span><span>More time, more impact</span></p>'


def approval_html(rows):
    """Who approves what: change, approver, and what must be true."""
    out = "".join(f'<li><div class="ap-what">{ui_icon(ic, 22)}<b>{what}</b></div><span class="ap-arrow" aria-hidden="true"></span>'
                  f'<div class="ap-who">{ui_icon(who_ic, 22)}<b>{who}</b><span>{need}</span></div></li>'
                  for ic, what, who_ic, who, need in rows)
    return f'<ol class="approval">{out}</ol>'


# ---------------------------------------------------------------- first-contribution guide

def _screen(body, url="github.com/ai-skills-without-borders/skills"):
    return (f'<div class="mock" aria-hidden="true"><div class="mock-bar"><i></i><i></i><i></i><span>{url}</span></div>'
            f'<div class="mock-body">{body}</div></div>')


def _field(label, value="", req=False, tall=False):
    star = '<em>*</em>' if req else ""
    return f'<div class="mf"><span>{label}{star}</span><div class="mf-in{" tall" if tall else ""}">{value}</div></div>'


def guide_html(gh):
    new_steps = [
        ("Open the form", "Click <b>Share a new skill</b>. It opens a short form on GitHub. You need a free GitHub account, nothing else.",
         _screen('<div class="m-title">Share a new skill</div><p class="m-p">Propose a skill for the library.</p><span class="m-btn hl">Share a new skill</span>', "ai-skills-without-borders.github.io")),
        ("Say who you are", "Your institution and country put you on the community map. Your name appears only if you tick the box.",
         _screen(_field("Institution", "Your medical school", True) + _field("Country", "Your country", True) + '<div class="m-check"><i>✓</i>Credit me by name</div>')),
        ("Describe the skill", "Six short parts: purpose, inputs, steps, expected output, how you know it works, and limits. Then attach a ZIP or paste the instructions.",
         _screen(_field("Purpose", "Writes exam items from objectives", True) + _field("Limitations", "Needs expert review", True) + '<div class="m-file">📎 my-skill.zip</div>')),
        ("Submit, and it's in", "A maintainer checks it and adds it to the library as a Draft, with you and your institution credited.",
         _screen('<span class="m-btn go">Submit new issue</span><div class="m-arrow">↓</div><div class="m-card"><b>Your skill</b><span class="m-chip">Draft</span></div>', "ai-skills-without-borders.github.io")),
    ]
    report_steps = [
        ("Open the skill's page", "Find the skill in the catalog and scroll to <b>Improve or adapt this skill</b>.",
         _screen('<div class="m-title">Exam Question Writer</div><div class="m-sub">Improve or adapt this skill</div><span class="m-link hl">Report how it went</span><span class="m-link">Suggest a change</span>', "ai-skills-without-borders.github.io")),
        ("Choose what to share", "<b>Report how it went</b> after using it, <b>Suggest a change</b> in plain words, or <b>Report a problem</b>.",
         _screen('<span class="m-opt hl">Usage report</span><span class="m-opt">Suggest a change</span><span class="m-opt">Problem</span><span class="m-opt">Review</span>')),
        ("Fill in a short form", "Your institution, what you asked, what worked and what didn't. About five minutes.",
         _screen(_field("Institution", "Your medical school", True) + _field("What worked", "Items matched our objectives") + _field("What didn't", "Too many options per item"))),
        ("Submit, and the skill improves", "A maintainer updates the skill, credits your institution, and your report adds to the skill's maturity.",
         _screen('<span class="m-btn go">Submit new issue</span><div class="m-arrow">↓</div><div class="m-card"><b>Exam Question Writer</b><span class="m-chip up">+1 usage report</span></div>', "ai-skills-without-borders.github.io")),
    ]

    def track(steps, cta, href):
        items = "".join(f'<li><div class="g-num">{k}</div><div class="g-text"><b>{t}</b><p>{d}</p></div>{m}</li>'
                        for k, (t, d, m) in enumerate(steps, 1))
        return f'<ol class="guide-steps">{items}</ol><p class="guide-cta"><a class="btn primary" href="{href}">{cta}</a></p>'

    return (
        '<div class="guide">'
        '<div class="guide-tabs" role="tablist" aria-label="Choose a guide">'
        '<button role="tab" id="gt-new" aria-controls="gp-new" aria-selected="true">Share a new skill</button>'
        '<button role="tab" id="gt-report" aria-controls="gp-report" aria-selected="false" tabindex="-1">Update or report on a skill</button>'
        '</div>'
        f'<div class="guide-panel" role="tabpanel" id="gp-new" aria-labelledby="gt-new">{track(new_steps, "Share a new skill", gh + "/issues/new?template=new-skill.yml")}</div>'
        f'<div class="guide-panel" role="tabpanel" id="gp-report" aria-labelledby="gt-report" hidden>{track(report_steps, "Browse the skills", "skills.html")}</div>'
        '</div>')

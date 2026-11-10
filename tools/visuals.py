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
    tools = ["Claude", "ChatGPT", "Gemini", "Copilot"]
    tiles, links = [], []
    for i, t in enumerate(tools):
        y = 22 + i * 82
        tiles.append(f'<rect x="300" y="{y}" width="146" height="58" rx="12" fill="#fff" stroke="{RULE}" stroke-width="2"/>'
                     f'<circle cx="326" cy="{y + 29}" r="9" fill="none" stroke="{TEAL}" stroke-width="2.4"/>'
                     f'<path d="m321.5 {y + 29}3 3 5-6" fill="none" stroke="{TEAL}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
                     f'<text x="345" y="{y + 35}" font-size="17" font-weight="700" fill="{NAVY}">{t}</text>')
        links.append(f'<path d="M168 176 C 236 176, 236 {y + 29}, 298 {y + 29}" fill="none" stroke="{BLUE}" stroke-width="3" '
                     f'stroke-linecap="round" stroke-dasharray="0.1 9"/>')
    doc = (f'<rect x="20" y="78" width="148" height="196" rx="12" fill="#fff" stroke="{NAVY}" stroke-width="2.5"/>'
           f'<path d="M20 90a12 12 0 0 1 12-12h124a12 12 0 0 1 12 12v22H20Z" fill="{NAVY}"/>'
           f'<text x="38" y="104" font-size="16" font-weight="700" fill="#fff">SKILL.md</text>'
           f'<rect x="38" y="130" width="88" height="10" rx="5" fill="{YELLOW}"/>'
           f'<text x="38" y="158" font-size="12" fill="#4b6178">when to use it</text>'
           f'<rect x="38" y="172" width="112" height="10" rx="5" fill="{TEAL}"/>'
           f'<text x="38" y="200" font-size="12" fill="#4b6178">the framework</text>'
           f'<rect x="38" y="214" width="100" height="10" rx="5" fill="{BLUE}"/>'
           f'<text x="38" y="242" font-size="12" fill="#4b6178">the knowledge</text>')
    return ('<svg class="hero-art" viewBox="0 0 460 352" role="img" aria-labelledby="hero-art-t">'
            '<title id="hero-art-t">One skill file works in Claude, ChatGPT, Gemini and Copilot</title>'
            f'<g font-family="Atkinson Hyperlegible, system-ui, sans-serif">{"".join(links)}{doc}{"".join(tiles)}</g></svg>')


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

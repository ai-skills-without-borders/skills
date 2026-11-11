"""
Build an editable PowerPoint version of a workshop's slides, with speaker notes.

Same slides and words as the browser version, so facilitators can translate or adapt them.
Uses python-pptx and only fonts that ship with Office (Calibri), in the site's colours.
"""
import re
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "assets" / "logo.png"

INK = RGBColor(0x22, 0x40, 0x5F)
SOFT = RGBColor(0x4B, 0x61, 0x78)
PAPER = RGBColor(0xF0, 0xF4, 0xF2)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MARKER = RGBColor(0xF4, 0xDC, 0x4A)
MARKER_SOFT = RGBColor(0xFB, 0xF0, 0xB0)
SAGE = RGBColor(0x3D, 0x96, 0x96)
RULE = RGBColor(0xD5, 0xDE, 0xDB)
FONT = "Calibri"

W, H = Inches(13.333), Inches(7.5)
MX, TOP = Inches(0.8), Inches(0.65)


def runs(s):
    """Split '**bold** rest' into (text, bold) pieces; drop links and code marks."""
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", s).replace("`", "")
    out = []
    for k, part in enumerate(re.split(r"\*\*(.+?)\*\*", s)):
        if part:
            out.append((part, k % 2 == 1))
    return out


def text(slide, x, y, w, h, content, size=20, color=INK, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space=0, name=None):
    """A text box. `content` is a string or a list of strings (one paragraph each)."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    paras = content if isinstance(content, list) else [content]
    for k, p in enumerate(paras):
        para = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        para.alignment = align
        if space and k:
            para.space_before = Pt(space)
        for t, b in runs(p):
            r = para.add_run()
            r.text = t
            r.font.size, r.font.name, r.font.bold = Pt(size), FONT, bold or b
            r.font.color.rgb = color
    return tb


def box(slide, x, y, w, h, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, name=None):
    s = slide.shapes.add_shape(shape, x, y, w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    s.line.fill.background()
    s.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = 0.08
    if name:
        s.name = name
    return s


def circle_num(slide, x, y, d, label, fill=INK, color=WHITE, size=18):
    c = box(slide, x, y, d, d, fill, MSO_SHAPE.OVAL)
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = str(label)
    r.font.size, r.font.bold, r.font.name = Pt(size), True, FONT
    r.font.color.rgb = color
    return c


def background(slide, color):
    f = slide.background.fill
    f.solid()
    f.fore_color.rgb = color


def title(slide, s, color=INK):
    text(slide, MX, TOP, W - 2 * MX, Inches(1.0), s, size=34, bold=True, color=color, name="Title")


def footer(slide, w, k, n, color=SOFT):
    text(slide, MX, H - Inches(0.55), Inches(8), Inches(0.3), w["title"], size=11, color=color)
    text(slide, W - MX - Inches(2), H - Inches(0.55), Inches(2), Inches(0.3), f"{k} / {n}", size=11, color=color, align=PP_ALIGN.RIGHT)


def body_top():
    return TOP + Inches(1.25)


def build(w, out_path, clock, segments, site):
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    blank = prs.slide_layouts[6]
    n = len(w["slides"])
    for k, s in enumerate(w["slides"], 1):
        sl = prs.slides.add_slide(blank)
        kind = s["kind"]
        pts = s.get("points", [])
        y0 = body_top() + (Inches(0.5) if len(s["title"]) > 52 and kind not in ("exercise", "title", "closing", "section") else 0)
        bw = W - 2 * MX
        bh = H - y0 - Inches(0.9) - (Inches(0.45) if s.get("link") else 0)

        if kind in ("title", "closing"):
            background(sl, INK)
            box(sl, MX, Inches(2.2), Inches(2.0), Inches(2.0), WHITE, MSO_SHAPE.OVAL)
            sl.shapes.add_picture(str(LOGO), MX + Inches(0.2), Inches(2.4), Inches(1.6), Inches(1.6))
            x = MX + Inches(2.6)
            text(sl, x, Inches(1.5), W - x - MX, Inches(0.4), "AI Skills Without Borders", size=16, bold=True, color=MARKER)
            text(sl, x, Inches(2.0), W - x - MX, Inches(1.6), s["title"], size=48 if kind == "title" else 38, bold=True, color=WHITE, anchor=MSO_ANCHOR.TOP)
            y = Inches(3.6) if kind == "title" else Inches(3.2)
            if s.get("text"):
                text(sl, x, y, W - x - MX, Inches(0.8), s["text"], size=24, color=WHITE)
            if pts:
                text(sl, x, y, W - x - MX, Inches(2.2), ["–  " + p for p in pts], size=20, color=WHITE, space=10)
            if s.get("link"):
                text(sl, x, Inches(5.9), W - x - MX, Inches(0.4), site + s["link"].replace("{ROOT}", ""), size=14, color=MARKER)
            footer(sl, w, k, n, RULE)

        elif kind == "section":
            background(sl, PAPER)
            lab = box(sl, MX, Inches(2.4), Inches(1.4), Inches(0.5), MARKER)
            text(sl, MX + Inches(0.15), Inches(2.47), Inches(1.2), Inches(0.4), s["text"], size=16, bold=True)
            text(sl, MX, Inches(3.1), bw, Inches(2.0), s["title"], size=60, bold=True)
            footer(sl, w, k, n)

        else:
            background(sl, WHITE)
            if kind != "exercise":
                title(sl, s["title"])
            if kind == "agenda":
                segs = segments(w)
                rh = min(Inches(0.62), bh / len(segs))
                for j, a in enumerate(segs):
                    y = y0 + rh * j
                    text(sl, MX, y + Inches(0.12), Inches(1.0), rh, clock(a["start"]), size=16, color=SOFT)
                    text(sl, MX + Inches(1.0), y + Inches(0.12), Inches(4.4), rh, a["title"], size=17, bold=True)
                    tx, tw = MX + Inches(5.6), bw - Inches(6.8)
                    box(sl, tx, y + Inches(0.17), tw, Inches(0.26), PAPER, MSO_SHAPE.RECTANGLE)
                    box(sl, tx + Emu(int(tw * a["start"] / w["minutes"])), y + Inches(0.17), Emu(int(tw * a["minutes"] / w["minutes"])), Inches(0.26), SAGE, MSO_SHAPE.RECTANGLE)
                    text(sl, W - MX - Inches(1.1), y + Inches(0.12), Inches(1.1), rh, f'{a["minutes"]} min', size=15, bold=True, align=PP_ALIGN.RIGHT)
            elif kind in ("steps", "checklist"):
                gap = Inches(0.14)
                rh = min(Inches(0.92), (bh - gap * (len(pts) - 1)) / len(pts))
                for j, p in enumerate(pts):
                    y = y0 + (rh + gap) * j
                    if kind == "steps":
                        box(sl, MX, y, bw, rh, PAPER)
                        circle_num(sl, MX + Inches(0.15), y + (rh - Inches(0.6)) / 2, Inches(0.6), j + 1)
                    else:
                        circle_num(sl, MX, y + (rh - Inches(0.5)) / 2, Inches(0.5), "✓", MARKER, INK, 16)
                    text(sl, MX + Inches(1.0), y, bw - Inches(1.2), rh, p, size=20, anchor=MSO_ANCHOR.MIDDLE)
            elif kind == "rules":
                cw, ch = (bw - Inches(0.3)) / 2, (bh - Inches(0.3)) / 2
                for j, p in enumerate(pts):
                    x, y = MX + (cw + Inches(0.3)) * (j % 2), y0 + (ch + Inches(0.3)) * (j // 2)
                    box(sl, x, y, cw, ch, MARKER_SOFT if j == 0 else PAPER)
                    text(sl, x + Inches(0.35), y + Inches(0.3), cw - Inches(0.7), ch - Inches(0.6), p, size=20)
            elif kind == "compare":
                cw = (bw - Inches(0.35)) / 2
                for j, (side, fill, col) in enumerate(((s["left"], PAPER, INK), (s["right"], INK, WHITE))):
                    x = MX + (cw + Inches(0.35)) * j
                    box(sl, x, y0, cw, bh, fill)
                    text(sl, x + Inches(0.4), y0 + Inches(0.35), cw - Inches(0.8), Inches(0.5), side["title"], size=22, bold=True, color=col)
                    text(sl, x + Inches(0.4), y0 + Inches(1.05), cw - Inches(0.8), bh - Inches(1.3), ["–  " + p for p in side["points"]], size=19, color=col, space=10)
            elif kind == "equation":
                p = s["parts"]
                ow = Inches(0.6)
                cw = (bw - 2 * ow) / 3
                y, ch = y0 + Inches(0.4), Inches(3.0)
                for j, part in enumerate(p):
                    x = MX + (cw + ow) * j
                    out = j == 2
                    box(sl, x, y, cw, ch, INK if out else PAPER)
                    text(sl, x + Inches(0.35), y + Inches(0.7), cw - Inches(0.7), Inches(0.6), part["title"], size=26, bold=True, color=WHITE if out else INK)
                    text(sl, x + Inches(0.35), y + Inches(1.45), cw - Inches(0.7), Inches(1.4), part["text"], size=18, color=WHITE if out else SOFT)
                    if j < 2:
                        text(sl, x + cw, y + Inches(1.1), ow, Inches(0.8), "+" if j == 0 else "=", size=40, bold=True, color=SAGE, align=PP_ALIGN.CENTER)
            elif kind == "grid":
                cards = s["cards"]
                cols = 3
                rows = (len(cards) + cols - 1) // cols
                cw, ch = (bw - Inches(0.25) * (cols - 1)) / cols, (bh - Inches(0.25) * (rows - 1)) / rows
                for j, c in enumerate(cards):
                    x, y = MX + (cw + Inches(0.25)) * (j % cols), y0 + (ch + Inches(0.25)) * (j // cols)
                    box(sl, x, y, cw, ch, MARKER_SOFT if (len(cards) == 5 and j == 4) else PAPER)
                    text(sl, x + Inches(0.3), y + Inches(0.25), cw - Inches(0.6), Inches(0.5), c["title"], size=19, bold=True)
                    text(sl, x + Inches(0.3), y + Inches(0.8), cw - Inches(0.6), ch - Inches(1.0), c["text"], size=16, color=SOFT)
            elif kind == "demo":
                lw = bw * 0.45
                text(sl, MX, y0, lw, Inches(0.5), "Watch for", size=22, bold=True)
                for j, p in enumerate(pts):
                    y = y0 + Inches(0.75) + Inches(0.8) * j
                    circle_num(sl, MX, y, Inches(0.45), "✓", MARKER, INK, 14)
                    text(sl, MX + Inches(0.7), y, lw - Inches(0.7), Inches(0.7), p, size=19, anchor=MSO_ANCHOR.MIDDLE)
                cx = MX + lw + Inches(0.5)
                cw = (W - MX - cx - Inches(0.3)) / 2
                for j, (lab, fill, col) in enumerate((("Without the skill", PAPER, INK), ("With the skill", INK, WHITE))):
                    x = cx + (cw + Inches(0.3)) * j
                    box(sl, x, y0, cw, bh, fill)
                    text(sl, x + Inches(0.25), y0 + Inches(0.25), cw - Inches(0.5), Inches(0.4), lab, size=16, bold=True, color=col)
                    lines = [None, None, None] if j == 0 else ["Which learners? Which framework?", None, "Approve this plan?", None]
                    for m, ln in enumerate(lines):
                        y = y0 + Inches(0.9) + Inches(0.75) * m
                        if ln:
                            box(sl, x + Inches(0.25), y, cw - Inches(0.5), Inches(0.6), MARKER if m == 0 else MARKER_SOFT)
                            text(sl, x + Inches(0.4), y, cw - Inches(0.8), Inches(0.6), ln, size=13, bold=True, anchor=MSO_ANCHOR.MIDDLE)
                        else:
                            box(sl, x + Inches(0.25), y + Inches(0.15), (cw - Inches(0.5)) * (0.6 if (j == 0 and m == 2) else 1), Inches(0.28), RULE if j == 0 else SOFT)
            elif kind == "exercise":
                d = Inches(2.8)
                circle_num(sl, MX, (H - d) / 2 - Inches(0.1), d, "", MARKER)
                text(sl, MX, (H - d) / 2 + Inches(0.55), d, Inches(1.2), str(s["minutes"]), size=80, bold=True, align=PP_ALIGN.CENTER)
                text(sl, MX, (H - d) / 2 + Inches(1.75), d, Inches(0.4), "minutes", size=18, bold=True, align=PP_ALIGN.CENTER)
                x = MX + d + Inches(0.7)
                box(sl, x, Inches(1.2), Inches(1.4), Inches(0.45), MARKER)
                text(sl, x + Inches(0.12), Inches(1.26), Inches(1.2), Inches(0.35), "Your turn", size=14, bold=True)
                text(sl, x, Inches(1.85), W - x - MX, Inches(0.9), s["title"], size=32, bold=True)
                for j, p in enumerate(pts):
                    y = Inches(2.95) + Inches(0.75) * j
                    circle_num(sl, x, y, Inches(0.45), j + 1, INK, WHITE, 14)
                    text(sl, x + Inches(0.7), y, W - x - MX - Inches(0.7), Inches(0.65), p, size=20, anchor=MSO_ANCHOR.MIDDLE)
            elif kind == "anatomy":
                fw = bw * 0.48
                box(sl, MX, y0, fw, bh, PAPER)
                text(sl, MX + Inches(0.3), y0 + Inches(0.2), fw, Inches(0.35), "SKILL.md", size=14, bold=True, color=SOFT)
                blocks = [("name: …\ndescription: what it does, and when", MARKER), ("## Step 1 …\n## Step 2 …", WHITE),
                          ("Stop: show the plan, wait for approval", MARKER_SOFT), ("## Output", WHITE), ("## Limitations", WHITE)]
                y = y0 + Inches(0.65)
                for b, fill in blocks:
                    hgt = Inches(0.42) * (b.count("\n") + 1) + Inches(0.12)
                    box(sl, MX + Inches(0.3), y, fw - Inches(0.6), hgt, fill)
                    text(sl, MX + Inches(0.45), y + Inches(0.06), fw - Inches(0.9), hgt, b.split("\n"), size=14, color=INK)
                    y += hgt + Inches(0.12)
                kx = MX + fw + Inches(0.6)
                for j, p in enumerate(pts):
                    yy = y0 + Inches(0.85) * j
                    circle_num(sl, kx, yy, Inches(0.5), j + 1)
                    text(sl, kx + Inches(0.75), yy, W - kx - MX - Inches(0.75), Inches(0.75), p, size=18, anchor=MSO_ANCHOR.MIDDLE)
            else:
                text(sl, MX, y0, bw, bh, ["–  " + p for p in pts], size=22, space=12)
            if s.get("link") and kind not in ("title", "closing"):
                link = s["link"].replace("{GH}", "github.com/ai-skills-without-borders/skills").replace("{ROOT}", site)
                text(sl, MX, H - Inches(1.0), bw, Inches(0.3), link.replace("https://", ""), size=12, color=SOFT)
            footer(sl, w, k, n)
        sl.notes_slide.notes_text_frame.text = re.sub(r"\*\*|`", "", s["notes"])
    prs.core_properties.title = f'{w["title"]}: workshop slides'
    prs.core_properties.author = "AI Skills Without Borders"
    prs.save(out_path)

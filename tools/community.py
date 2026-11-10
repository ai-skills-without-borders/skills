"""Community registry: load and validate community/contributors.yaml, and render the
community page (map, countries, institutions, recent contributions)."""
import datetime as dt
import html
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "community" / "contributors.yaml"
WORLD = Path(__file__).resolve().parent / "site" / "world.json"

TYPES = {
    "skill": ("New skill", "#22405f"),
    "improvement": ("Improvement", "#3d9696"),
    "variant": ("Institutional variant", "#4a86a8"),
    "usage-report": ("Usage report", "#7cc4c4"),
    "review": ("Review", "#9cc6dd"),
}


def e(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def load():
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
    return data.get("institutions") or {}, data.get("contributions") or []


def _world():
    return json.loads(WORLD.read_text(encoding="utf-8"))


def country_name(code, world=None):
    world = world or _world()
    return world["names"].get(code, code)


def validate(skill_names):
    errors = []
    try:
        insts, contribs = load()
    except Exception as ex:  # noqa: BLE001
        return [f"[community] cannot read {REGISTRY.name}: {ex}"]
    world = _world()
    for iid, i in insts.items():
        tag = f"[community] institution {iid}"
        if not re.fullmatch(r"[a-z0-9-]+", iid):
            errors.append(f"{tag}: id must be lowercase letters, digits or hyphens")
        for k in ("name", "country"):
            if not i.get(k):
                errors.append(f"{tag} missing '{k}'")
        if i.get("country") and i["country"] not in world["names"]:
            errors.append(f"{tag}: country '{i['country']}' is not an ISO 3166-1 alpha-2 code on the map")
        for k, lo, hi in (("lat", -90, 90), ("lon", -180, 180)):
            v = i.get(k)
            if not isinstance(v, (int, float)) or not lo <= v <= hi:
                errors.append(f"{tag}: '{k}' must be a number between {lo} and {hi}")
    for n, c in enumerate(contribs, 1):
        tag = f"[community] contribution {n}"
        if c.get("type") not in TYPES:
            errors.append(f"{tag}: type must be one of {sorted(TYPES)}")
        if c.get("institution") not in insts:
            errors.append(f"{tag}: institution '{c.get('institution')}' is not listed under institutions")
        d = c.get("date")
        if not isinstance(d, dt.date):
            errors.append(f"{tag}: date must be YYYY-MM-DD")
        if not c.get("skill"):
            errors.append(f"{tag}: every contribution must name the skill it is about (only contributions to skills are recorded)")
        elif c["skill"] not in skill_names:
            errors.append(f"{tag}: unknown skill '{c['skill']}'")
    return errors


def validate_cards(cards):
    """Skill cards must say where people come from: maintainers and reviewers name an
    institution, and used_at lists institution ids from the registry."""
    errors = []
    insts, _ = load()
    for c in cards:
        tag = f"[{c['name']}]"
        for k in ("maintainers", "reviewers"):
            for p in c.get(k) or []:
                if not re.search(r"\(.+\)\s*$", str(p)):
                    errors.append(f"{tag} card.yaml {k}: '{p}' must end with the institution in brackets, e.g. 'Name (Institution)'")
        for u in c.get("used_at") or []:
            if u not in insts:
                errors.append(f"{tag} card.yaml used_at: '{u}' must be an institution id from community/contributors.yaml")
    return errors


# ---------------------------------------------------------------- page parts

def _project(lat, lon, scale, translate):
    lam, phi = math.radians(lon), math.radians(lat)
    p2 = phi * phi
    p4 = p2 * p2
    x = lam * (0.8707 - 0.131979 * p2 + p4 * (-0.013791 + p4 * (0.003971 * p2 - 0.001529 * p4)))
    y = phi * (1.007226 + p2 * (0.015085 + p4 * (-0.044475 + 0.028874 * p2 - 0.005916 * p4)))
    return x * scale + translate[0], -y * scale + translate[1]


def stats():
    insts, contribs = load()
    by_country = Counter(insts[c["institution"]]["country"] for c in contribs)
    by_inst = Counter(c["institution"] for c in contribs)
    insts = {k: v for k, v in insts.items() if by_inst.get(k)}  # only institutions with skill contributions
    return insts, contribs, by_country, by_inst


def counters_html():
    insts, contribs, by_country, _ = stats()
    skills = len({c["skill"] for c in contribs if c.get("skill")})
    items = [(len(by_country), "countries"), (len(insts), "institutions"), (len(contribs), "contributions"),
             (skills, "skills with contributions")]
    return '<div class="counters">' + "".join(f'<div><b>{n}</b><span>{label}</span></div>' for n, label in items) + "</div>"


def map_svg():
    world = _world()
    insts, _, by_country, by_inst = stats()
    top = max(by_country.values() or [1]) or 1
    shapes = []
    for code, d in world["paths"].items():
        n = by_country.get(code)
        if n is None:
            shapes.append(f'<path d="{d}" class="land"/>')
        else:
            level = 1 + min(3, int(3 * n / top)) if n else 1
            name = world["names"].get(code, code)
            shapes.append(f'<path d="{d}" class="land on l{level}"><title>{e(name)}: {n} contribution{"s" if n != 1 else ""}</title></path>')
    dots = []
    for iid, i in insts.items():
        x, y = _project(i["lat"], i["lon"], world["scale"], world["translate"])
        r = 5 + min(7, by_inst[iid] ** 0.5 * 1.6)
        cls = "inst founding" if i.get("founding") else "inst"
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" class="{cls}"><title>{e(i["name"])}: {by_inst[iid]} contribution{"s" if by_inst[iid] != 1 else ""}</title></circle>')
    names = ", ".join(f'{i["name"]} ({country_name(i["country"], world)})' for i in insts.values())
    return (f'<svg class="world" viewBox="0 0 {world["width"]} {world["height"]}" role="img" aria-labelledby="world-t">'
            f'<title id="world-t">Map of contributing institutions: {e(names)}</title>'
            f'<g>{"".join(shapes)}</g><g>{"".join(dots)}</g></svg>')


def _flag(code):
    return "".join(chr(0x1F1E6 + ord(ch) - ord("A")) for ch in code.upper())


def countries_html():
    world = _world()
    insts, contribs, by_country, _ = stats()
    inst_count = Counter(i["country"] for i in insts.values())
    top = max(by_country.values() or [1]) or 1
    rows = []
    for code, n in sorted(by_country.items(), key=lambda kv: (-kv[1], country_name(kv[0], world))):
        k = inst_count[code]
        rows.append(f'<li><span class="c-name"><span class="flag" aria-hidden="true">{_flag(code)}</span>{e(country_name(code, world))}</span>'
                    f'<span class="c-bar"><span style="width:{max(2, n / top * 100):.1f}%"></span></span>'
                    f'<span class="c-n">{n} <small>{k} institution{"s" if k != 1 else ""}</small></span></li>')
    return f'<ol class="countries">{"".join(rows)}</ol>'


def institutions_html():
    world = _world()
    insts, contribs, _, by_inst = stats()
    kinds = defaultdict(Counter)
    for c in contribs:
        kinds[c["institution"]][c["type"]] += 1
    top = max(by_inst.values() or [1]) or 1
    rows = []
    for rank, (iid, n) in enumerate(sorted(by_inst.items(), key=lambda kv: (-kv[1], insts[kv[0]]["name"])), 1):
        i = insts[iid]
        segs = "".join(f'<span style="width:{m / top * 100:.2f}%;background:{TYPES[t][1]}" title="{TYPES[t][0]}: {m}"></span>'
                       for t, m in sorted(kinds[iid].items(), key=lambda kv: list(TYPES).index(kv[0])))
        badge = ""
        where = ", ".join(x for x in (i.get("city"), country_name(i["country"], world)) if x)
        rows.append(f'<li><span class="rank">{rank}</span><div class="i-main"><b>{e(i["name"])}</b>'
                    f'<span class="i-where"><span class="flag" aria-hidden="true">{_flag(i["country"])}</span>{e(where)} {badge}</span>'
                    f'<span class="i-bar">{segs}</span></div><span class="i-n">{n}</span></li>')
    legend = "".join(f'<span><i style="background:{col}"></i>{label}</span>' for label, col in TYPES.values())
    return f'<ol class="insts">{"".join(rows)}</ol><p class="type-legend">{legend}</p>'


def recent_html(titles, limit=12):
    insts, contribs, _, _ = stats()
    items = sorted(enumerate(contribs), key=lambda kc: (kc[1]["date"], kc[0]), reverse=True)[:limit]
    rows = []
    for _, c in items:
        i = insts[c["institution"]]
        what = TYPES[c["type"]][0]
        if c.get("skill"):
            head = f'<a href="skills/{e(c["skill"])}.html">{e(titles.get(c["skill"], c["skill"]))}</a>'
            if c.get("note"):
                head += f' <span class="r-sub">{e(c["note"])}</span>'
        else:
            head = e(c.get("note") or what)
        who = f'{e(c["person"])}, ' if c.get("person") else ""
        link = f' <a href="{e(c["link"])}">Details</a>' if c.get("link") else ""
        rows.append(f'<li><time datetime="{c["date"]}">{c["date"]:%d %b %Y}</time>'
                    f'<span class="r-type" style="--c:{TYPES[c["type"]][1]}">{what}</span>'
                    f'<span class="r-body"><span class="r-head">{head}{link}</span>'
                    f'<span class="r-note"><span class="flag" aria-hidden="true">{_flag(i["country"])}</span>{who}{e(i["name"])}</span></span></li>')
    return f'<ol class="recent">{"".join(rows)}</ol>'


def validate_templates():
    """Issue forms must parse, and every form must ask for institution and country."""
    errors = []
    for f in sorted((ROOT / ".github" / "ISSUE_TEMPLATE").glob("*.yml")):
        tag = f"[forms] {f.name}"
        try:
            d = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception as ex:  # noqa: BLE001
            errors.append(f"{tag} is not valid YAML: {str(ex).splitlines()[0]}")
            continue
        ids = {}
        for b in d.get("body", []):
            if b.get("id"):
                if b["id"] in ids:
                    errors.append(f"{tag} duplicate field id '{b['id']}'")
                ids[b["id"]] = b
            for k, v in (b.get("attributes") or {}).items():
                if v is None:
                    errors.append(f"{tag} field '{b.get('id')}' has an empty attribute '{k}' (an unquoted comma in a label?)")
        for need in ("institution", "country"):
            if not (ids.get(need, {}).get("validations") or {}).get("required"):
                errors.append(f"{tag} must have a required '{need}' field")
    return errors

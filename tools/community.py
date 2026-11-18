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
REPO = "ai-skills-without-borders/skills"
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


GENERIC = {"the", "of", "and", "for", "at", "in", "de", "la", "le", "du", "der", "und", "school", "medicine", "medical",
           "university", "universität", "université", "universidad", "college", "institute", "institution", "science",
           "sciences", "health", "center", "centre", "faculty", "hospital", "department", "graduate", "program",
           "national", "academy", "research", "campus", "state", "city", "foundation"}


def _words(text):
    return {w for w in re.findall(r"[^\W\d_]{3,}", (text or "").lower()) if w not in GENERIC}


def country_code(text, world=None):
    """An ISO alpha-2 code from what a contributor typed ("Israel", "USA", "uk", "IL"), or ""."""
    world = world or _world()
    t = re.sub(r"[^a-z ]", "", (text or "").lower()).strip()
    aliases = {"usa": "US", "us": "US", "united states": "US", "america": "US", "uk": "GB", "england": "GB",
               "scotland": "GB", "wales": "GB", "great britain": "GB", "britain": "GB", "korea": "KR",
               "south korea": "KR", "uae": "AE", "holland": "NL", "czech republic": "CZ", "russia": "RU"}
    if t in aliases:
        return aliases[t]
    for code, name in world["names"].items():
        if t and (t == code.lower() or t == name.lower() or t == re.sub(r"[^a-z ]", "", name.lower())):
            return code
    return ""


def match_institution(insts, name, country=""):
    """The id of the listed institution a contributor means, however they wrote its name, or None."""
    n = (name or "").strip().lower()
    if not n:
        return None
    for k, v in insts.items():
        full = v["name"].lower()
        if n in (k, full) or n in full or full in n:
            return k
    code = country_code(country) if country else ""
    mine = _words(n)
    scored = []
    for k, v in insts.items():
        if code and v.get("country") and v["country"] != code:
            continue
        shared = mine & (_words(v["name"]) | _words(k.replace("-", " ")) | {w for a in v.get("aliases") or [] for w in _words(a)})
        if shared:
            scored.append((len(shared), k))
    scored.sort(reverse=True)
    if scored and (len(scored) == 1 or scored[0][0] > scored[1][0]):
        return scored[0][1]
    return None


def _unproject(x, y, scale, translate):
    """Latitude and longitude of a point on the map (inverse of _project)."""
    xr, yr = (x - translate[0]) / scale, -(y - translate[1]) / scale
    lo, hi = -math.pi / 2, math.pi / 2
    for _ in range(60):
        phi = (lo + hi) / 2
        p2 = phi * phi; p4 = p2 * p2
        yy = phi * (1.007226 + p2 * (0.015085 + p4 * (-0.044475 + 0.028874 * p2 - 0.005916 * p4)))
        lo, hi = (phi, hi) if yy < yr else (lo, phi)
    p2 = phi * phi; p4 = p2 * p2
    lam = xr / (0.8707 - 0.131979 * p2 + p4 * (-0.013791 + p4 * (0.003971 * p2 - 0.001529 * p4)))
    return round(math.degrees(phi), 2), round(math.degrees(lam), 2)


def find_or_add_institution(name, country):
    """The id for an institution, adding it to the record (placed at its country's centre on the map) if new.
    Returns (id, added); id is "" when the country can't be recognised, so a person can help."""
    insts, _ = load()
    iid = match_institution(insts, name, country)
    if iid:
        return iid, False
    name = " ".join((name or "").split())[:150]
    world = _world()
    code = country_code(country, world)
    if not name or not code or code not in world.get("centroids", {}):
        return "", False
    lat, lon = _unproject(*world["centroids"][code], world["scale"], world["translate"])
    base = "-".join(sorted(_words(name), key=name.lower().find)[:3]) or re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:30]
    base = re.sub(r"[^a-z0-9-]+", "", base) or "institution"
    iid, n = base, 2
    while iid in insts:
        iid, n = f"{base}-{n}", n + 1
    entry = (f"  {iid}:\n    name: {json.dumps(name, ensure_ascii=False)}\n    country: {code}\n"
             f"    lat: {lat}\n    lon: {lon}\n")
    text = REGISTRY.read_text(encoding="utf-8")
    text = text.replace("\ncontributions:\n", "\n" + entry + "\ncontributions:\n", 1)
    REGISTRY.write_text(text, encoding="utf-8")
    return iid, True


def sync_skill_contributions(cards):
    """Every skill in the library is recorded as a contribution, however it arrived (issue form,
    website, pull request or a maintainer's commit). Missing ones are added from the skill's card.
    Returns the names added; raises if a skill's institution isn't in the record yet."""
    import subprocess
    insts, contribs = load()
    have = {c["skill"] for c in contribs if c.get("type") == "skill"}
    added, lines = [], []
    for c in cards:
        if c["name"] in have:
            continue
        origin = (c.get("origin_institution") or "").lower()
        inst = match_institution(insts, origin)
        if not inst:
            raise SystemExit(f"[community] skill '{c['name']}': its institution '{c.get('origin_institution')}' is not in "
                             "community/contributors.yaml; add the institution there (name, country, lat, lon).")
        date = subprocess.run(["git", "log", "--diff-filter=A", "--format=%as", "--", f"skills/{c['name']}/SKILL.md"],
                              cwd=ROOT, capture_output=True, text=True).stdout.split()
        date = date[-1] if date else __import__("datetime").date.today().isoformat()
        person = (c.get("maintainers") or [""])[0].split(" (")[0].strip()
        lines += [f"  - date: {date}", "    type: skill", f"    institution: {inst}", f"    skill: {c['name']}"]
        if person and not person.lower().startswith("contributor"):
            lines.append(f"    person: {json.dumps(person, ensure_ascii=False)}")
        lines.append(f"    link: https://github.com/{REPO}/tree/main/skills/{c['name']}")
        added.append(c["name"])
    if lines:
        with (ROOT / "community" / "contributors.yaml").open("a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
    return added


def stats():
    insts, contribs = load()
    by_country = Counter(insts[c["institution"]]["country"] for c in contribs)
    by_inst = Counter(c["institution"] for c in contribs)
    insts = {k: v for k, v in insts.items() if by_inst.get(k)}  # only institutions with skill contributions
    return insts, contribs, by_country, by_inst


def counters_html(n_skills=None):
    insts, contribs, by_country, _ = stats()
    skills = n_skills if n_skills is not None else len({c["skill"] for c in contribs if c.get("skill")})
    items = [(len(by_country), "countries"), (len(insts), "institutions"), (len(contribs), "contributions"),
             (skills, "skills in the library")]
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
        if f.name == "config.yml":
            continue
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


def feed_xml(titles, site_url, library_name):
    """Atom feed of contributions to skills, newest first, for anyone who wants to follow the library."""
    from xml.sax.saxutils import escape as x
    insts, contribs, _, _ = stats()
    items = sorted(enumerate(contribs), key=lambda kc: (kc[1]["date"], kc[0]), reverse=True)[:50]
    updated = f'{items[0][1]["date"]}T00:00:00Z' if items else "2026-01-01T00:00:00Z"
    entries = []
    for k, c in items:
        i = insts.get(c["institution"], {"name": c["institution"]})
        skill = titles.get(c["skill"], c["skill"])
        what = TYPES[c["type"]][0]
        title = f"{what}: {skill}" if c["type"] == "skill" else f"{what} of {skill}"
        who = f'{c["person"]}, ' if c.get("person") else ""
        url = f'{site_url}skills/{c["skill"]}.html'
        summary = f'{who}{i["name"]}.' + (f' {c["note"]}' if c.get("note") else "")
        entries.append(f'<entry><id>{x(url)}#{c["date"]}-{k}</id><title>{x(title)}</title>'
                       f'<link href="{x(url)}"/><updated>{c["date"]}T00:00:00Z</updated>'
                       f'<summary>{x(summary)}</summary></entry>')
    return ('<?xml version="1.0" encoding="utf-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom">'
            f'<id>{x(site_url)}feed.xml</id><title>{x(library_name)}: new skills and contributions</title>'
            f'<link href="{x(site_url)}feed.xml" rel="self"/><link href="{x(site_url)}community.html"/>'
            f'<updated>{updated}</updated>{"".join(entries)}</feed>\n')

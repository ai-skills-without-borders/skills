"""Principles registry: load and validate guide/principles.yaml, and generate
the principle list in guide/pedagogy.md and the gap report guide/principle-gaps.md."""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "guide" / "principles.yaml"
PEDAGOGY_MD = ROOT / "guide" / "pedagogy.md"
GAPS_MD = ROOT / "guide" / "principle-gaps.md"

LAYERS = {
    "science": ("Overarching principles of science teaching",
                "Shared by biomedical research, PhD and pre-clinical teaching. Most come from the learning sciences or general STEM education, so each also needs evidence from health-professions education."),
    "medicine": ("Principles specific to medical education",
                 "Principles with no direct counterpart in general science teaching, from health-professions education research and standards."),
    "ai": ("Teaching in the AI era",
           "Principles for teaching with AI, across both layers above."),
}
ROLES = {"origin", "science-ed", "med-ed", "standard"}
POPULATIONS = {"lab", "school", "stem-ug", "higher-ed", "health-professions", "standard"}
BASIS = {"research", "standard", "practice"}
POP_LABEL = {"lab": "laboratory studies", "school": "school students", "stem-ug": "undergraduate STEM",
             "higher-ed": "higher education", "health-professions": "health-professions learners", "standard": "professional standard"}
SPECIAL_APPLIES = {"all", "library"}


def load():
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    sources = data["sources"]
    principles = []
    for p in data["principles"]:
        refs = []
        for item in p.get("sources", []):
            sid, _, role = item.partition(":")
            refs.append({"id": sid, "role": role, **sources.get(sid, {})})
        principles.append({**p, "refs": refs, "applies": p.get("applies") or {}})
    return sources, principles


def has_medical_evidence(p):
    """True when a health-professions study or a medical-education standard backs the principle."""
    return any(is_medical(r) and not r.get("context_only") for r in p["refs"])


def is_medical(r):
    return r.get("population") == "health-professions" or bool(r.get("medical"))


def skills_of(p, skill_names):
    a = p["applies"]
    if "all" in a:
        return list(skill_names)
    return [s for s in a if s not in SPECIAL_APPLIES]


def validate(skill_names):
    errors = []
    try:
        sources, principles = load()
    except Exception as ex:  # noqa: BLE001
        return [f"[principles] cannot read {REGISTRY.name}: {ex}"]
    for sid, s in sources.items():
        for k in ("cite", "short", "population", "design", "transfer"):
            if not s.get(k):
                errors.append(f"[principles] source {sid} missing '{k}'")
        if s.get("population") not in POPULATIONS:
            errors.append(f"[principles] source {sid} population must be one of {sorted(POPULATIONS)}")
    used = set()
    ids = set()
    for p in principles:
        tag = f"[principles] {p.get('id')}"
        if p.get("id") in ids:
            errors.append(f"{tag} duplicate id")
        ids.add(p.get("id"))
        for k in ("id", "name", "layer", "basis", "summary"):
            if not p.get(k):
                errors.append(f"{tag} missing '{k}'")
        if p.get("layer") not in LAYERS:
            errors.append(f"{tag} layer must be one of {sorted(LAYERS)}")
        if p.get("basis") not in BASIS:
            errors.append(f"{tag} basis must be one of {sorted(BASIS)}")
        if not any(r["role"] == "origin" for r in p["refs"]):
            errors.append(f"{tag} needs an origin source")
        for r in p["refs"]:
            used.add(r["id"])
            if r["id"] not in sources:
                errors.append(f"{tag} cites unknown source '{r['id']}'")
            if r["role"] not in ROLES:
                errors.append(f"{tag} source {r['id']} role must be one of {sorted(ROLES)}")
        for s in p["applies"]:
            if s not in SPECIAL_APPLIES and s not in skill_names:
                errors.append(f"{tag} applies to unknown skill '{s}'")
    for sid in sources:
        if sid not in used:
            errors.append(f"[principles] source {sid} is not cited by any principle")
    return errors


# ---------------------------------------------------------------- generated Markdown

def _link(r):
    if r.get("doi"):
        return f" https://doi.org/{r['doi']}"
    if r.get("url"):
        return f" {r['url']}"
    return ""


def _evidence_line(p):
    if has_medical_evidence(p):
        return ""
    return "\n> **Evidence from general education only.** The registry has no health-professions source for this principle yet. Treat it as a well-supported hypothesis for medical learners, and report what you see.\n"


def pedagogy_section(skill_names):
    """The principle list for guide/pedagogy.md, grouped by layer, with two tiers of sources."""
    _, principles = load()
    out, n = [], 0
    basis_label = {"research": "Research", "standard": "Standard", "practice": "Practice"}
    for layer, (title, intro) in LAYERS.items():
        out += [f"## {title}", "", intro, ""]
        for p in [p for p in principles if p["layer"] == layer]:
            n += 1
            out += [f"### {n}. {p['name']} — *{basis_label[p['basis']]}*", "", p["summary"], ""]
            general = [r for r in p["refs"] if not is_medical(r)]
            medical = [r for r in p["refs"] if is_medical(r)]
            out.append("**Sources**")
            for r in general:
                out.append(f"- {r['short']} ({r['role']}; {POP_LABEL[r['population']]}, {r['design']}). {r['transfer']}")
            for r in medical:
                out.append(f"- *Medical education:* {r['short']} ({r['design']}). {r['transfer']}")
            out.append(_evidence_line(p))
            if p["applies"]:
                out += ["**Where it appears**"]
                for s, how in p["applies"].items():
                    who = {"all": "Every skill", "library": "The library"}.get(s, f"`{s}`")
                    out.append(f"- {who}: {how}")
                out.append("")
            else:
                out += ["**Where it appears:** no skill yet. A candidate for a new skill or an addition to an existing one.", ""]
            if p.get("practice_note"):
                out += [f"*Practice:* {p['practice_note']}", ""]
            if p.get("limits"):
                out += [f"**Limit:** {p['limits']}", ""]
    return "\n".join(out).strip()


def references_section():
    sources, _ = load()
    items = sorted(sources.values(), key=lambda s: s["cite"].lower())
    return "## References\n\n" + "\n".join(f"- {s['cite']}{_link(s)}" for s in items)


def write_pedagogy(skill_names):
    text = PEDAGOGY_MD.read_text(encoding="utf-8")
    for tag, body in (("PRINCIPLES", pedagogy_section(skill_names)), ("REFERENCES", references_section())):
        text = re.sub(rf"<!-- {tag}:START -->.*?<!-- {tag}:END -->",
                      f"<!-- {tag}:START -->\n{body}\n<!-- {tag}:END -->", text, flags=re.S)
    PEDAGOGY_MD.write_text(text, encoding="utf-8")


def write_gaps(skill_names):
    _, principles = load()
    no_med = [p for p in principles if not has_medical_evidence(p)]
    no_skill = [p for p in principles if not skills_of(p, skill_names) and "library" not in p["applies"]]
    one_source = [p for p in principles if len(p["refs"]) == 1]
    covered = {s for p in principles for s in skills_of(p, skill_names)}
    orphan_skills = [s for s in skill_names if s not in covered]
    count = {s: sum(s in skills_of(p, skill_names) for p in principles) for s in skill_names}

    lines = [
        "# Principle gap report",
        "",
        "Generated from `guide/principles.yaml` by `tools/build.py`. Do not edit by hand.",
        "",
        "This report shows where the library's pedagogy is thin, so reviewers know where to look first.",
        "",
        f"**{len(principles)} principles** in three layers; "
        f"**{len(principles) - len(no_med)}** have evidence from health-professions education.",
        "",
        "## 1. Principles with evidence from general education only",
        "",
        "The registry has no health-professions source for these yet. Each needs one: a study such as an RCT, a meta-analysis or a BEME review, or a medical-education standard. Suggest one in an issue.",
        "",
    ]
    lines += [f"- **{p['name']}** ({p['layer']}): {', '.join(r['short'] for r in p['refs'])}" for p in no_med] or ["- None."]
    lines += ["", "## 2. Principles that no skill applies yet", "",
              "Candidates for a new skill, or an addition to an existing one.", ""]
    lines += [f"- **{p['name']}** ({p['layer']}). {p['summary']}" for p in no_skill] or ["- None."]
    lines += ["", "## 3. Principles resting on a single source", ""]
    lines += [f"- **{p['name']}**: {p['refs'][0]['short']}" for p in one_source] or ["- None."]
    lines += ["", "## 4. Skills with no principle mapped", ""]
    lines += [f"- `{s}`" for s in orphan_skills] or ["- None. Every skill applies at least one principle."]
    lines += ["", "## Principles per skill", "", "| Skill | Principles |", "|---|---|"]
    lines += [f"| `{s}` | {count[s]} |" for s in skill_names]
    lines += ["", "## Evidence by layer", "", "| Layer | Principles | With medical-education evidence |", "|---|---|---|"]
    for layer, (title, _) in LAYERS.items():
        ps = [p for p in principles if p["layer"] == layer]
        lines.append(f"| {title} | {len(ps)} | {sum(has_medical_evidence(p) for p in ps)} |")
    GAPS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

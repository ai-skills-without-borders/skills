# Clinical Integration Task Generator — paste-in version

From the AI Skills Without Borders library, v0.1.0 (CC-BY-4.0). Source: https://github.com/ai-skills-without-borders/skills/tree/main/skills/clinical-integration-notebooks

How to use: paste the **Instructions** section into the instructions of a custom GPT, Gem or Project (or at the start of a chat). Add the **Reference files** as knowledge files, or paste them too if there is room. Where the instructions mention a file such as `references/x.md`, it is included below under that name.

---

## Instructions

Use this when: Builds clinical integration sessions for a methods-based course. For each integration task date, it finds a recent NEJM clinical case (MGH Case Records, or Clinical Problem-Solving if needed). The case has to fit methods students have already learned, including at least one taught since the previous task. It then writes a student-facing session notebook and an instructor key.  Students don't diagnose the patient. Working in small teams, they choose course methods and combine them into a plan a physician-scientist could use to investigate the disease mechanism. Selected students then present one method each in a chalk talk and answer questions.  Use it when you teach methods in separate sessions (lab techniques, omics, imaging, data analysis) and want recurring sessions where students apply them together to a real patient. This works best in preclinical, MD-PhD or biomedical graduate courses. It is also useful when you need a fresh case each year without the hours of searching for one.

# Clinical Integration Task Generator

**Input:** a course's assignments (zip of notebooks, slides, or a methods book) and the **dates of its clinical integration tasks**.
**Output:** for each task, a recent **NEJM** clinical case that fits the methods taught so far, a **student page (.html)** that runs the session, and an **instructor key (.html)**. Pages are self-contained (inline styles, embedded logo): they open in any browser, upload to Moodle or any LMS, and print to PDF.

The skill works for any school. Everything school-specific (course name, session timing, language, logo, labels) lives in a **course profile** (`profile.json`). The pedagogy, rules and scripts are shared. Developed for the CMBC course at the Weizmann Gutwirth MD-PhD School, which ships as a preset.

## Pedagogy (why the task looks like this)
Keep these principles when you pick cases, write handouts or adapt the format for another school. Each design choice serves one of them.

1. **Integration.** Methods are usually taught one session at a time. The task makes students combine several of them on one real problem. Each task must draw on recently taught methods (retrieval while they're fresh) and on earlier ones (spaced, cumulative practice). The final task covers as much of the course as possible.
2. **Authentic context, physician-scientist identity.** A real NEJM case shows why the methods matter at the bedside. Students don't **diagnose**; they ask *what mechanism could explain this, and how would I test it?* That keeps preclinical students on mechanisms and methods rather than clinical knowledge they don't have yet.
3. **Productive ambiguity.** The handout hides the diagnosis and doesn't say which methods to use. Students must choose, and more than one good plan exists. Never give the answer away in the handout or the focus hint.
4. **Team work.** Groups of 2-3 read, choose methods and build one shared investigation plan. Each group has to agree on distinct methods so that presentations don't overlap. That's the interdependence. Groups also help their presenters rehearse, which makes the presentation a team product.
5. **Individual accountability.** Presenters are selected, so everyone must be ready to present any part of the plan.
6. **Presentation and defense.** A short chalk talk on one method (principle, why it fits, expected results, limits), followed by Q&A. Students practise explaining a method clearly and defending a choice under questions. This is peer teaching for the rest of the class.
7. **Aligned assessment.** The rubric scores the same things the task trains: method accuracy and relevance, integration and reflection, communication and defense.
8. **Instructor as facilitator.** During group work the instructor circulates and asks questions rather than giving answers. The instructor key (diagnosis, matched methods, justification) supports the Q&A and an optional closing debrief where the diagnosis is revealed and linked back to the methods.

When a school changes the format (timing, group size, number of presenters), keep every element: individual reading, group method selection, group integration, rehearsal, selected presentations with Q&A.

## 0. Course profile
If the user gives a saved `profile.json` or names the **CMBC preset** (below), use it. Otherwise, build one. Read what you can from the materials first, then ask only for what's still missing (at most 4 questions per round). If the user is away, use the defaults and list them at the top of the reply.

| Key | What it controls | Default |
|---|---|---|
| `course_name` | Name in student text ("the methods learned in ...") | `the course` |
| `materials_name` | What students select methods from | `course methods materials` |
| `learner_role` | Who investigates the case | `physician-scientist` |
| `task_label` | Schedule text before the task number | `integration task` |
| `task_title`, `file_prefix` | Page title and file names | `Integration Task`, `Integration_` |
| `extra_non_method` | Regex for more non-method schedule rows | none |
| `case_source` | Case series named on the page | NEJM Case Records of the MGH |
| `learning_goals` | Goals shown to students (integration, reasoning, team work, communication) | generic versions in the script |
| `group_size`, `group_steps` | Group-work phase: `[{minutes,title,text}]` | 2-3; 20/70/30/30 min |
| `presenters`, `talk_min`, `qa_min`, `total_min` | Presentation phase and total | 5, 7, 5, 210 |
| `min_methods`, `min_new_methods` | Matching thresholds | 2, 1 |
| `discussion_questions`, `presentation_points`, `evaluation` | Rubric text | generic versions in the script |
| `logo_path`, `logo_base_dir` | Logo file; embedded in the page if found at build time, otherwise linked (null = no logo) | null, cwd |
| `language`, `rtl`, `labels` | Page language, right-to-left (Hebrew, Arabic), translated UI strings | `en`, false, English |

Profile strings may use `{materials_name}`, `{presenters}`, `{talk_min}`, `{qa_min}`, `{course_name}`, `{learner_role}`, `{group_size}`, `{case_source}`.

The builder **asserts** that `sum(group_steps) + presenters x (talk_min + qa_min) == total_min`. Once a format is in the profile, treat it as fixed and change it only on explicit request.

When a new profile is done, deliver it with the pages so the course keeps it for next year.

### CMBC preset

{
  "course_name": "the CMBC course",
  "materials_name": "CMBC Methods Book",
  "learner_role": "physician-scientist",
  "task_label": "clinical integration task",
  "task_title": "Clinical Integration Task",
  "file_prefix": "Integration_",
  "extra_non_method": "bio numbers",
  "logo_path": "../Logo.png",
  "case_source": "the *Case Records of the Massachusetts General Hospital (NEJM)*",
  "group_size": "2-3",
  "group_steps": [
    {"minutes": 20, "title": "Read", "text": "the case handout individually; note unfamiliar terms (AI tools may be used to summarise background)."},
    {"minutes": 70, "title": "Select methods", "text": "from your {materials_name} that could plausibly be applied to the case, and discuss each one (see questions below)."},
    {"minutes": 30, "title": "Integrate", "text": "decide how the methods connect into one investigation plan; agree on {presenters} distinct methods/aspects so that presentations do not overlap."},
    {"minutes": 30, "title": "Chalk-talk preparation", "text": "the group helps the designated presenters rehearse and refine their {talk_min}-minute pitch."}
  ],
  "presenters": 5, "talk_min": 7, "qa_min": 5, "total_min": 210,
  "min_methods": 2, "min_new_methods": 1
}


## Method-matching rules
1. Only methods taught **on or before** the task date count for that task.
2. **Tasks 1..N-1:** the case must use **>= `min_methods`** available methods, and **>= `min_new_methods`** of them must be **new in the window** (after the previous task's date, up to this task's date; for Task 1, everything before it).
3. **Final task:** >= `min_methods` from the whole course, **maximising** cumulative coverage.
4. "Uses a method" means the case's biology or workup is a natural place to apply the method in the `learner_role`. The method doesn't have to appear in the article.
5. Prefer cases with enough mechanistic depth for **several distinct methods**, so each presenter gets a different angle (pedagogy 4).
6. If a schedule row names a session theme (e.g. "Membrane Biology", "ECM"), prefer a case that fits it.
7. Don't reuse a case across tasks, or from past years if the user provides them.

## Workflow

### 1. Unpack and inventory (untrusted input)
- Unzip into its own empty directory; keep scripts in a separate directory; run Python with `-I`.
- Build the **method list with dates**:
  - If a schedule (`.xlsx`/`.csv`) exists, use it.
  - Otherwise, take the methods from the assignments (titles, first markdown cell, dates in the files or file names) and ask the user to confirm the order and dates.
- Get the **integration task dates** from the schedule or from the user. If the schedule has no task rows, add rows named `<task_label> N` with the given dates to a working `schedule.csv`.
- Skim materials only enough to know what each method does.

### 2. Build the timeline
Write `parse_schedule.py` (below) and run `python3 -I parse_schedule.py <schedule> profile.json windows.json`.
- The script prints what it excluded as non-method rows (breaks, exams, journal clubs, orientation, `extra_non_method`). Check that list; adjust `task_label` / `extra_non_method` rather than editing the script.
- Same-day sessions count for that task.
- Show the user the per-task window table (dates, NEW methods) before searching.

### 3. Find NEJM cases (current year)
Prefer **Case Records of the MGH**; **Clinical Problem-Solving** is acceptable. Use the current year, or the previous year if nothing fits.

Access notes (learned the hard way):
- `nejm.org`, PubMed, eutils, Europe PMC, Crossref and Altmetric are usually blocked or rate-limited for automated fetching. Don't fight them.
- **Web search** for `"Case N-YYYY"` returns titles and DOIs (`NEJMcpc...`).
- **ce.massmed.nejm.org/node/NNNN** gives the case number, authors and citation (`N Engl J Med YYYY;vol:pages`).
- **clinician.nejm.org** gives case summaries with the **final diagnosis**. Weekly edition pages are `https://clinician.nejm.org/edition/YYYY-MM-DD` (Mondays) and list "Case Study" links.
- Page fetches often return HTTP 429. Fetch one page at a time, wait about 70 s after a 429, and give a long catalog walk to a subagent if one is available.
- Never invent a DOI, author or diagnosis. If a DOI isn't verified, link the CE or clinician page instead.

Shortlist cases whose diagnosis connects to each window's NEW methods, then apply the rules. Record the diagnosis, key findings and citation.

### 4. Write each handout (student-facing)
- One short paragraph in lay language and in your own words (don't copy the article's text): age/sex, presenting symptoms, key exam/lab/imaging/biopsy findings, and treatment if useful.
- **Do not reveal the diagnosis** or name the disease or gene. Don't list which course methods to use (pedagogy 3).
- Write in the course's language. For RTL courses, set `language` and `rtl: true`, and translate `labels`.
- Optional `focus_hint` (one sentence) steering toward the session theme or the new methods without naming them as the answer.

### 5. Generate the pages
Write one spec JSON per task (keys in the script docstring). Make sure the `markdown` package is installed (`pip install markdown`, add `--break-system-packages` if pip refuses), then run:
`python3 -I build_integration_html.py profile.json spec_tN.json out/`
This writes `<file_prefix>N.html` and `<file_prefix>N_instructor_key.html`.
- The student page contains: learning goals, case background, handout, schedule at a glance, group steps with discussion questions, presentation requirements and evaluation criteria.
- The key holds the article, citation, diagnosis, methods with dates and NEW flags, how each method applies, and the justification. Add 2-3 suggested Q&A questions and a debrief note to the key's `summary` (pedagogy 8).
- `last_modified` defaults to today in D.M.YYYY. If the logo isn't found at build time, the page links to `logo_path` instead, so keep the page next to the logo when distributing.

### 6. Check and deliver
- Open one page in a browser (or render a screenshot) to eyeball the layout, tables and logo; for RTL courses, check that the text runs right-to-left.
- Check each handout against pedagogy 3: no diagnosis, disease or gene name, no method list.
- Check the reference link opens the right case.
- Deliver the pages, keys and (if new) `profile.json` as files. In the reply, give a compact per-task table: date, window, case, matched methods with dates, and NEW flag. Remind the user that the key is for instructors only.

## parse_schedule.py

"""Parse a course schedule (.xlsx/.csv) and print the method windows for each integration task.

Usage: python3 -I parse_schedule.py <schedule.xlsx|.csv> [profile.json] [out.json]
Assumes one row per session with a name column and a date column (header row detected
by looking for cells containing 'name'/'session'/'topic' and 'date'). Rows whose name matches
the profile's task_label (default 'integration task') followed by a number are tasks;
non-method rows (holidays, exams, journal clubs, opening day, plus the profile's
extra_non_method regex) are excluded from the method list.
"""
import csv, datetime as dt, json, re, sys

BASE_NON_METHOD = (r"holiday|vacation|break|election|opening day|orientation|longitudinal|^jc\b|journal club|"
                   r"experiment(al)? planning|^test\b|exam|quiz|review session|feedback")


def rows_from(path):
    if path.lower().endswith(".csv"):
        with open(path, newline="", encoding="utf-8-sig") as f:
            return [list(r) for r in csv.reader(f)]
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    out = []
    for ws in wb:
        out += [list(r) for r in ws.iter_rows(values_only=True)]
    return out


def to_date(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    if isinstance(v, str):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y", "%m/%d/%Y", "%d/%m/%y", "%d-%m-%Y", "%d %B %Y", "%d %b %Y"):
            try:
                return dt.datetime.strptime(v.strip(), fmt).date()
            except ValueError:
                pass
    return None


def main(path, profile_path=None, out=None):
    prof = json.load(open(profile_path, encoding="utf-8")) if profile_path else {}
    label = prof.get("task_label", "integration task")
    task_re = re.compile(re.escape(label).replace(r"\ ", r"\s+") + r"\s*(\d+)", re.I)
    extra = prof.get("extra_non_method")
    non_method = re.compile(BASE_NON_METHOD + (f"|{extra}" if extra else ""), re.I)

    rows = rows_from(path)
    name_i = date_i = None
    for r in rows:
        low = [str(c).lower() if c is not None else "" for c in r]
        ni = next((i for i, c in enumerate(low) if any(k in c for k in ("name", "session", "topic", "title"))), None)
        di = next((i for i, c in enumerate(low) if "date" in c), None)
        if ni is not None and di is not None:
            name_i, date_i = ni, di
            break
    if name_i is None:
        name_i, date_i = 0, 1
    sessions = []
    for r in rows:
        if len(r) <= max(name_i, date_i):
            continue
        name, d = r[name_i], to_date(r[date_i])
        if not name or not d:
            continue
        sessions.append({"name": str(name).strip(), "date": d})
    sessions.sort(key=lambda s: s["date"])
    tasks = sorted((int(task_re.search(s["name"]).group(1)), s) for s in sessions if task_re.search(s["name"]))
    if not tasks:
        sys.exit(f"No rows match task label '{label} N'. Set task_label in the profile.")
    methods = [s for s in sessions if not task_re.search(s["name"]) and not non_method.search(s["name"])]
    result, prev = [], None
    for n, t in tasks:
        upto = [m for m in methods if m["date"] <= t["date"]]
        new = [m for m in upto if prev is None or m["date"] > prev]
        result.append({
            "task": n, "date": t["date"].isoformat(), "row_label": t["name"],
            "previous_task_date": prev.isoformat() if prev else None,
            "methods_available": [{"name": m["name"], "date": m["date"].isoformat()} for m in upto],
            "methods_new_in_window": [{"name": m["name"], "date": m["date"].isoformat()} for m in new],
        })
        prev = t["date"]
    for t in result:
        print(f"\n=== Task {t['task']} — {t['date']} ({t['row_label']})")
        print(f"  window: after {t['previous_task_date'] or 'course start'} up to {t['date']}")
        for m in t["methods_available"]:
            flag = "NEW" if m in t["methods_new_in_window"] else "   "
            print(f"  {flag} {m['date']}  {m['name']}")
    excluded = [s["name"] for s in sessions if non_method.search(s["name"]) and not task_re.search(s["name"])]
    if excluded:
        print("\nExcluded as non-method rows (check these):", "; ".join(excluded))
    if out:
        json.dump(result, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"\nwrote {out}")


if __name__ == "__main__":
    main(*sys.argv[1:])


## build_integration_html.py

"""Build one integration-task page (.html) plus optional instructor key (.html) from a profile and a task spec.

Usage: python3 -I build_integration_html.py <profile.json> <spec.json> <out_dir>
Needs the `markdown` package (pip install markdown). Output pages are self-contained:
CSS is inline and a local logo file is embedded as base64.

Profile keys (course-level, reused for every task; all optional, defaults shown in DEFAULTS):
  course_name, institution, materials_name, learner_role, task_title, file_prefix, logo_path,
  case_source, learning_goals [str], group_size, group_steps [{minutes,title,text}], presenters, talk_min, qa_min,
  total_min, discussion_questions [str], presentation_points [str], evaluation [[title, text]],
  language (html lang, default en), rtl (bool, right-to-left page for Hebrew/Arabic),
  logo_base_dir (where a relative logo_path is found at build time; default cwd),
  labels {dict of UI strings to translate; see DEFAULTS["labels"]}.
  Strings may use {materials_name}, {presenters}, {talk_min}, {qa_min}, {course_name}, {learner_role}.
Spec keys (per task):
  task_number (int), task_date ("YYYY-MM-DD"), last_modified ("D.M.YYYY", optional -> today),
  handout (markdown, lay description, NO diagnosis), reference_url, reference_label,
  focus_hint (optional), instructor_key (optional dict ->
     {article, citation, diagnosis, summary, methods:[{name,date,new:bool,use}], justification}).
Timing: group steps + presenters*(talk+qa) must equal total_min (asserted).
"""
import base64, datetime as dt, html, json, mimetypes, os, sys

import markdown

DEFAULTS = {
    "course_name": "the course", "institution": "", "materials_name": "course methods materials",
    "learner_role": "physician-scientist", "task_title": "Integration Task", "file_prefix": "Integration_",
    "logo_path": None, "case_source": "the *Case Records of the Massachusetts General Hospital (NEJM)*", "group_size": "2-3",
    "learning_goals": [
        "**Integrate** methods learned in separate sessions into one coherent investigation of a real patient.",
        "**Reason as a {learner_role}:** turn clinical findings into mechanistic questions and choose methods that answer them.",
        "**Work as a team:** divide the problem, negotiate one shared plan, and help each other prepare.",
        "**Communicate and defend** a method choice clearly to peers, including its limits."],
    "group_steps": [
        {"minutes": 20, "title": "Read", "text": "the case handout individually; note unfamiliar terms."},
        {"minutes": 70, "title": "Select methods", "text": "from the {materials_name} that could plausibly be applied to the case, and discuss each one (see questions below)."},
        {"minutes": 30, "title": "Integrate", "text": "decide how the methods connect into one investigation plan; agree on {presenters} distinct methods/aspects so that presentations do not overlap."},
        {"minutes": 30, "title": "Presentation preparation", "text": "help the designated presenters rehearse their {talk_min}-minute pitch."}],
    "presenters": 5, "talk_min": 7, "qa_min": 5, "total_min": 210,
    "discussion_questions": [
        "The **biological/clinical question** it addresses in this case.",
        "The **data in / data out** for the method.",
        "**Strengths and limitations** of using this method here.",
        "How this method could be **combined with other methods** for deeper insight."],
    "presentation_points": ["The **principle of the method**.", "Why it is appropriate for the case.",
                            "What type of **results** it would produce.", "Any **assumptions, trade-offs, or limitations**."],
    "evaluation": [
        ["Method Accuracy & Relevance", "Correct use of the chosen method, clearly linked to the case."],
        ["Integration & Reflection", "Awareness of connections to other methods; strengths, limitations, assumptions."],
        ["Communication & Defense", "Clarity of presentation and ability to respond to questions."]],
    "rtl": False,
    "labels": {
        "instructions": "Instructions", "date": "Date", "total_time": "Total time",
        "background": "Case Background", "handout": "Case Handout", "your_task": "Your task",
        "focus": "Session focus", "no_need": "No need to read the full paper. Case inspired by:",
        "reference": "Reference", "at_a_glance": "Schedule at a glance", "time": "Time", "activity": "Activity",
        "what_to_do": "What to do", "step1": "Step 1 - Small-group reading & preparation",
        "step2": "Step 2 - Presentations + Q&A", "in_groups": "In groups of {group_size} students:",
        "for_each": "For each method, discuss:", "presenters_line": "**{presenters} students** will be selected to present to the entire class, each focusing on **one method/aspect**.",
        "must_cover": "Each presentation must cover:", "evaluation": "Evaluation Criteria",
        "assessed": "Your performance will be assessed based on:",
        "background_text": "You will be provided with a clinical case from {case_source}. The case describes a patient's clinical findings and suspected disease process.\n\nYour task is not to *diagnose* the patient (you might not even be familiar with some of the terms), but to use the methods you have learned in {course_name} to propose how a **{learner_role}** could investigate the biological mechanisms underlying the case.",
        "task_text": "Using the methods learned so far in {course_name}, outline how to investigate the mechanisms behind this case; focus on method choice, data in/out, strengths/limits, and how methods integrate.",
        "key_title": "Instructor key (do not distribute)", "goals": "Learning goals"},
}


CSS = """
body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;max-width:860px;margin:2rem auto;padding:0 1.25rem;line-height:1.55;color:#1f2328}
h1{font-size:1.7rem;border-bottom:2px solid #d0d7de;padding-bottom:.3rem}h2{font-size:1.3rem;margin-top:2rem}h4{font-size:1.05rem}
table{border-collapse:collapse;width:100%;margin:1rem 0}th,td{border:1px solid #d0d7de;padding:.45rem .6rem;text-align:start;vertical-align:top}th{background:#f6f8fa}
blockquote{border-inline-start:4px solid #d0d7de;margin:1rem 0;padding:.2rem 1rem;color:#57606a}
img.logo{max-height:80px}.meta{color:#57606a;font-size:.9rem}hr{border:0;border-top:1px solid #d0d7de;margin:2rem 0}
@media print{body{margin:0;max-width:none}a{color:inherit}}
"""


def page(title, body_md, lang="en", rtl=False, logo_html=""):
    body = markdown.markdown(body_md, extensions=["tables", "sane_lists"])
    d = ' dir="rtl"' if rtl else ""
    return (f'<!DOCTYPE html>\n<html lang="{lang}"{d}>\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{html.escape(title)}</title>\n'
            f'<style>{CSS}</style>\n</head>\n<body>\n{logo_html}{body}\n</body>\n</html>\n')


def logo_tag(path, base_dir):
    if not path:
        return ""
    local = path if os.path.isabs(path) else os.path.join(base_dir, path)
    if os.path.isfile(local):
        mime = mimetypes.guess_type(local)[0] or "image/png"
        data = base64.b64encode(open(local, "rb").read()).decode()
        return f'<img class="logo" alt="Logo" src="data:{mime};base64,{data}">\n'
    return f'<img class="logo" alt="Logo" src="{html.escape(path)}">\n'


def hm(minutes):
    h, m = divmod(minutes, 60)
    return f"{h}:{m:02d}"


def dur(minutes):
    h, m = divmod(minutes, 60)
    return " ".join(p for p in (f"{h} h" if h else "", f"{m} min" if m else "") if p)


def build(profile, spec, out_dir):
    p = {**DEFAULTS, **profile, "labels": {**DEFAULTS["labels"], **profile.get("labels", {})}}
    L = p["labels"]
    fmt = dict(materials_name=p["materials_name"], presenters=p["presenters"], talk_min=p["talk_min"],
               qa_min=p["qa_min"], course_name=p["course_name"], learner_role=p["learner_role"],
               group_size=p["group_size"], case_source=p["case_source"])
    f = lambda s: s.format(**fmt)

    group_min = sum(s["minutes"] for s in p["group_steps"])
    pres_min = p["presenters"] * (p["talk_min"] + p["qa_min"])
    assert group_min + pres_min == p["total_min"], (
        f"timing mismatch: group {group_min} + presentations {pres_min} != total {p['total_min']}")

    n = spec["task_number"]
    today = dt.date.today()
    lm = spec.get("last_modified") or f"{today.day}.{today.month}.{today.year}"
    task_date = dt.date.fromisoformat(spec["task_date"]).strftime("%A, %d %B %Y")
    focus = f"\n\n*{L['focus']}:* {spec['focus_hint']}" if spec.get("focus_hint") else ""
    title = p["task_title"]
    goals = "\n".join(f"- {f(g)}" for g in p["learning_goals"])

    header = f"""
<p class="meta">Last modified: {lm}</p>

# {title} {n} - {L['instructions']}

**{L['date']}:** {task_date}  |  **{L['total_time']}:** {dur(p['total_min'])} ({dur(group_min)} + {dur(pres_min)})

## {L['goals']}
{goals}

## {L['background']}
{f(L['background_text'])}

---

# {L['handout']} - {title} {n}

{spec['handout'].strip()}

#### {L['your_task']}: {f(L['task_text'])}{focus}

{L['no_need']}

> {L['reference']} ({spec.get('reference_label', 'NEJM case')}): [{spec['reference_url']}]({spec['reference_url']})
"""

    rows, t = [], 0
    for s in p["group_steps"]:
        rows.append(f"| {hm(t)} - {hm(t + s['minutes'])} | **{f(s['title'])}:** {f(s['text'])} |")
        t += s["minutes"]
    qs = "\n".join(f"1. {q}" for q in p["discussion_questions"])
    pts = "\n".join(f"  - {x}" for x in p["presentation_points"])
    ev = "\n".join(f"- **{a}:** {f(b)}" for a, b in p["evaluation"])
    steps = f"""
---

## {L['at_a_glance']} ({dur(p['total_min'])})

| {L['time']} | {L['activity']} |
|---|---|
| 0:00 - {hm(group_min)} | **{L['step1']}** ({dur(group_min)}) |
| {hm(group_min)} - {hm(p['total_min'])} | **{L['step2']}** ({dur(pres_min)}) |

## {L['step1']} ({dur(group_min)})
{f(L['in_groups'])}

| {L['time']} | {L['what_to_do']} |
|---|---|
{chr(10).join(rows)}

{L['for_each']}
{qs}

## {L['step2']} ({dur(pres_min)})
{f(L['presenters_line'])}

- **{L['time']}:** {p['talk_min']} + {p['qa_min']} min Q&A ({p['presenters']} x ({p['talk_min']} + {p['qa_min']}) min = {pres_min} min).
- {L['must_cover']}
{pts}

# {L['evaluation']}
{L['assessed']}

{ev}
"""
    os.makedirs(out_dir, exist_ok=True)
    lang, rtl = p.get("language", "en"), p["rtl"]
    logo = logo_tag(p.get("logo_path"), p.get("logo_base_dir", os.getcwd()))
    fname = f"{p['file_prefix']}{n}.html"
    path = os.path.join(out_dir, fname)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(page(f"{title} {n}", header + steps, lang, rtl, logo))
    print("wrote", path)

    key = spec.get("instructor_key")
    if key:
        lines = [f"# {title} {n} - {L['key_title']}", "",
                 f"**Task date:** {spec['task_date']}", "", f"**Article:** {key['article']}", "",
                 f"**Citation:** {key['citation']}", "", f"**Final diagnosis:** {key['diagnosis']}", "",
                 key.get("summary", ""), "", "| Method | Taught | New in window | Use in this case |",
                 "|---|---|---|---|"]
        for m in key["methods"]:
            lines.append(f"| {m['name']} | {m['date']} | {'yes' if m.get('new') else ''} | {m['use']} |")
        lines += ["", f"**Justification:** {key['justification']}", ""]
        kpath = os.path.join(out_dir, f"{p['file_prefix']}{n}_instructor_key.html")
        with open(kpath, "w", encoding="utf-8") as fh:
            fh.write(page(f"{title} {n} - key", "\n".join(lines), lang, rtl))
        print("wrote", kpath)


if __name__ == "__main__":
    build(json.load(open(sys.argv[1], encoding="utf-8")),
          json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3])

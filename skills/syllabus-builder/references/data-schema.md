# Companion data file — `<course>_syllabus_data.json`

The data file stores everything needed to update the syllabus later without re-reading all the old material. Write it alongside the syllabus. In update mode, read it back, merge new material, bump `meta.version`, and add a changelog entry.

## Item type

Most fields are **Items**: either a plain string, or an object

```json
{"text": "content", "tbd": "what is missing", "status": "planned", "source": "S2 slide 4"}
```

- `text` only → normal content
- `tbd` only → placeholder `[TO BE COMPLETED: …]`
- `text` + `tbd` → content followed by a placeholder for the missing part
- `status: "planned"` → shown as "(planned)"
- `source` → traceability; always fill for factual items

## Structure

```json
{
  "meta": {
    "course_title": "",
    "year_semester": "",
    "learner_stage": "preclinical | clinical | phd | md-phd | postdoc",
    "course_kind": "block | module | longitudinal | elective | lab",
    "institution": "",
    "language": "en",
    "template": "institution template name, or 'default'",
    "framework": {"name": "", "version": "", "source": "file name or URL supplied by the course leader"},
    "version": 1,
    "last_updated": "YYYY-MM-DD",
    "sources": [{"id": "S1", "name": "", "kind": "slides | outline | notebook | exam | conversation", "notes": ""}]
  },
  "description": Item,
  "general_info": {"credits": Item, "meetings": Item, "director": Item, "administrator": Item, "instructors": [Item], "location": Item},
  "schedule": {
    "rows": [{"date": Item, "time": Item, "location": Item, "activity": Item, "format": "", "objectives": "O1, O3", "framework_items": ""}],
    "other": [Item]
  },
  "materials": {"reading": [Item], "methods": [Item], "digital_tools": [Item], "ai_policy": Item},
  "objectives": [
    {"id": "C1", "text": "", "verb": "", "level_3": 2, "bloom": "Apply", "framework_items": ["ID"], "source": ""}
  ],
  "competencies": [
    {"item": "framework ID", "wording": "verbatim from framework", "level": "E | P",
     "activities": "", "evidence": "", "milestone": "", "status": "planned (optional)"}
  ],
  "assessment": {"grading_type": Item, "forms": [Item], "feedback": [Item], "criteria": [Item]},
  "internal": {
    "section_status": {"Description": "complete | partial | missing"},
    "links": [{"item": "", "level": "E | P", "activity": "", "source": "", "artifact": "", "status": ""}],
    "exposure_only": [""],
    "cheap_upgrades": [""],
    "matrix_check": {"expected_found": [], "expected_missing": [], "unexpected_found": []},
    "gaps": [""],
    "open_questions": [""],
    "framework_issues": [""],
    "material_issues": [""],
    "handoffs": [""],
    "changelog": [{"version": 1, "date": "YYYY-MM-DD", "changes": ""}]
  }
}
```

If objectives came from `learning-objectives-designer`, copy its IDs unchanged into `objectives[].id`.

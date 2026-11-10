# Deliverable Specs

Each teaching session typically has four components. This file covers the three ancillary ones — the pre-session reader, the comprehension quiz, and the intro lecture brief. The session itself (your PBL case or RBL investigation) is covered in `structural-options.md`, `pedagogical-canon.md`, and `facilitator-voice.md`.

The four components per session:
1. **Pre-Session Reader** — assigned reading before the session
2. **Comprehension Quiz** — short entry check at the start of the session
3. **Intro Lecture Brief** — spec for a 30–45 minute contextualizing lecture
4. **Session** (PBL or RBL) — the main case or investigation document

---

## A note on sources before you start

This skill works best when you supply your own source library — the textbook chapters, articles, or readings your course already uses. When you provide sources, the reader draft will point into them with accurate page numbers and framing.

**If you have not supplied sources:**

The skill will tell you so plainly rather than invent citations. Fabricated page numbers and references are worse than none — a student who follows a bad citation loses the point entirely. When sources are missing, drafts will mark every factual claim and citation with **[UNVERIFIED]** so you can check each one against a real source before anything ships.

To add sources: share the files, paste the relevant passages, or point the skill to page ranges in a text you have access to. Even a table of contents or chapter list helps narrow what to ask for.

---

## 1. Pre-Session Reader

### Purpose

Students arrive having read a targeted set of material — enough to give them a conceptual foothold so the session is not a cold start. The reader is a preparation scaffold, not a mini-lecture.

### What it is NOT

- A comprehensive summary of the topic
- A Wikipedia-style overview the AI writes from scratch
- An attempt to teach everything — that is the session's job
- Longer than your students will actually read

### What it IS

- A **pointer document** — specific pages or sections in your course's texts, with brief notes on why each piece is included
- A **framing document** — a short paragraph at the top establishing the central question the session will explore
- A **curated list** — page ranges, estimated reading times, and a 1–2 sentence note per item

### Structure

```
# Reader — [Session Title]

## The question we're sitting with
[One paragraph. What is the question or puzzle the session will open?
What should students be asking as they read?]

## What you already know
[Two or three sentences pointing back to prior sessions or prior
coursework that built the scaffolding for this one. Specific, not vague.]

## What to read before the session
Total time: [estimated hours], [estimated pages]

1. [Source, specific pages or sections] ([estimated time])
   [1–2 sentence note: what the student should get from this piece,
   and why it's here rather than something else.]

2. [Source, specific pages or sections] ([estimated time])
   [1–2 sentence note]

3. [Additional piece if needed]
   [1–2 sentence note]

## Active reading prompt
[One short question or lens to carry through the reading. Not something
students answer in writing — something that orients their attention.
Example: "As you read, keep asking: what would have to break for this
system to fail? We'll start from your answers."]
```

### Voice

Collegial framing, not lecture. Talk to a curious person, not a student completing an assignment. No preamble like "In this reader we will cover…".

### Length discipline

Set a page cap appropriate for your students' preparation load and stick to it. A reader that exceeds what your students will actually complete is counterproductive. If the ideal reading list is too long, cut the least essential piece rather than expanding the cap.

### Common AI drafting errors to watch for

- Writing its own summary of the topic instead of pointing to your sources. Push back: "No summary prose — point to the sources with page numbers and a 2-sentence note per item."
- Overshooting your page cap. Enforce it.
- Forgetting the active reading prompt. Include it.
- Inserting fabricated page numbers when no source was provided. Demand [UNVERIFIED] flags instead.

---

## 2. Comprehension Quiz

### Purpose

A short entry check at the start of the session — typically 10–15 minutes. It tests whether students did the reading. Easy level. Not an intellectual stretch — a commitment device and a signal to students that preparation is taken seriously.

### Core principle

**Every answer must be derivable from the assigned reading alone.** If a student who did the reading carefully cannot answer a question, the question is testing outside knowledge, not preparation. Rewrite it.

### Format

- **4–6 questions** (calibrate to your time window)
- **Single best answer** from a set of options
- **One inference per question** — identify the key concept, not a chain of reasoning
- Easy level — a prepared student should answer in 1–2 minutes per question; an unprepared student should have to guess

### Each question has three parts

1. **The question** (stem + options)
2. **The answer with explanation** (1 short paragraph — teaches even students who got it right)
3. **The reader citation** (which passage or page this question draws from)

### Example structure

```
Q1. [One-paragraph scenario or concept setup. Keep it brief — if
students need more than a minute to read the stem, it's too long.]

A) [Option]
B) [Option]
C) [Option]
D) [Option]
E) [Option]

Answer: [Letter]

Explanation: [1 paragraph. Explains why the correct answer is right
and why the most tempting wrong answer is wrong. Ties back to the
reader content.]

Reader source: [Specific passage, section, or page range.]
```

The scenario can be discipline-appropriate — a patient, a policy case, a lab observation, a historical puzzle, a data table — whatever your field uses as its natural unit of "a situation worth analyzing."

### Difficulty calibration

The quiz measures "did you prepare," not "how deep is your understanding" — the session handles the latter. If a well-prepared student can miss a question because it requires synthesis beyond the reading, rewrite the question.

### What to reject

- **Two-layer questions** — require the student to first figure out one thing and then figure out another. These test synthesis, not preparation. Cut to one inference.
- **Obvious distractors** — if four of five options are clearly implausible, the question measures reading-the-question, not reading-the-reader. Make the wrong answers plausible given partial preparation.
- **Abbreviations or jargon not introduced in the reader** — if it's in the quiz, it needs to appear in the reading.

### End-of-session questions for assessment pools

If your course uses a cumulative exam, the comprehension quiz questions are typically too easy to promote directly. A better pattern: include 3–5 harder questions at the end of the session document that require synthesis across the day's work. Flag those as exam candidates. The morning quiz and the end-of-session questions serve different purposes.

---

## 3. Intro Lecture Brief

### Purpose

A spec for a 30–45 minute lecture delivered at the start of the session, after the quiz. The lecture sets the stage — it does NOT cover the topic comprehensively (that is what the reading was for). Its job is to make students curious about what they just read and ready to engage with the case or investigation.

### Register

**Contextualization, not coverage.** Why does this topic matter? What is the shape of the open question? What would Feynman have asked a student about this before starting? The lecture should sharpen curiosity, not deliver information.

### The brief vs. the lecture

The brief is not a script — it is a spec for a skilled lecturer. It tells them what must land, what they can skip, and what the transition to the session looks like. Respect the lecturer's autonomy to deliver it in their own voice.

### What the brief contains

```
# Lecture Brief — [Session Title]

## Central question
[One sentence. The question the lecture circles around. Not the topic —
the question.]

## Suggested lecturer
[If you have collaborators or domain experts who might deliver this,
name them here with a one-line rationale. If the course instructor
delivers all lectures, omit this.]

## The five beats (30–45 min)

Beat 1 (5 min) — Hook
  [The provocative opening. A paradox, a historical puzzle, a surprising
  piece of data, a patient outcome that defies the obvious explanation.
  What makes a student lean forward?]

Beat 2 (10 min) — Frame
  [The conceptual landscape — not everything, just the frame that makes
  the session make sense. What does the student need to orient?]

Beat 3 (10 min) — One mechanism or idea in depth
  [Pick one thing and go deep. Feynman-style: not a survey, but a
  specific example that reveals the pattern. The rest can be left to
  the session.]

Beat 4 (10 min) — Open questions / current frontier
  [What doesn't the field know? Where are the live debates? What would
  a researcher in this area lose sleep over? This is especially
  important for advanced students who need to see the edge.]

Beat 5 (5 min) — Bridge to session
  [Explicit connection: lecture → session. "We've just seen why X is
  puzzling. In the next four hours, you're going to work through a case
  that puts you right at that puzzle."]

## What to leave out
[List 2–3 things the lecturer might be tempted to include but should
not. Usually: comprehensive coverage of the topic, the full mechanism
(that's for the session), anything the reading already did well.]

## Visual aids
[2–4 suggested figures or diagrams. Prioritize: one that establishes
the conceptual frame, one that shows a real example, one that opens
rather than closes a question.]

## The must-land idea
[If the lecturer runs short on time and has to cut, what is the single
idea that must land before they hand off to the session? One sentence.]
```

### Voice of the brief

Teacher-to-teacher. Collegial. The brief helps a knowledgeable colleague prepare, without over-specifying their delivery.

**Don't:**
- Script the lecturer's sentences
- Tell the lecturer how students will feel
- Explain the topic as if the lecturer doesn't know it

**Do:**
- Flag the single must-land idea per beat
- Name the bridge moment to the session explicitly
- Point to 2–4 visual aids with brief rationale

### Length

**The brief itself: approximately 2 pages.** If it runs longer, you are over-specifying. The brief is a skeleton for a skilled colleague, not a teleprompter.

---

## Cross-references

- `pedagogical-canon.md` — design principles that apply to all four deliverables
- `facilitator-voice.md` — voice guidance for reader framing and lecture briefs
- `student-calibration.md` — calibrating quiz difficulty and reading load to your students
- `working-with-the-ai.md` — pushback phrases when readers drift to summary prose, quizzes get two-layered, or lecture briefs get over-scripted
- `quality-checklist.md` — final checks before any deliverable ships

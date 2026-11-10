# Getting Started

Welcome. This skill helps you build discovery-based teaching sessions — and the readings, quizzes, and lectures around them — in your own field. You bring the subject expertise; the skill brings the learning design. You do not need to be an AI power user to use it well.

This page is short on purpose. Read it once, then start.

---

## What this skill is

It turns the AI into a **design partner** for active-learning sessions: case-driven PBL, or tool-driven RBL where students operate a real dataset, simulator, or instrument. It enforces a portable set of design principles (see `pedagogical-canon.md`) so that what you produce makes students *think* rather than *look things up*.

It is **not** a content generator that spits out a finished session on one prompt. It works through a conversation — and the conversation is where the quality comes from.

---

## Equip it first (recommended)

The skill runs on its own, but it gets much better when you bring two things:

- **A source of truth** — the authoritative material your course rests on (a textbook chapter, a review, a dataset, trusted notes). This grounds the *facts*. Without it, the skill reasons from its own training and can produce citations that look right but are invented; with it, every claim is anchored to something you can check.
- **Best examples** — one or two sessions or cases you consider gold-standard. This sets the *bar*. "Good" is hard to describe and easy to show; an exemplar tells the skill the structure, depth, and voice you want better than any rule — and lets a colleague match your house style without you in the room.

They guard against different failures: a session can be *correct but flat*, or *elegant but wrong*. Bring both if you can; if you bring only one, bring the source of truth. Full detail — what makes a good exemplar and how to hand it over — is in `equipping-the-skill.md`.

---

## How to work with it

- **Configure first.** Before it builds anything, the skill will ask about your discipline, your students' actual stage, the session format, the source of truth and best examples you can bring (see above), and the tools you have. Answer these as concretely as you can — especially *what your students cannot yet do*. This is the most important thing you'll tell it.
- **Answer the design questions honestly.** It will ask reflexive questions ("what's the one thing students should own by the end?"). If you don't know yet, say so — that's what the discovery conversation is for. If you give a three-part answer, it should ask you to narrow.
- **You are the expert.** When your instinct disagrees with the skill, your instinct wins. The references are a proxy for a learning designer's thinking, not an authority over your subject.
- **Reject AI effusiveness.** If the facilitator notes say things like "students will feel something shift here" or "this is where the magic happens" — that's a failure mode, not good writing. Reject it and say so. See `facilitator-voice.md`.
- **Insist on alignment before drafting.** The sessions that fail are the ones where someone skipped agreement on the skeleton and jumped to prose. If you're being handed full paragraphs before you've agreed on the phase structure, stop and back up.

---

## The workflow at a glance

1. **Configure** — discipline, students, format, sources, voice.
2. **Discover** — the skill asks design questions; you answer.
3. **Choose a structure** — it offers 2–3 options; you pick.
4. **Align** — you both agree on the skeleton before any prose.
5. **Draft** — it writes interleaved student/facilitator content.
6. **Calibrate & review** — every prompt is tested against your students' stage and the quality checklist.
7. **Iterate** — surgical edits, versioned.

---

## What the skill cannot do

- **It cannot know your students unless you tell it.** Stage, prior units, what they've been taught — these are inputs, not guesses.
- **It cannot know your sources.** It will not invent citations or page numbers; if you don't give it sources, it will flag every factual claim as unverified for you to check.
- **It cannot confirm what a tool can do.** For an RBL, tell it the real capabilities of your simulator/dataset/instrument. It must never design a task around a feature you haven't confirmed.
- **It cannot supply lived experience.** If a case needs a real human scene, you may need to write the human texture from experience and hand it over for the question-writing.

When it hits one of these limits, it should ask you — not fill the gap silently. If it fills a gap instead of asking, that's a bug; correct it (see `working-with-the-ai.md`).

---

## If you're stuck

Tell the skill what feels off in plain language — "this prompt feels like an exam question", "this is moving too fast for my students", "this paragraph sounds like a brochure." `working-with-the-ai.md` has paste-ready phrases for the common cases. You don't need the right vocabulary; you just need to name the discomfort.

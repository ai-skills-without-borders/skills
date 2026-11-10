# Equipping the Skill

The skill works on its own, but it gets markedly better when you give it two things up front: a **source of truth** and one or two **best examples**. One grounds the *facts*; the other sets the *bar*. Ten minutes here improves every session you build afterward.

These two inputs are different and guard against different failures. Bring both if you can.

| Input | Answers the question | Without it |
|-------|---------------------|------------|
| **Source of truth** | *Is this correct?* (facts, citations) | The skill reasons from its own training; citations may be fabricated |
| **Best examples** | *Is this good?* (structure, depth, voice) | The skill falls back to a generic default quality bar |

---

## 1. A source of truth — grounds the facts

**What it is:** the authoritative material your course rests on — a textbook chapter, a review article, a dataset, a standard reference, lecture notes you trust. Whatever you'd point a student to and say "this is correct."

**Why it matters:** without it, the skill reasons from its own training. It may be approximately right, but it cannot cite *your* curriculum, and it can produce confident-looking citations that are invented. With it, every factual claim and page reference is anchored to something real you can check.

**How to give it:**
- Paste the relevant text into the conversation, or
- Point the skill to a file ("use `chapter-4.pdf` in this folder"), or
- Drop them in this skill's `sources/` folder (its `README.md` explains it).

**What the skill does with it:** grounds factual claims in your source and cites it where useful. When you have *not* given it one, it flags every factual claim as **unverified** rather than inventing a citation — and you can ask it to list which claims it could not source.

---

## 2. Best examples — set the bar

**What it is:** one or two sessions, cases, or activities you consider gold-standard — your own, a colleague's, or a published exemplar. The thing you'd hold up and say "this is the quality and style I want."

**Why it matters:** "good" is hard to specify in the abstract and easy to show by example. An exemplar tells the skill — far more precisely than any rule — the structure, depth, step-width, and voice you're aiming for. It also lets a colleague who has never built a session match your house style without you in the room.

**A good exemplar is:**
- A *complete* unit, or at least a full phase — not a fragment — so the structure is visible.
- Something you genuinely admire, not just the most recent thing you have.
- Ideally annotated with one line on *why* it's good ("the productive trap in phase 2 is the whole point"), so the skill copies the substance, not the surface.

**How to give it:** paste it, point to the file, or drop it in this skill's `examples/` folder (see the `README.md` there).

**What the skill does with it:** treats the exemplar as the benchmark — it matches structure and voice to your example rather than to a generic default. When an expert authored the example, it starts from their design and layers improvements on top rather than overwriting it.

---

## If you have only one — or neither

If you can bring only one, bring the **source of truth**: fabricated facts are the more dangerous failure, and an elegant session built on a wrong premise is worse than a plain one built on a right premise.

If you have neither, the skill still runs. It will tell you what it's assuming, flag unsourced claims, and default to the built-in `pedagogical-canon.md` and `facilitator-voice.md`. Treat that output as a strong first draft to check against your own sources and standards — not as ship-ready.

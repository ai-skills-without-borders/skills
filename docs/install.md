# Installing the skills

Every skill is a folder with a `SKILL.md` in the open Agent Skills format. Pick your tool below. Menu names change often — if a step doesn't match what you see, check your tool's help pages for "skills".

Downloads (built by `tools/build.py`, also on the catalog site):
- `dist/zips/<skill>.zip` — the skill folder, for uploading
- `dist/paste/<skill>.md` — a single paste-in file for tools without skill support

---

## Claude

**Claude.ai / Claude desktop (individual):** Settings → Capabilities: make sure code execution / file creation is on. Then Customize → Skills → **+** → Upload a skill → choose `<skill>.zip`. Uploaded skills start **off** — switch the toggle on.

**Claude for organizations:** an admin can register this repository as an organization plugin source with automatic sync, so everyone gets updates without re-uploading.

**Claude Code:**
```
/plugin marketplace add ai-skills-without-borders/skills
/plugin install ai-skills-without-borders@ai-skills-without-borders
```
Update later with `/plugin marketplace update ai-skills-without-borders`.

## ChatGPT (Business, Enterprise, Edu, Healthcare)

Skills → Create → **Upload from your computer** → choose `<skill>.zip`. ChatGPT scans the upload; most skills are available as soon as the scan finishes. Workspace admins control who may upload, share and publish skills; a skill can be published to the whole workspace.

## Gemini Enterprise

Skills → **+** → Upload → choose the `SKILL.md` or `<skill>.zip`. Gemini Enterprise reads the name and description from `SKILL.md`. If your admin allows sharing, share it with colleagues from the Skills page. Note: skills with scripts run Python or Bash only.

## Microsoft 365 Copilot

**Copilot Cowork:** put each skill folder (with its `SKILL.md`) in your OneDrive under `Documents/Cowork/Skills/`. Start a new Cowork conversation. Limits apply (number of custom skills and file size) — check Microsoft's current documentation.

**Copilot Studio agents:** in the agent's skills settings, upload the skill file or package.

Both need a Microsoft 365 Copilot license.

## Coding agents (Codex, Gemini CLI, GitHub Copilot in VS Code, Cursor)

Clone the repository and copy the skill folders into your agent's skills directory — for example `.agents/skills/` in a project (read by Gemini CLI and other tools that follow the standard), or `~/.codex/skills/` for Codex. Start a new session.

## Free or personal plans without skills (ChatGPT Free/Plus, Gemini app, Copilot consumer)

Use the paste-in version `dist/paste/<skill>.md`:

- **ChatGPT custom GPT:** paste the *Instructions* section into the GPT's instructions; upload the *Reference files* section (or the skill's `references/` files) as knowledge files.
- **Gemini Gem:** paste the whole file into the Gem's instructions (or the instructions part, and add references as files).
- **Claude Project / ChatGPT Project:** paste into the project instructions; add reference files to the project.
- **Any chat:** paste the file at the start of a conversation.

Paste-in versions can't run scripts. `lesson-format-checker` still works by reading, more slowly.

---

## Which tools run code?

Only `lesson-format-checker` has optional scripts (notebook inspection and timing checks). Tools that run code in a sandbox (Claude with code execution, ChatGPT with skills, Gemini Enterprise skills, coding agents) can use them; elsewhere the skill does the same checks by reading.

## After installing

Try the skill on a small real task, then tell us how it went — a [usage report](../community/usage-report.md) takes five minutes and helps every other educator.

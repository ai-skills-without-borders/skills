# Website forms: one-time setup (about 15 minutes)

The Share page (`share.html`) lets anyone send a usage report or a new skill without a GitHub account.
It posts to a small Cloudflare Worker (`worker.js`), which checks the visitor is a person and files the
GitHub issue. Everything after that is the repository's usual automation.

Free plans are enough for all of it. You need to do this once; nothing here needs looking after.

## 1. A GitHub token for the Worker

1. On GitHub, open your picture (top right) → **Settings** → **Developer settings** → **Personal access tokens** → **Fine-grained tokens** → **Generate new token**.
2. **Token name:** `skills website forms`. **Expiration:** the longest offered (set a reminder to renew it).
3. **Resource owner:** `ai-skills-without-borders`. **Repository access:** *Only select repositories* → `skills`.
   If the organization isn't offered, an owner must allow fine-grained tokens: organization **Settings → Personal access tokens → Settings**.
4. **Permissions → Repository permissions → Issues:** *Read and write*. Nothing else.
5. **Generate token** and copy it. You'll paste it in step 3; GitHub shows it only once.

## 2. A Cloudflare account and a Turnstile widget

1. Sign up at **dash.cloudflare.com** (free). No domain is needed.
2. In the left menu open **Turnstile** → **Add widget**.
   - **Widget name:** `skills site`
   - **Hostname:** `ai-skills-without-borders.github.io` (and your own domain later, if the site moves)
   - **Widget mode:** *Managed*
3. **Create**. Keep the page open: you need the **Site key** and the **Secret key**.

## 3. The Worker

1. In the left menu open **Workers & Pages** → **Create** → **Create Worker**. Name it `asb-forms` → **Deploy**.
2. **Edit code**: delete what's there, paste the whole of `worker/worker.js` from this repository, **Deploy**.
3. Open the Worker's **Settings → Variables and Secrets** and add:

   | Type | Name | Value |
   |---|---|---|
   | Secret | `GITHUB_TOKEN` | the token from step 1 |
   | Secret | `TURNSTILE_SECRET` | the Turnstile *Secret key* |
   | Text | `REPO` | `ai-skills-without-borders/skills` |
   | Text | `SITE` | `https://ai-skills-without-borders.github.io/skills/` |

4. Optional, recommended: a limit of five submissions an hour per address. **Storage & Databases → KV → Create** a namespace called `asb-limits`; then in the Worker's **Settings → Bindings → Add → KV namespace**, variable name `LIMITS`, namespace `asb-limits`.
5. Note the Worker's address, shown on its page: `https://asb-forms.<something>.workers.dev`.

## 4. Switch the forms on

In `config.yaml`:

```yaml
web_forms:
  endpoint: "https://asb-forms.<something>.workers.dev/submit"
  turnstile_sitekey: "<the Turnstile Site key>"
```

Commit. After the next build the Share page's forms are live (until then it points to GitHub and email).

## How submissions are handled

- Issues from the website carry the label **via-website** and record no GitHub user.
- **Usage reports** publish automatically, like those from known contributors. To withdraw one, add the label **withdrawn** to its issue: everything it changed is undone.
- **New skills** open a pull request for one maintainer's approval.
- If the token expires, submissions fail with a message asking people to try later or email; renew the token (step 1) and replace the `GITHUB_TOKEN` secret.

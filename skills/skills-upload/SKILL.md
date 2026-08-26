---
name: skills-upload
description: Get set up to contribute a skill to the OGP shared skills library (opengovsg/corp-ai-skills), then upload one. Handles gh authentication, checks repo access, and opens the PR from wherever you are working — no permanent clone required. Triggers on "/skills-upload", "upload this skill", "add this skill to the OGP skills repo", "contribute a skill", or any ask to get set up to contribute skills.
---

# skills-upload: get set up, then upload

A convenience, not a requirement. Anyone can contribute by opening an ordinary PR that adds `skills/<name>/` to `opengovsg/corp-ai-skills` — the repo installs the improvement nudge and syncs `index.md` on merge, however the PR arrived. This skill exists to spare a first-time contributor the setup and the git steps.

So don't treat any of this as load-bearing. If something here fails, say so and point the user at `CONTRIBUTING.md` in that repo; the manual route works fine.

**Not your job:** installing the nudge, or editing `index.md`. The intake Action owns both, after merge. Touching them here would create a second source of truth that drifts.

## Phase 1: Setup

Work through these, skipping whatever already holds. Report what you skipped rather than staying silent.

1. **Is `gh` installed?** `gh --version`. If not, tell the user how to install it for their platform and stop until they have.
2. **Is `gh` authenticated?** `gh auth status`. If not, have them run `gh auth login` themselves — walk them through the prompts, but never handle their credentials.
3. **Can they reach the repo?** `gh repo view opengovsg/corp-ai-skills --json name`. Everyone in OGP should be able to; a failure here means they're outside the org or not authenticated to it. Say which, and stop.

## Phase 2: Intake

Gather, asking only for what's missing:

1. **The skill folder** — a local path containing at least a `SKILL.md`.
2. **Name** — kebab-case, defaulting to the folder name.
3. **Frontmatter check** — `SKILL.md` must have `name` (matching the folder) and a `description` covering both what the skill does and when it triggers. If the description only says what it does, offer to draft the trigger half; don't invent it silently.

Then a few early warnings. None of them block — the reviewer does the real assessment — but each saves a round trip:

- **Secrets.** Scan the folder for anything token-shaped, a webhook URL, or a private key. A hit is a hard stop: the check will fail the PR anyway, and the credential needs rotating because this repo is readable across OGP.
- **Scope.** Flag anything the reviewer's security pass will catch: shell commands whose effect isn't stated, sending data to an external endpoint, reading outside the skill's stated scope, fetch-then-execute. Tell the user what you found and let them decide whether it's necessary.
- **Overlap.** `gh api repos/opengovsg/corp-ai-skills/contents/index.md --jq .content | base64 -d` and read the table. If an existing skill plausibly answers the same request, name it and ask whether to continue.
- **Personal references.** Scan for a person's name, a Slack handle, or an absolute home-directory path — signs the skill was written for one person's setup rather than a colleague who's never seen it (this is a real, recurring failure mode: a skill copied over from someone's personal vault often still gatekeeps a decision on that person by name). Point out what you found and ask whether to generalise it, e.g. naming a role or channel instead.

## Phase 3: Open the PR

The user is probably working in their own repo or workspace, so never initialise, commit to, or add a remote to wherever they are. Work in a temp directory and discard it.

1. Check for write access: `gh api repos/opengovsg/corp-ai-skills --jq .permissions.push`. Everyone in OGP should have it through the `all-ogp` team. If false, stop and ask the library owner to check their organisation membership or repository access; organisation-level forking is disabled, so a fork is not a fallback.
2. `gh repo clone opengovsg/corp-ai-skills` into a temp directory.
3. Branch `skill/<name>`.
4. Copy the skill folder to `skills/<name>/`.
5. Stage that exact path only — never `-A`, never a directory-wide add.
6. Commit `Add skill: <name>`.
7. Push and `gh pr create --repo opengovsg/corp-ai-skills`. The body says what the skill does, who owns it, and that the frontmatter and secret checks passed.
8. Delete the temp directory.
9. Report the PR URL, and say what happens next: the check runs immediately, the reviewer comments a verdict within minutes, a human merges, and the nudge is installed on merge.

## Boundaries

- Never merge, never push to `main`.
- Never edit a skill other than the one being uploaded.
- Never write anything into the user's own working directory.
- Never invent a purpose line or an owner — ask.
- One skill per PR.

## Improving this skill

<!-- ogp-improvement-nudge v1 — installed automatically; edit nudge.md, not this copy -->
Near the end of any session that used this skill: if anything in it was wrong, missing, out of date, or harder than it should have been, tell the user briefly and offer to open an improvement PR. Make the offer once, without pressure, and skip it entirely if the session ran without friction.

If they accept, read `CONTRIBUTING.md` in `opengovsg/corp-ai-skills` — from a local clone if there is one, otherwise `gh api repos/opengovsg/corp-ai-skills/contents/CONTRIBUTING.md --jq .content | base64 -d` — and follow it. Regardless of what it says: branch `skill-fix/<skill-name>`, stage only this skill's folder by exact path, never commit to `main`, and say in the PR body what happened in the session that prompted the change.

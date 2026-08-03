# Contributing

Everything here arrives by pull request. Two ways in, and neither asks you to learn the repo's conventions — the automation handles those.

You don't need write access. Everyone in OGP can read this repo, which means everyone can fork it and open a PR.

## Adding a new skill

Open a PR that adds `skills/<name>/`, containing at least a `SKILL.md`. Any branch name, any method: the GitHub web UI, `gh`, a fork, a clone, or the `skills-upload` skill if you have it.

The `SKILL.md` needs YAML frontmatter with:

- `name` — kebab-case, matching the folder name
- `description` — what the skill does *and* the phrases or situations that should trigger it. Both halves matter; a description that only says what it does won't fire reliably.

You do not need to add the improvement nudge, or touch `index.md`. Both happen automatically when your PR merges.

**Keep the skill general.** Edge cases, long lookup tables, and worked examples belong in `references/<topic>.md` that the skill points at — they cost context on every invocation and pay off occasionally.

## Improving a skill you've used

This is the path most changes take, and usually your assistant offers it before you think of it — every skill carries a nudge that fires when a session hits friction.

Whether prompted or not:

1. Branch `skill-fix/<skill-name>`.
2. Stage only that skill's folder, by exact path. Never `-A`.
3. Never commit to `main`.
4. In the PR body, say what happened in the session that prompted the change. This is the most useful thing in the PR — it tells the reviewer whether the fix addresses the real problem. If you're removing a check, a confirmation step, or a safety rail, say why: the reviewer treats an unexplained removal as a failure.

No local clone needed. Clone to a temp directory, push to your fork, and discard it; nothing has to live in your workspace.

## What happens to your PR

| | Who | What |
|---|---|---|
| Immediately | `skills-check` Action | Refuses secrets, reports a missing or stale nudge |
| Minutes later | The reviewer agent | Scores the change and comments one verdict |
| Then | A human | Merges or closes. No agent has merge authority |
| On merge | `skills-intake` Action | Installs the current nudge, syncs the `index.md` row |

If the check reports a missing nudge, ignore it — that's informational. It gets installed after merge.

## What the reviewer judges

**Security, on every contribution.** A skill is executable instruction: it runs with whatever access the person invoking it has. Shell commands whose effect isn't stated, anything sending data outward, reads outside the skill's stated scope, fetch-then-execute, instructions to skip a confirmation or hide output — all fail. On a change to an existing skill, removing a safety rail without explaining why fails too.

**A new skill**, additionally on three counts:

- **Overlap** — would a request that triggers your skill also plausibly trigger an existing one? Overlapping skills fail by mis-triggering, not by duplicating text.
- **Genericity** — usable by anyone in OGP. No absolute paths, no one person's channels or accounts, no hardcoded IDs that belong in an intake question.
- **Completeness** — could someone who has never seen it run it end-to-end from the folder alone?

**A change to an existing skill**, additionally on where it belongs. The principle: **a skill stays as general as possible, and reference files carry the specificity.** A change that sharpens the skill generally gets merged; a change serving specific use cases becomes `references/<topic>.md`; a change that's really a different job becomes its own skill. When a change is both substantial and use-case-specific, generality wins and it goes to a reference.

Trivial fixes — a typo, a clearer sentence — just get merged. No triage.

## Hard rules

- Never commit a secret. The check fails the PR, but rotate anything real that was exposed — this repo is readable across OGP.
- Never edit an installed nudge block. Change `nudge.md` and the intake Action rewrites every copy.
- One skill per PR. Two skills in one diff makes the review ambiguous and the revert messy.

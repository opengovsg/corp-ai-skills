# CLAUDE.md — corp-ai skills

Agent operating rules for this repo. For what the repo *is*, read [`README.md`](README.md); for what's in it, [`index.md`](index.md).

This repo holds one kind of thing: Claude Code skills for OGP, in `skills/<name>/`. If a change doesn't add or improve a skill, or the machinery that reviews them, it probably belongs somewhere else — say so rather than filing it here.

## Contributions arrive as pull requests

Never commit to `main`. Never merge. A human decides every merge, and the review agent has no merge authority either.

When helping someone add or improve a skill, follow [`CONTRIBUTING.md`](CONTRIBUTING.md) — it is the canonical process, and the improvement nudge inside every skill points at it.

## Never hardcode a secret

No API key, token, or webhook URL, anywhere, including in examples. A skill needing credentials documents how to obtain them at runtime; it never carries them. The intake check fails a PR on a suspected secret, but the real cost lands before that — anything committed to an org-visible repo must be treated as exposed and rotated.

## The nudge is generated, not written

`nudge.md` is the single source of truth. Never edit an installed copy inside a skill's `SKILL.md`, and never hand-write one into a new skill — the intake Action installs and repairs it after merge. If the wording needs to change, change `nudge.md` and bump its version.

## Writing skills

- A `SKILL.md` needs YAML frontmatter with `name` (matching the folder) and a `description` covering both what the skill does *and* when it triggers. A description missing the trigger half won't fire reliably.
- **Keep the skill general; put specificity in reference files.** A skill that serves everyone stays short and loads fast. Edge cases, long lookup tables, and worked examples belong in `references/<topic>.md` that the skill points at, because they cost context on every invocation and pay off occasionally.
- Write for a colleague who has never seen it: no absolute paths, no one person's channels or accounts, no hardcoded IDs that belong in an intake question.

## House style

- British English in prose. American English in identifiers and library tokens.
- Em dashes only where they earn their place. Default to commas, parentheses, colons, or sentence breaks.
- Code comments explain why, not what.
- Automations are Python, standard library first. Add a dependency only when stdlib genuinely can't do the job.

## Changes to the machinery

The Actions in `.github/` and the prompt in `reviewer/` govern every contribution, so treat them as load-bearing:

- Deterministic work (secret scanning, nudge installation, index sync) belongs in the scripts. Judgement (overlap, genericity, completeness, security, routing) belongs in the reviewer's rubrics. Don't move work across that line without saying why.
- The reviewer prompt in `reviewer/PROMPT.md` is the canonical copy; the Cloud Routine on claude.ai must match it. Changing one without the other silently breaks the review.

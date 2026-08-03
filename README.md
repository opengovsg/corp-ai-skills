# corp-ai skills

A shared library of Claude Code skills for OGP. Starting with Corporate, open to the whole organisation over time.

A skill is a folder of instructions an AI assistant reads when a task matches it — how OGP does CV screening, how to draft an offer, how to query BambooHR. The point of keeping them here rather than in personal setups is that a skill improves every time anyone uses it, instead of rotting in one person's machine.

**New here?** [`index.md`](index.md) lists every skill and who owns it. [`CONTRIBUTING.md`](CONTRIBUTING.md) covers how to add one or improve one.

## Layout

```
skills/<name>/     one folder per skill, each with a SKILL.md
index.md           the map: every skill, purpose, owner, status
nudge.md           canonical improvement-nudge text
CONTRIBUTING.md    how to add a skill, how the improvement loop works
reviewer/          the review agent's prompt and rubrics
.github/           the deterministic checks that run on every PR
```

## How a skill improves

Every skill here ends with an improvement nudge. When a session using that skill hits friction — something out of date, a step that didn't work — the assistant offers to open a PR fixing it. The person says yes; their assistant does the rest.

That's the whole mechanism, and it's why nothing here depends on anyone remembering this repo exists. The nudge is installed automatically after merge, so a contributor who has never read this file still ships a skill that carries it.

## What happens to a pull request

| | What | Where |
|---|---|---|
| On the PR | Refuse secrets, report a missing or stale nudge | `.github/workflows/skills-check.yml` |
| On the PR | Score the change and comment one verdict | [`reviewer/`](reviewer/) — a Claude Code Cloud Routine |
| On merge | Install the nudge, sync the `index.md` row | `.github/workflows/skills-intake.yml` |
| Always | Merge or close | A human. No agent has merge authority |

Checks run on the PR; writes happen after merge. That split is deliberate — this repo is org-visible, so most contributions arrive from forks whose branches an Action cannot write to.

## A note on trust

Anyone in OGP can read this repo, and a skill is executable instruction: it runs with whatever access the person invoking it has. So the reviewer includes a security pass, and the golden rule for readers is the same as for any shared code — **read a skill before you run it.** Skills here are reviewed, not sandboxed.

Never commit a secret. Nothing in this repo needs one; skills that touch an API should route through the credential patterns documented alongside that service, never inline.

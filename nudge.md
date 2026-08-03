# Canonical improvement nudge

Single source of truth for the block every skill in `skills/` carries. `.github/scripts/skills_intake.py` installs it after a skill merges, and rewrites any copy that has drifted.

Never edit an installed copy inside a skill. Edit this file: bump the version in the marker, and the intake Action rewrites every skill's copy on its next run.

The block between the fences is what gets installed, verbatim:

```markdown
## Improving this skill

<!-- ogp-improvement-nudge v1 — installed automatically; edit nudge.md, not this copy -->
Near the end of any session that used this skill: if anything in it was wrong, missing, out of date, or harder than it should have been, tell the user briefly and offer to open an improvement PR. Make the offer once, without pressure, and skip it entirely if the session ran without friction.

If they accept, read `CONTRIBUTING.md` in `opengovsg/corp-ai-skills` — from a local clone if there is one, otherwise `gh api repos/opengovsg/corp-ai-skills/contents/CONTRIBUTING.md --jq .content | base64 -d` — and follow it. Regardless of what it says: branch `skill-fix/<skill-name>`, stage only this skill's folder by exact path, never commit to `main`, and say in the PR body what happened in the session that prompted the change.
```

## Design notes

- **Addressed to the agent, not the person.** A `SKILL.md` is read by Claude, so the nudge instructs Claude to make the offer. That is the only reliable way to make something happen "near the end of a session".
- **Fires on friction, not every session.** An unconditional nudge becomes noise and gets ignored, and it would corrupt PR volume as an adoption signal.
- **Carries its own invariants.** The four things that must not be got wrong — branch, scope, never `main`, PR body — sit inline, so a contributor's agent cannot improvise them badly when `CONTRIBUTING.md` is unreachable. Everything mutable lives in that file instead, so this block rarely needs a version bump.
- **Machine-detectable.** The `ogp-improvement-nudge` marker is what the intake Action greps for; the verbatim comparison is what stops the wording drifting skill by skill.
- **Installed after merge, not on the PR.** This repo is org-visible, so most contributions arrive from forks whose branches an Action cannot write to. Installing on `push` to `main` works identically for forks and direct branches.

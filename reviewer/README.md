# reviewer

The review agent for this repo. A Claude Code Cloud Routine on claude.ai — this folder holds its canonical prompt and rubrics; the routine on claude.ai must match them.

## What it does

Triggered when a Pull Request is opened. If the diff touches `skills/`, it splits deterministically on whether a skill is being added or modified, loads the one matching rubric, and leaves a single comment with a verdict. It never merges.

| Case | Rubric | Checks |
|---|---|---|
| Adds a new `skills/<name>/SKILL.md` | `rubrics/new-skill.md` | security, overlap (trigger collision), genericity, completeness |
| Modifies an existing `skills/<name>/` | `rubrics/improvement.md` | security gate, genericity gate, then route: merge / reference / new skill |

## Why one routine and not two

The claude.ai PR trigger cannot filter by path, branch, or label, so every PR-triggered routine wakes on every PR in the repo. Two reviewer routines would each wake on the other's PRs, and a routing agent can't help — nothing in a GitHub Action can dispatch a specific Cloud Routine.

So this is one routine that wakes once per PR and abandons non-skills PRs in a single step. The new-versus-existing split happens inside it, off the diff, with no judgement involved. Because only one rubric is ever loaded into context, the two rubrics still can't contaminate each other — which is what two separate routines were meant to buy.

## Division of labour

Only judgement lives here. Mechanical work sits in GitHub Actions, which *can* filter by path natively and need no credentials:

- `skills-check.yml` — on the PR: refuse secrets, report a missing or stale nudge. Read-only, so it works on fork PRs.
- `skills-intake.yml` — on push to `main`: install the nudge, sync `index.md`.

## Setup on claude.ai

- Trigger: GitHub → Pull request opened, repo `opengovsg/corp-ai-skills`
- Connector: GitHub (needs PR read, file read, and comment)
- No secrets in the environment box
- Prompt: paste `PROMPT.md` verbatim

## Known limitations

- **Wakes on every PR** and self-filters on the first step. Cheap, but not free.
- The direct-branch PR path used by OGP contributors is verified. Organisation-level forking is disabled; if that policy changes, verify the trigger on a fork PR before relying on that path.
- Same model family as the contributor's assistant, so shared blind spots. This is a filter, not a guarantee — the human is the gate, and the security rubric is not a substitute for reading a skill before running it.

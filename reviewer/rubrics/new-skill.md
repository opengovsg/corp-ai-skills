# New-skill rubric

Applies when the PR adds a `skills/<name>/SKILL.md` that does not exist on base. Four verdicts, reached independently, each one line.

## 1. Security

This repo is readable by everyone in OGP, and a skill is executable instruction: it runs with whatever access the person invoking it has. Review it as you would code you are about to run, not as documentation.

`FAIL` if the skill:

- Runs shell commands whose effect isn't obvious and stated, or builds a command from data it read elsewhere.
- Sends repository content, file contents, credentials, or user data to any external endpoint. Reading from an external source is normal; writing outward is the thing to catch.
- Reads outside its stated scope — the user's home directory, other repos, credential stores, shell history, browser data — without the purpose plainly requiring it.
- Instructs the agent to bypass a confirmation, suppress output, act without telling the user, or continue past an error it should surface.
- Fetches and then executes remote content (`curl … | sh`, downloading a script and running it), or pulls instructions from a URL at runtime.
- Escalates privilege, edits git config or CI configuration, or modifies files under `.github/`.

`FLAG` where the behaviour is legitimate but consequential and the description doesn't warn the user — a skill that deletes, sends email, posts publicly, or writes to a shared system. Name the action and ask whether the human wants it gated behind confirmation.

`PASS` otherwise. Judge intent by effect, not by comments: a reassuring comment above a risky command doesn't change what the command does.

## 2. Overlap

Read `index.md` and the `description` frontmatter of every existing skill in `skills/`.

Judge **trigger collision**, not content similarity. The failure mode of overlapping skills is not duplicated text — it is ambiguous triggering, where the agent loads the wrong skill or loads both. So the question is: given a request that would trigger this new skill, would it also plausibly trigger an existing one?

|  | Same outcome | Different outcome |
|---|---|---|
| **Same triggers** | `FAIL — duplicate of <name>; edit that skill instead` | `FAIL — collides with <name>; both descriptions need disambiguating, or the two should merge with a branch` |
| **Different triggers** | `FLAG — same domain as <name>, different job; proceed with a cross-reference in both descriptions` | `PASS` |

Judge on job-to-be-done. Two skills can share no vocabulary and still collide, or name the same service and be genuinely distinct.

If two skills have different triggers but heavily overlapping bodies, note it: the shared content probably belongs in a reference file both can point at.

## 3. Genericity

The base principle: **a skill stays as general as possible, and reference files carry the specificity.** A skill here must be usable by anyone in OGP, not just its author.

`FAIL` if any of:

- Absolute paths, or paths into a personal vault or machine.
- Assumes one named person's accounts, channels, calendar, or data — unless the skill's stated purpose is genuinely person-specific.
- Hardcoded IDs, dates, or names that plainly belong in intake questions or a config file.
- Instructions that only parse with the author's private context ("as usual", "the normal channel").
- A secret of any kind. The deterministic check catches the obvious shapes, but say so loudly if you see one it missed — anything committed here must be treated as exposed and rotated.

`PASS` otherwise. Naming a service or a shared team resource is fine. Naming *whose* it is, is not.

## 4. Completeness

The test: could someone who has never seen this skill run it end-to-end from the folder alone?

`FAIL` if any of:

- Frontmatter missing `name` (must match the folder) or `description`.
- The description doesn't state both what the skill does *and* the phrases or situations that trigger it.
- Steps reference files, credentials, or connectors without saying where they live. A skill needing credentials must say how to obtain them at runtime, never carry them.
- A step assumes access or context the folder never establishes.

`PASS` otherwise.

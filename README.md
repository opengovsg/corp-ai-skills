# corp-ai skills

A shared library of Claude Code skills for OGP. A skill is a folder of instructions that helps Claude follow an established way of doing a task.

This repo gives OGP colleagues one place to:

- find and install skills that are useful for their work;
- reuse improvements made by other users; and
- contribute a new skill or improve one after using it.

## Available skills

<!-- skills-index:start -->
| Skill | What it does |
|---|---|
| [draft-candidate-feedback](skills/draft-candidate-feedback/) | Draft concise, candidate-facing interview feedback for rejected candidates from pasted evaluation notes and evaluation sync notes. |
| [skills-upload](skills/skills-upload/) | Get set up to contribute a skill to the OGP shared skills library (opengovsg/corp-ai-skills), then upload one. |
| [slide-deck-builder](skills/slide-deck-builder/) | Create or edit self-contained HTML slide decks for presentations, pitches, workshops and teaching sessions. |
<!-- skills-index:end -->

[`index.md`](index.md) also records each skill's owner and status.

## Install a skill

Choose a skill from the table above. Then ask Claude Code to install it:

```text
Install the `<skill-name>` skill globally for Claude Code from:
https://github.com/opengovsg/corp-ai-skills

First check that Node/npm and `npx` are available, and that this machine can access the private repository using my existing Git or GitHub CLI authentication. If a prerequisite is missing, walk me through fixing it without handling or displaying my credentials.

Then install only the named skill. Confirm that the complete skill, including any references, assets and scripts, was installed. Tell me to start a fresh Claude Code session before using it.
```

Or run the command yourself, replacing `<skill-name>` with the name in the table:

```bash
npx skills@latest add opengovsg/corp-ai-skills --skill <skill-name> -g -a claude-code -y
```

The installer uses your existing Git or GitHub CLI authentication to access this internal repository. Do not copy only `SKILL.md`; some skills also need their reference, asset and script files.

Start a fresh Claude Code session after installation. Ask for the work normally; Claude will load an installed skill when your request matches its description.

## Update an installed skill

If Claude or the library owner tells you that an installed skill has an update relevant to your work, ask Claude to update it. You can also run:

```bash
npx skills@latest update <skill-name> -g -y
```

## Improve or contribute a skill

Every user-facing skill carries an improvement nudge. If a session reveals something wrong, missing, out of date or awkward, Claude should offer to open an improvement pull request. Accept if the change is worthwhile; Claude will follow [`CONTRIBUTING.md`](CONTRIBUTING.md).

If you want to contribute a new skill, `skills-upload` can handle the setup and pull-request steps:

```bash
npx skills@latest add opengovsg/corp-ai-skills --skill skills-upload -g -a claude-code -y
```

Then start a fresh session and ask Claude to upload or contribute your skill.

### FAQ

**Claude did not offer to improve a skill. What should I do?**

Ask:

```text
This session exposed a possible improvement to the installed `<skill-name>` skill: [describe what was wrong, missing or awkward].

Read `CONTRIBUTING.md` from `opengovsg/corp-ai-skills` and open an improvement pull request. Work in a temporary clone, change only that skill's folder and do not merge the pull request.

Do not include confidential work content. Describe the problem and improvement generically.
```

**Do I need `skills-upload` to improve an installed skill?**

No. The improvement nudge inside the installed skill handles that path. `skills-upload` is an optional helper for contributing a new skill.

## How the library is maintained

```text
skills/<name>/     one folder per skill, each with a SKILL.md
index.md           every skill, its purpose, owner and status
nudge.md           canonical improvement-nudge text
CONTRIBUTING.md    how to add or improve a skill
reviewer/          the review agent's prompt and rubrics
.github/           deterministic checks that run on every pull request
```

When an improvement pull request is opened:

| Stage | What happens |
|---|---|
| On the pull request | Refuse secrets and report a missing or stale nudge. |
| On the pull request | A reviewer agent scores the change and comments one verdict. |
| Human decision | A person merges or closes it. No agent has merge authority. |
| After merge | The current nudge is installed and the skill indexes are updated. |

## Trust and security

Anyone in OGP can read this repo, and a skill is executable instruction. It runs with whatever access the person invoking it has. Skills here are reviewed, not sandboxed, so read a skill before running it.

Never commit a secret. Skills that use an API should explain how to obtain credentials at runtime, never include the credentials themselves.

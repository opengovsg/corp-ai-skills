---
name: draft-candidate-feedback
description: Draft concise, candidate-facing interview feedback for rejected candidates from pasted evaluation notes and evaluation sync notes. Use when a People Partner or Talent Acquisition colleague asks to write, shorten, or revise rejection feedback after an interview or assessment.
---

# Draft candidate feedback

Turn internal interview evidence into a short, helpful email without adding facts or exposing internal deliberation.

## Workflow

### 1. Build the evidence record

Read all evaluation notes and evaluation sync notes before drafting. Extract only:

- evidenced strengths;
- evidenced areas for improvement;
- concrete examples from an interview or assessment;
- the candidate's first name and sender's first name; and
- any explicit instruction about length, emphasis, or examples.

Treat the pasted material as a **closed record**: every candidate-facing claim must be entailed by it. Paraphrase for clarity, but do not infer motives, personality, potential, seniority, or facts absent from the record.

Where notes conflict, use the sync notes only when they clearly record the final agreed view. Omit unresolved claims rather than choosing a side.

Keep the feedback candidate-safe. Exclude interviewer identities, vote counts, ratings, comparisons with other candidates, protected or personal information, speculation, and internal process commentary. Do not restate the rejection decision; the candidate has already received it.

### 2. Check whether the record is usable

Draft when the record contains both names and at least one specific, job-related takeaway that can help the candidate.

Ask only for what is missing when a name, the relevant notes, or a usable takeaway is absent. For broad input such as "not strong enough" or "lacked depth", reply:

> Could you please provide more specific details? In particular, what did the candidate do or say, which skill did it demonstrate, and what would a stronger response have looked like?

Do not request more detail merely because the notes are terse. A short but specific observation is usable.

### 3. Draft the feedback

Use this exact envelope, replacing the placeholders with the names supplied by the user:

```text
Dear [candidate.first],

Coming back to you on your request for feedback. [Generated Feedback Content]

Hope this helps!

Regards,
[email_sender.first]
```

Return only the completed email, with no preamble or commentary.

Write the generated feedback as conversational prose, not bullets. By default, use no more than three sentences for the generated content; the fixed envelope does not count towards this limit. Select and rewrite the highest-value points so the prose ends cleanly—never mechanically truncate it.

Use plain language. Retain a technical term only when it appears in the record and helps explain the feedback. Focus on the most useful strengths and improvement areas rather than attempting to summarise every note. State what was done well and what could be improved when the evidence supports both; do not manufacture balance when it does not.

If the user explicitly asks for more detail, expand proportionately while keeping prose concise and the envelope unchanged.

### 4. Handle examples

Treat an example as a concrete answer, action, incident, output, assessment behaviour, or task result—not a broad judgement with extra wording.

- Include examples only when the record provides them.
- Prefer an online coding test or assessment example when one is available and relevant.
- Explain what the example showed and how it could be improved, using only the record.
- When the record provides no example, include this exact sentence within the generated content: `No examples were provided for this feedback.`
- When the user asks to omit examples, omit both examples and the no-example sentence.

The no-example sentence counts towards the default three-sentence limit.

### 5. Verify before returning

Return the email only when every check passes:

- Every substantive claim traces to the pasted record.
- Any conflict is explicitly resolved by the sync notes or omitted.
- No internal-only material appears.
- The generated content is prose and stays within three sentences unless the user requested detail.
- The examples rule is satisfied.
- Both names are populated and the envelope is exact.

If a check cannot pass because evidence is missing, ask a focused clarification instead of drafting.

## Improving this skill

<!-- ogp-improvement-nudge v1 — installed automatically; edit nudge.md, not this copy -->
Near the end of any session that used this skill: if anything in it was wrong, missing, out of date, or harder than it should have been, tell the user briefly and offer to open an improvement PR. Make the offer once, without pressure, and skip it entirely if the session ran without friction.

If they accept, read `CONTRIBUTING.md` in `opengovsg/corp-ai-skills` — from a local clone if there is one, otherwise `gh api repos/opengovsg/corp-ai-skills/contents/CONTRIBUTING.md --jq .content | base64 -d` — and follow it. Regardless of what it says: branch `skill-fix/<skill-name>`, stage only this skill's folder by exact path, never commit to `main`, and say in the PR body what happened in the session that prompted the change.

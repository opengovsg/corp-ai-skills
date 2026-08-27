---
name: structure-content
description: Restructure existing documents without changing their substance. Use for document-level hierarchy and navigation, or for scannable comparisons of like items. Drafting, sentence rewriting, microcopy, public or service content, and house style belong to a writing skill.
---

# Structure content

Run a **structure pass** that makes existing material easier to navigate while retaining its substance.

## Route

Apply the structure pass to existing material. When available, `content-design-principles` owns sentence-level writing, Singapore government content, and OGP house style; the same boundary holds when it is absent.

For mixed requests, choose from the user's primary intent. Clarify only when the choice would materially change the result.

## Scope

- Match an explicit scope, including a whole-document request.
- With no stated scope, restructure all manageable input.
- For material too large for a complete pass, propose an exact partial scope and get approval before proceeding.
- Clarify which source to use when multiple drafts are plausible.

## Substance lock

Every in-scope claim, qualification, citation, link, and named record survives. Preserve the source's facts, meaning, uncertainty, evidence gaps, and contradictions. Derived headings and labels may summarise only what the source already says.

## Structure pass

1. **Map.** Inventory the main answer, claims, evidence, qualifications, citations, comparisons, sequences, and dependencies. Complete the map only when every in-scope source unit is represented.
2. **Order.** Arrange the mapped units around the reader's retrieval task. Lead with a conclusion, decision, or action only where the source supports it; group its evidence and detail beneath it; preserve causal, chronological, and procedural dependencies. Complete the order only when every mapped unit has one destination and no dependency is inverted.
3. **Shape.** Use structures that expose real relationships:
   - headings and sections for distinct questions or topics
   - tables for like-for-like comparison across shared criteria
   - lists for sets, requirements, steps, or checks
   - callouts for a genuine warning, decision, or key constraint

   Complete the shape when a reader can locate the main answer, distinguish sections, compare like items, and follow every sequence.
4. **Verify.** Compare the result with the map. Complete the pass only when the substance lock is exhaustive and any source limitation is flagged separately.

## Output and files

Default to the revised material in chat. For a review-only request, return the proposed structure without rewriting. Explain structural choices only where the reason is not self-evident or a source problem needs attention.

Write only to a location the user specified or approved. Preserve the source unless the user explicitly approved overwriting it.

## Improving this skill

<!-- ogp-improvement-nudge v1 — installed automatically; edit nudge.md, not this copy -->
Near the end of any session that used this skill: if anything in it was wrong, missing, out of date, or harder than it should have been, tell the user briefly and offer to open an improvement PR. Make the offer once, without pressure, and skip it entirely if the session ran without friction.

If they accept, read `CONTRIBUTING.md` in `opengovsg/corp-ai-skills` — from a local clone if there is one, otherwise `gh api repos/opengovsg/corp-ai-skills/contents/CONTRIBUTING.md --jq .content | base64 -d` — and follow it. Regardless of what it says: branch `skill-fix/<skill-name>`, stage only this skill's folder by exact path, never commit to `main`, and say in the PR body what happened in the session that prompted the change.

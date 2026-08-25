# Claude deck workflow

Use this branch only in Claude or Claude Code. Complete every gate; resolve relative paths from the skill root.

## Plan from the brief, not the reference

Inspect `assets/ogp-slides/calibration-reference.png` for scale, rhythm and canvas confidence. It is a quality bar, not a template: create a new narrative and layout sequence. Every large field must carry content, hierarchy or meaning.

Before coding, record the communication job, cumulative narrative and one-sentence composition intent per slide in a build note. If the user asks only for a “test deck”, make a design-system specimen with explicitly illustrative copy; do not invent an explainer or factual claims about the organisation.

Use extended reasoning. Start only when every slide has a distinct narrative job and the planned silhouette sequence does not reproduce the calibration reference. Consult `references/visual-components.md` only for a genuine content need.

## Build and substantiate

Author HTML and PPTX natively, sharing only the narrative and design system. Preserve notes across formats.

Verify wording, examples, numbers and diagrams. Every non-trivial external claim needs a real URL or a named user-provided source in a non-visible HTML comment or PPTX note; “general knowledge” is not provenance. Remove or qualify anything uncertain.

## Prove the revision

After the first complete export, create `deck-review.md` in the working directory with one row per slide: `slide | finding | action | verified`. Each finding must explicitly cover hierarchy, back-row legibility, canvas/whitespace, silhouette and accuracy; use `none — <specific reason>` only when clean.

1. Render every slide full-size and complete every review row from the render.
2. Resolve every material finding, then rerender every changed slide and mark it verified.
3. For HTML, run `node <skill-root>/scripts/audit-html-rendered.mjs <deck> --review <review> --against <skill-root>/assets/ogp-slides/calibration.html`. For PPTX, run `python3 <skill-root>/scripts/audit-pptx.py <deck>`, adding `--ogp` for OGP.
4. Inspect the final full-size slides individually and the montage for deck-level rhythm.

An unavailable render or audit blocks delivery. Completion requires passing audits, a complete verified review, resolved findings, sourced claims and a coherent final montage. Remove the temporary build note and review only after reporting the completed gates.

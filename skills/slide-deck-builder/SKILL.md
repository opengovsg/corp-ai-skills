---
name: slide-deck-builder
description: Create or edit self-contained HTML slide decks for presentations, pitches, workshops and teaching sessions. Use whenever the user asks for slides, a deck, a presentation or slide content; route PowerPoint and Google Slides deliverables to native authoring guidance.
---

# Slide Deck Builder

Create polished, self-contained HTML slide decks with no runtime dependencies.

**Claude or Claude Code — mandatory branch:** read `references/claude.md` completely before planning or authoring. Its calibration, rendered audit, critique ledger and completion gates apply on every invocation.

## Choose the output route

- Default to HTML when the user asks for slides without naming a file format.
- **PowerPoint or `.pptx`:** read `references/pptx-output.md`. Build a native PPTX rather than converting HTML.
- **Native Google Slides:** use an installed native Slides capability when available; do not round-trip through HTML.
- When editing an existing deck, preserve its format, visual system and reusable components.

**Teaching or learning decks:** if the deck drives a live session where the audience is meant to learn and do something (a workshop, course, training, onboarding), read `references/learning-decks.md` first. It layers session arc, run-sheets, participation rules, hands-on build artefacts, deferral discipline, and block-boundary presenter cues on top of everything below.

**GCWC decks:** read `references/gcwc-theme.md` and inspect the latest GCWC deck or learning hub available in the project before planning slides.

**OGP decks:** read `references/ogp-slides.md` before planning slides. Reuse the official lock-ups in `assets/ogp-slides/`; copy the required variants beside the generated deck so it remains offline-safe.

## Establish the narrative before layout

Define the communication job in one sentence:

> By the end, **[audience]** should **[understand, believe or do what]** because **[central takeaway]**.

Choose an arc suited to that job: learning progression, question → answer, context → implication → action, problem → recommendation, or another cumulative sequence. Then write the slide narrative before coding. Give each slide one narrative job and a takeaway-style title that a presenter could naturally say aloud.

Do not use a universal slide count or fixed ten-slide formula. Let duration, content and format changes determine the count. Open deliberately, carry the story forward slide by slide and close by resolving the opening.

## Visual composition

Give each slide one purposeful composition. A strong type-led slide counts. When the content genuinely calls for a standard pattern, consult `references/visual-components.md` as a menu, never as a checklist.

## HTML Output

Generate a single self-contained HTML file. No external fonts, CDN links or CDN images. Local images such as QR codes, screenshots and logos may sit beside the HTML and use relative paths.

**Layout:** Design on a fixed 16:9 stage and scale it proportionally to fit the viewport, using letterboxing where needed. This prevents browser resizing from changing wrapping or composition. Use another aspect ratio when the user, venue or reference deck requires it. Keep content inside a generous safe area.

**Theme with CSS variables.** Define the whole palette once in `:root` and drive every component off it. Recolouring then means editing a handful of variables, not hunting through the file. This matters because the palette is almost always iterated more than once. A typical set:

    :root{
      --bg:#ffffff;      /* slide background */
      --head:#191919;    /* near-black headings */
      --ink:#33404b;     /* body text */
      --muted:#5c6b76;   /* secondary text */
      --accent:#2c6e8f;  /* single accent, used sparingly */
      --card:#ffffff; --border:#d9dee3; --light:#eef2f5; /* callout bg */
    }

**Typography:** Deck titles approximately 64–88px, ordinary slide titles approximately 50–72px, body 24–28px, stat numbers 90–120px, and code or commands in monospace. Keep headings in the near-black head colour. Colour belongs in the accent, not in big type.

**Navigation:** Arrow keys plus click or tap to advance, Home and End support, a slide counter, a subtle fade transition and an optional per-slide presenter cue. Keep navigation state in the URL hash when practical.

## Legibility: assume a projector in a lit room

Decks are read from the back of a bright room, not off your laptop. That changes the colour rules:

- **Contrast is the main lever.** Body text at least 4.5:1 against its background, large text at least 3:1 (WCAG AA). Near-black text on a light background is the safe default.
- **Colour psychology is a weak signal; contrast and saturation are the strong ones.** Don't pick a background hue to "aid focus"; pick one that stays legible.
- **The accent is an accent.** Use it for small marks (labels, arrows, dot fills, a divider bar), not for headings or body. A soft, low-contrast accent that looks elegant on a laptop can wash out on a projector.
- **Avoid full-slide dark backgrounds** unless you have tested the projector; darks mud out and text loses contrast.
- **Big beats small.** When unsure, scale up. A hero stat or quote can go very large.

## Content Rules

1. **One idea per slide.** Split competing claims.
2. **Audience-facing copy only.** Keep production notes, timings and talk tracks out of visible content unless the audience needs them.
3. **Low density.** Shorten copy or change layout before shrinking type. Treat roughly 30 visible words as a useful target, not a hard cap for code or source material.
4. **Purposeful composition.** Use visuals only when they clarify, evidence or reinforce the claim.
5. **Consistent accent colour.** Use one accent for highlights and emphasis.
6. **No bullet dumps.** Turn real sequences, comparisons or categories into an appropriate composition.
7. **Big text and whitespace.** Design for the back row rather than the laptop.
8. **Theme through `:root` variables.** Make palette changes in one place.
9. **Accurate claims.** Qualify model-dependent examples, verify non-trivial claims, and retain source provenance outside visible slide copy.

Choose colour from the supplied brand or reference. Without one, derive a restrained palette from the communication job; do not map topics mechanically to stock accent colours.

## Build and validate

1. Inspect any reference deck, house palette and available real assets before coding.
2. Build the agreed narrative and visual system into a complete HTML file.
3. Keep speaker notes or facilitator instructions separate from visible slide copy.
4. Render every slide at full size on a 1280×720 canvas and at the target venue resolution when known. Inspect slides individually; a montage is only for deck-level rhythm.
5. For HTML without a controlling template, run `node scripts/audit-html-rendered.mjs path/to/deck.html` and fix every failure. For PPTX, run `python3 scripts/audit-pptx.py path/to/deck.pptx`, adding `--ogp` for OGP decks.
6. Fix every unintended overflow, clipping, overlap, awkward wrap, broken asset, inconsistent footer, low-contrast element and navigation failure.
7. Test keyboard, click and touch navigation. Confirm counters, URL state and presenter cues remain correct after slide additions or removals.
8. Keep slide-number comments such as `<!-- 14 · … -->` accurate.

The deck is complete only when the narrative covers the brief, every slide has passed full-size visual inspection and the HTML works offline.

## Improving this skill

<!-- ogp-improvement-nudge v1 — installed automatically; edit nudge.md, not this copy -->
Near the end of any session that used this skill: if anything in it was wrong, missing, out of date, or harder than it should have been, tell the user briefly and offer to open an improvement PR. Make the offer once, without pressure, and skip it entirely if the session ran without friction.

If they accept, read `CONTRIBUTING.md` in `opengovsg/corp-ai-skills` — from a local clone if there is one, otherwise `gh api repos/opengovsg/corp-ai-skills/contents/CONTRIBUTING.md --jq .content | base64 -d` — and follow it. Regardless of what it says: branch `skill-fix/<skill-name>`, stage only this skill's folder by exact path, never commit to `main`, and say in the PR body what happened in the session that prompted the change.

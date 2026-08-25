# PPTX output

Use this reference when the requested deliverable is PowerPoint or `.pptx`.

## Hand-off contract

1. Apply this skill's narrative, content and visual-composition rules. Read every relevant branch reference, such as `learning-decks.md`, `gcwc-theme.md` or `ogp-slides.md`.
2. If the environment has a native presentation skill, read and follow it. In Codex, use the installed `Presentations` skill. Otherwise read [`native-pptx-authoring.md`](native-pptx-authoring.md) as the complete portable contract.
3. Build the presentation natively as PPTX. Use HTML only as a separately requested deliverable, never as an intermediate converted into PowerPoint.

## Choose the native visual route

Follow the first matching route:

- **Existing PPTX, template or reference deck:** preserve its master, layouts and inherited elements through the template-following route.
- **Explicit house style or brand direction:** build a custom native deck from that direction. For OGP, apply `ogp-slides.md` and reuse the official assets in `assets/ogp-slides/`.
- **No visual direction:** use the environment's presentation layout library when available; otherwise compose from first principles using the portable reference.

## Preserve the design intent

- Translate the narrative and composition into editable PowerPoint text, images, shapes and speaker notes.
- Keep logos and supplied media as real assets rather than approximating them with drawn shapes.
- Preserve speaker notes and add source blocks for externally sourced claims and assets.
- Maintain the requested aspect ratio; use 16:9 when none is specified.

## OGP typography

For an OGP PPTX, use `Helvetica Neue` as both the PowerPoint theme font and the explicit typeface for every text object. OGP uses macOS, where Helvetica Neue is available. Then run:

```bash
python3 scripts/set-pptx-font.py path/to/deck.pptx --font "Helvetica Neue"
```

The script aligns the theme and slide text, and removes stale embedded-font payloads that can trigger misleading font names with substituted glyphs. PowerPoint has no CSS-style font stack; use `Arial` instead when the audience is not on OGP-managed Macs. Re-render after any typeface change because font metrics change wrapping.

## Completion

Render and inspect every slide individually, run the native overflow and overlap checks, then run `python3 scripts/audit-pptx.py path/to/deck.pptx` and fix every failure. Add `--ogp` for OGP decks. Deliver the final `.pptx`; include HTML only when the user explicitly asks for both formats.

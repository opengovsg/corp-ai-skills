# Native PPTX authoring

Use this portable contract when the environment has no dedicated presentation skill. It captures the decisions and completion standards required for a native PowerPoint deliverable without assuming Codex or a particular library.

## Route

Follow the first matching route:

1. **Existing PPTX, template or reference deck:** preserve its masters, layouts, theme, fonts and inherited elements. Duplicate suitable layouts and edit their placeholders or objects in place.
2. **Explicit visual direction:** build an editable native deck from that direction. Treat supplied brand assets and palette as controlling constraints.
3. **No visual direction:** compose a restrained 16:9 deck from first principles with equal margins, clear hierarchy and varied slide silhouettes.

Never convert HTML screenshots into PowerPoint. Text, shapes, tables, charts and notes should remain editable. Keep logos and media as real assets.

## Plan before authoring

Define one communication job:

> By the end, **[audience]** should **[outcome]** because **[central takeaway]**.

Choose a cumulative arc suited to that job. Give every slide one narrative job and a takeaway-style title. Open with the reason the deck matters; close by resolving it. Keep visible copy audience-facing and keep production notes out of the canvas.

## Authoring defaults

- Use 16:9 unless the brief or reference specifies another ratio.
- Keep equal left and right margins and one dominant composition per slide.
- Keep titles on one line when the design intends one line; shorten copy or change layout before shrinking type.
- Without a controlling template, use at least 50 pt for deck titles, 40 pt for slide titles, 24 pt for subheads and 18 pt for body copy.
- Prefer light backgrounds and projector-safe contrast.
- Avoid dense dashboards and repeated UI-style cards unless the content genuinely requires them.
- Use simple native shapes for simple processes. Use charts for quantitative relationships, not decoration.
- Add source notes for externally sourced claims and assets.

## Fonts

Set a real typeface in both the theme and slide text.

- PowerPoint does not support a CSS-style ordered fallback list.
- Choose a typeface installed on the target machines and re-render the entire deck because substitutions change line breaks and object fit.
- For OGP, use Helvetica Neue in both the theme and every text object via `scripts/set-pptx-font.py`; use Arial for cross-platform delivery.

## Native implementation

Use the environment's most reliable PPTX authoring library or application. The implementation must support:

- editable text, shapes, images, tables and charts;
- slide size, masters or layouts, and theme fonts;
- speaker notes when the deck needs presenter guidance or citations;
- deterministic export to `.pptx`;
- rendering every slide to an image for QA.

Keep temporary renders, layouts and inspection files outside the final output folder. Preserve the source file when editing and export a copy unless the user requests an in-place change.

## QA gate

The deck is complete only when all of these are true:

1. Every slide has been rendered at full size and inspected individually.
2. No unintended overlap, clipping, overflow, awkward wrap, broken asset or unresolved placeholder remains.
3. Titles, logos, footers and slide numbers are consistent.
4. Charts and tables match their data and labels.
5. The narrative covers the brief and the closing resolves the opening.
6. Theme and explicit slide typefaces have been inspected inside the PPTX package.
7. `scripts/audit-pptx.py` passes; for OGP, it passes with `--ogp`.

Use a montage only to judge deck-level rhythm; it does not replace full-size inspection.

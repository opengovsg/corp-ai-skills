# OGP slides

Use this reference for Open Government Products decks. It translates the official OGP Brand Guidelines 2025 into presentation-scale rules.

## Identity assets

Use only the bundled official horizontal lock-ups:

- `assets/ogp-slides/logo-hori-default.svg` — blue mark with black wordmark for white and pale-grey surfaces.
- `assets/ogp-slides/logo-hori-white.svg` — white reverse lock-up for OGP Blue or black surfaces.

Copy the required variants into the generated deck's own asset folder and use relative paths. This keeps output offline-safe and prevents it from depending on the skill's installation path.

Preserve the full lock-up. Keep its aspect ratio and clear space; do not recreate, crop, recolour, rotate, stretch, add effects or separate the wordmark from the mark.

## Palette

Use OGP Blue as the primary colour. Use its tints and neutral greys for supporting surfaces; use red only for semantic emphasis.

```css
:root {
  --ogp-blue-50: #F7F9FE;
  --ogp-blue-100: #E1EBFD;
  --ogp-blue-200: #ACC7FA;
  --ogp-blue-300: #82ABF7;
  --ogp-blue-500: #276EF1;
  --ogp-blue-600: #0D4FCA;
  --ogp-blue-700: #0B44AC;
  --ogp-blue-800: #093890;
  --ogp-blue-900: #072A69;
  --ogp-dark: #1D1D1D;
  --ogp-grey-50: #F9F9F9;
  --ogp-grey-100: #E9E9E9;
  --ogp-grey-200: #BFBFBF;
  --ogp-grey-500: #686868;
  --ogp-grey-600: #535353;
  --ogp-white: #FFFFFF;
  --ogp-red: #FB5D64;
}
```

Use `#276EF1` for the title slide and strong structural accents. Keep most content slides white, using blue tints for comparison panels, steps and quiet emphasis. Prefer near-black text on light surfaces for projector contrast.

## Typography and composition

- Inspect `assets/ogp-slides/calibration-reference.png` for scale, rhythm and canvas utilisation. Treat it as a quality bar, never a layout source.
- **HTML:** use `Inter, "Helvetica Neue", Arial, sans-serif` without loading a remote font.
- **PPTX:** use `Helvetica Neue` in the theme and explicitly on every text object. Read `pptx-output.md` and run `scripts/set-pptx-font.py` after native export. PowerPoint cannot store an ordered fallback stack; use `Arial` instead when cross-platform portability matters more than the OGP macOS standard.
- Use tightly tracked, bold headings at presentation scale: approximately 60–88px at 1280×720.
- Use generous whitespace and a 1280×720 stage with approximately 80px horizontal safe margins.
- Prefer clean white space, tonal surfaces and simple rules over shadows or decorative texture.
- Use one dominant composition per slide: type, comparison, flow or a small card group.
- Keep product-interface chrome out of the slide vocabulary unless showing a real interface.

## Logo placement

- **Title slide:** use the white reverse lock-up at the top-left on a full OGP Blue background, approximately 220px wide.
- **Ordinary content slides:** use the default lock-up consistently at the top-left, approximately 150px wide. Keep it visually subordinate to the slide title and preserve clear space.
- **Closing slide:** use the default lock-up at the top-left, approximately 210px wide when the closing title is larger than ordinary slide titles.
- Keep the slide number at the bottom-right.
- Use one logo placement per slide; do not combine header and footer lock-ups.

## Template family

**Title:** OGP Blue canvas; reverse logo top-left; one large outcome-oriented title; optional short subtitle.

**Content:** white canvas; compact default logo top-left; takeaway title aligned to the left grid; one dominant visual treatment; restrained blue accents.

**Section divider:** white or pale-blue canvas; compact default logo top-left; small blue section label; large dark title; minimal supporting content.

**Closing:** white canvas; default logo top-left; resolve the opening with one final takeaway or action. Add a tonal field only when it carries information or hierarchy.

## Validation

Render every slide at 1280×720. For HTML run `node scripts/audit-html-rendered.mjs path/to/deck.html`; for PPTX run `python3 scripts/audit-pptx.py path/to/deck.pptx --ogp`. Check that both logo variants load offline, retain their proportions and remain on clean backgrounds. Confirm that content-slide logo sizing is consistent, every slide number is present, and all text meets projected contrast requirements. For PPTX, inspect the package to confirm Helvetica Neue in both theme font slots and every slide's explicit Latin, East Asian and complex-script run properties; confirm there is no stale embedded-font list or font payload.

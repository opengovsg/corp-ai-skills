# Learning and teaching decks

Read this when the deck drives a live *learning* session: a workshop, course, training, or onboarding, where the audience learns something and does something rather than just watching. GCWC (Getting Comfy with Claude) is the running example, but the patterns apply to any teaching topic.

Everything in the parent `SKILL.md` still holds (self-contained HTML, `:root` theming, projector legibility, one idea per slide). This file adds what teaching decks need on top.

## Design from a run-sheet, not a slide count

Start from time, not slides. Block out the session by minutes and format before writing a single slide:

| Min | Block | Format |
|--|--|--|
| 5 | Open, why this matters | Slides |
| 10 | Teach one concept | Slides |
| 10 | Check understanding | Poll or quiz |
| 20 | Do it in teams | Breakout + share-back |
| 15 | Hands-on build | Guided from a starter prompt |
| — | Buffer | — |

Budget teachable minutes and leave real buffer; live sessions always overrun. The slides serve the run-sheet, not the reverse.

## Write the complete slide narrative

Before coding, map every slide to the run-sheet. Record:

- time block and format;
- narrative job and audience-facing takeaway title;
- visible content and visual treatment;
- facilitator notes or transition cue; and
- participant action or leave-with output, where relevant.

Keep timings and facilitator notes out of visible slide copy unless participants need them. The narrative is complete when every run-sheet block has the slides, mechanics and output needed to run it.

## Session arc (multi-session programmes)

- **Compounding.** Each session ends with something the participant keeps, and that output becomes the next session's starting point. Name one leave-with artefact per session and carry it forward.
- **Name continuity.** If this builds on a prior programme or session, say so on an early slide: what they can already do, what is new now.
- **Direction vs task-fit.** Keep aspirational "where this is going" claims separate from "which tool for which job" teaching, so the two never contradict each other in the room.

## Participation rules

- **Never cold-call individuals.** No "who wants to volunteer?" Use anonymous polls (e.g. Menti) and team outputs only.
- **Team share-backs, not solo performances.** Don't over-constrain the share-back ("one line each") unless time is genuinely tight.
- **Bake activity mechanics into slides:** a poll slide with join code, QR and prize; a team-discussion slide with the exact questions; a build slide with the prompt.

## Presenter cues in the footer

General decks can show `Next → …` on each slide. Teaching decks should also mark **block boundaries** with a distinct, stronger cue (`Next section → …`, in a solid or inverted style). It is a stop-signal: the point where the facilitator pauses, checks the room, or switches format. Knowing where the seams are is worth more to a facilitator than to a keynote speaker.

## Deferral discipline

Beginners drown if you show them everything. For each advanced topic that tempts you:

- **Defer it and name the owning session in the slide** ("the controls come in session 3"). This reassures without teaching.
- **"Use before understand" is fine.** Let them use a connector today and learn what it actually is later; say so out loud.
- **Keep definitions to one line with a pointer** ("a skill is a saved set of instructions Claude runs on command; we go deeper in session 2").

## Teach the discriminating question

For any "which one, and when" topic, teach the *question the learner asks themselves*, not a lookup table. Give it as a single lens ("does this need to live somewhere and keep working?"), then let a sorting activity exercise it. The lens is the transferable skill; the table is not.

## Hands-on builds

- **Give a starter prompt to fill in, not a blank page.** Show placeholders (`[like this]`) for the parts they personalise.
- **Put complete prompts on the learning hub.** Projected slides show the short action, any single command required and where to find the copyable prompt.
- **One participant command or action per slide.** Split the safety caveat, command and follow-up. This rule applies to learning decks, not general presentations.
- **Set the honest expectation** of what v1 will and will not do, so the result does not disappoint.

## Placeholders to leave in the deck

Some things only exist on the day. Leave clearly-marked placeholders so nothing is forgotten:

- Attendance QR (embed the real PNG once you have it; a placeholder box until then).
- Poll join code, address, and prize.
- Anything that needs the room (whiteboards, breakout groupings).

## Colour for learning, the honest version

There is no magic "focus" hue. The evidence for colour-psychology effects on learning is weak. What reliably helps is legibility: high contrast, restrained saturation, one calm accent, near-black headings on a light background. Choose the palette for the back row of a lit room, not for mood. (See parent `SKILL.md`, Legibility section.)

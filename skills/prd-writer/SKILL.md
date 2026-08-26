---
name: prd-writer
description: Draft proportional mini-PRDs for new products or flows. Use when the user asks for a PRD or wants to turn a bounded intervention into a hypothesis and evidence of success.
---

# Mini-PRD Writer

A mini-PRD makes work legible: why it matters, what change is proposed, why that change should work, and what evidence would change our confidence. The why is load-bearing; measurement serves it.

## Steps

1. **Check the fit.** A PRD belongs to a bounded product or flow intervention that supports a real hypothesis: _if X, then Y, because Z_. Route a stance to a charter or policy, diagnostic or coordination work to strategy, a choice between options to a decision memo, and recurring operations to a runbook. Proceed once the intervention and intended outcome are clear.

2. **Establish the why.** Read the prompt and relevant context. Articulate the problem, why it matters now, the intended outcome, and the causal reason this intervention should produce it. Ask only about gaps that could change that reasoning. Continue when the hypothesis is specific and non-tautological, with genuine uncertainty named.

3. **Find useful evidence.** Start with existing operational data and any relevant central outcome metric. Choose the smallest set of signals that could confirm, falsify, or update the hypothesis. Add a baseline, target or desired direction, and review point where meaningful. When quantification would create metric theatre, use observable qualitative evidence or a learning question and explain the limitation.

4. **Draft proportionally.** Give every mini-PRD a clear why, intervention and hypothesis, and evidence of success. Add users, scope, non-goals, assumptions, risks, rollout, ownership, or other material only when it helps readers understand or execute the work.

5. **Pressure-test.** Challenge the _because_ clause and whether the chosen evidence tracks the outcome rather than activity. Revise until the causal claim survives the challenge or its weakness is explicit.

6. **Deliver.** Save where the user requested; otherwise write `prd.md` in the current working directory. The mini-PRD is complete when a reader can explain why the work exists, how the intervention is expected to cause the outcome, and what evidence would change the decision.

## Shapes, if one helps

Read a template only when the reader needs a shape the six steps above don't already give them. A template is a checklist of what to consider, never a set of headings to fill in.

- `references/intervention-template.md` — programmes, process, behaviour change. Carries the three-line theory of change and the guardrail-metric framing.
- `references/build-spec-template.md` — automations, builds, vendor work. Carries the functional/non-functional split and the kill criterion.
- `references/procurement-appendix.md` — append when the PRD goes to Corp team or vendor purchase approval. Carries the SVP justification and cost reasonableness sections OGP procurement expects; there is no way to reconstruct these from first principles.

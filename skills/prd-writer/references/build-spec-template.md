# Build-Spec PRD template

For automations, scripts, features, or vendor integrations. Structured around requirements, alternatives, and technical considerations.

British English. Em dashes only where they earn their place. Standard markdown only.

---

```markdown
# [Project name]

**Owner:** [name]   **Status:** Draft   **Last updated:** [date]

---

## TL;DR
3 to 4 sentences.

## Background
Problem and context. What triggered this. What is in place today and why it is not working. ~150 words.

## Goals
Bulleted. Each goal measurable or observable.

## Non-goals
Bulleted.

## Users and use cases
Short list or table.

## Requirements

### Functional
Numbered list.

### Non-functional
Numbered list. Performance, security, access control, auditability, data residency. If genuinely none, write "N/A" with a one-line reason.

### UX notes
Where the tool lives, how users access it, key flows.

## Alternatives considered

| Option | Why considered | Why ruled out |
|---|---|---|
|  |  |  |

At least two.

## Assumptions
*What we believe* then *what we are betting on* then *what would prove it wrong*.

## Technical considerations
Build vs integrate vs buy. Systems touched, credentials, data flow, known constraints.

## Success metrics (mandatory table)

| Metric | Baseline | Target | Timeline |
|---|---|---|---|
|  |  |  |  |

Include a kill criterion.

## Risks and trade-offs
Each as: "We chose X over Y because Z. The cost is W."

## Rollout and ownership
How this ships. Who owns it after launch. Manual fallback. Owner rotation plan.

## Open questions
Things deferred. Each with an owner or decide-by date.
```

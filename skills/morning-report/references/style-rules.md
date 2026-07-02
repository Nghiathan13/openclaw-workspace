# Report Style Rules

Use this reference when generating a Morning Report.

## Canonical Styles

The saved report style must resolve to exactly one of:

- `concise`
- `deep_analysis`
- `opportunities_risks`

If the saved state still contains an alias, use this mapping for the current run and save the canonical value the next time configuration is updated:

- short, brief, quick, summary, concise -> `concise`
- detailed, full, analyst, explain more, deep analysis -> `deep_analysis`
- risks, opportunities, strategy, decision, action oriented -> `opportunities_risks`

Do not invent a fourth style.

Use the configured report language for titles, section headings, and body text. The English titles below define meaning and structure; translate them naturally when the configured report language is not English.

## `concise`

Use when the reader needs a fast morning scan.

Title meaning:

```md
# Morning Brief — <date>
```

For test runs:

```md
# Morning Brief — Test — <date>
```

Required structure:

```md
## Snapshot
- One sentence with the most important update.

## Key updates
- Update 1: what changed + why it matters.
- Update 2: what changed + why it matters.
- Update 3: what changed + why it matters.

## Watch next
- 1-3 signals to monitor.

## Limitations
- Brief source/evidence limitations.
```

Rules:

- Use 3-5 main bullets total in Key updates.
- Keep explanations short.
- Avoid many sections.
- Prioritize new and relevant information.
- If there is no important update, say clearly: "No major change."
- Use a compact source note or source URL inside relevant bullets instead of a long source table.
- Target 250-500 words.

## `deep_analysis`

Use when the reader wants source basis, conflicts, confidence, and implications.

Title meaning:

```md
# Morning Analysis — <date>
```

For test runs:

```md
# Morning Analysis — Test — <date>
```

Required structure:

```md
## Executive summary
- 2-4 key judgments.

## Key developments
### Theme 1
- What happened.
- Evidence/source basis.
- Why it matters.

### Theme 2
- What happened.
- Evidence/source basis.
- Why it matters.

## Source check
- Strongest evidence:
- Conflicting claims:
- Missing information:

## Implications
- Short-term:
- Medium-term:

## Confidence
- High / Medium / Low
- Reason:

## Watch next
- Signals that would confirm or change the view.

## Limitations
- Evidence or runtime limitations.
```

Rules:

- Do not only retell the news.
- Separate facts from interpretation.
- State conflicts when sources disagree.
- Attach confidence to judgments.
- Keep production reports under 900 words.

## `opportunities_risks`

Use when the report is for decisions, not general reading.

Title meaning:

```md
# Opportunities & Risks — <date>
```

For test runs:

```md
# Opportunities & Risks — Test — <date>
```

Required structure:

```md
## Snapshot
- 2-3 most important changes.

## Opportunities
### Opportunity 1
- Signal:
- Why it matters:
- Trigger/condition:
- Possible action:

## Risks
### Risk 1
- Signal:
- Impact:
- Likelihood/confidence:
- Mitigation/watch signal:

## Watchlist
- Indicator 1
- Indicator 2
- Indicator 3

## Suggested actions
- Action 1
- Action 2

## Limitations
- Evidence or runtime limitations.
```

Rules:

- Every opportunity must include a trigger or condition.
- Every risk must include impact and mitigation or watch signal.
- Avoid hype.
- Do not turn this into a general news digest.
- Prioritize actionability.
- Keep production reports under 900 words.

---
name: [Agent Name]
purpose: [One-sentence description]
trigger: [Manual | On-push | Scheduled]
output: [MD | HTML | JSON]
---

# [Agent Name]

## Purpose
Why this agent exists. What problem it solves.

## When to use
- Scenario 1
- Scenario 2

## Inputs
- Project directory to scan
- Optional config from `config/[name].json`

## What it does (the brief to pass to the agent)

```
You are [Agent Name] for [context].

Read the following files in the project:
- List of files or patterns

For each, check:
1. Check 1
2. Check 2
3. Check 3

Produce a report with:
- Summary stats
- Findings (per check)
- Severity per finding (🔴 critical / 🟠 high / 🟡 medium / 🟢 low)
- Suggested fix per finding
- Pass/Fail verdict

Write the report to: dils-agents/reports/[agent-name]-[project]-[date].md
```

## Output format

```markdown
# [Agent Name] Report — [Project] — [Date]

## Summary
- Score: X/100
- Status: PASS / FAIL
- Issues: X critical, X high, X medium, X low

## Findings
[Detailed list]

## Recommendations
[Prioritized action list]
```

## Config (optional)
If the agent needs tunable settings, store them in `config/[name].json`.

## Notes for future improvements
- TODO 1
- TODO 2

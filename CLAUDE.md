# DILS Agents — Claude Code Project Context

## What this project is
A collection of specialized AI agents that run against any project in `C:/Automation/Github/`. Each agent is a markdown file describing its purpose, brief, and output format. Claude reads the agent file and executes it.

## Key facts for Claude

- **Cross-project scope** — agents here scan OTHER repos (investment-tracker, dnd-tracker, future projects)
- **No build, no runtime** — pure markdown specs + JSON config
- **Agents are disposable workers** — each invocation starts fresh, gets a complete brief, produces a report
- **Reports land in `reports/`** — HTML preferred, MD acceptable

## Project structure

```
dils-agents/
├── CLAUDE.md                # this file (auto-loaded context)
├── README.md                # human-facing intro
├── agents/                  # agent definitions
│   ├── dils-quality-checker.md   ⭐ flagship — pre-CTO-handoff QA gate
│   ├── security-auditor.md       OWASP + RLS deep scan
│   ├── learning-tracker.md       Noah's skill progression
│   └── template.md               for creating new agents
├── config/
│   ├── dils-standards.json       DILS quality thresholds
│   └── skill-taxonomy.json       skill tree definition
└── reports/                 # generated HTML reports
```

## How to invoke an agent

When the user asks to run an agent:
1. Read the agent's `.md` file in `agents/`
2. Read the relevant config from `config/` if mentioned
3. Identify the target project (current directory or specified)
4. Execute the agent's brief verbatim, producing output to `reports/`
5. Show the user a summary + link to the full report

## How to create a new agent

When the user asks to add a new agent:
1. Copy `agents/template.md` to `agents/[new-name].md`
2. Fill in: Purpose, Trigger, Inputs, Brief, Output format
3. Update `README.md` agent table
4. Optionally add config in `config/[new-name].json`

## Conventions for agent briefs

- Use clear numbered steps
- Specify exact files to read
- Define output format precisely (template if HTML)
- Include severity scoring (🔴 critical / 🟠 high / 🟡 medium / 🟢 low)
- End with a clear verdict (PASS/FAIL or recommendations)

## Current agents — status

| Agent | Status | Last run |
|-------|--------|----------|
| DILS Quality Checker | ✅ Spec ready, awaiting first run | — |
| Security Auditor | ✅ Spec ready | — |
| Learning Tracker | ✅ Spec ready | — |
| Collaboration Manager | 📋 Planned | — |
| CRM Connector | 📋 Planned (waits on DILS LLM connector) | — |

## Related projects

- `C:/Automation/Github/my-projects/investment-tracker/` — first real test target
- `C:/Automation/Github/my-projects/dnd-tracker/` — secondary test target

## Roadmap

1. **This week** — DILS QC standards co-defined with CTO
2. **Next week** — First real DILS QC run on investment-tracker
3. **Following** — Security Auditor + Learning Tracker live
4. **Future** — Collaboration Manager + CRM Connector

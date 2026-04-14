# DILS Agents — Custom AI Agent Infrastructure

A collection of specialized Claude Code agents that run against any project in `C:/Automation/Github/my-projects/`.

## Philosophy

Agents are **disposable specialists**. Each one:
- Has a single, clear purpose
- Gets a complete briefing up front
- Produces a standardized report
- Doesn't depend on state from other agents
- Can be invoked manually or scheduled

## How to invoke an agent

From any project, in Claude Code, say:
```
Run the DILS Quality Checker on this project.
```

Claude reads the agent definition, runs it against the current project, produces a report in `/reports/`.

## Directory structure

```
dils-agents/
├── README.md                           # this file
├── agents/
│   ├── dils-quality-checker.md         # QA gate before CTO handoff
│   ├── security-auditor.md             # Security + RLS + secrets scan
│   ├── learning-tracker.md             # Tracks Noah's skill progression
│   └── template.md                     # Template for new agents
├── config/
│   ├── dils-standards.json             # DILS quality standards
│   └── skill-taxonomy.json             # Learning tracker skill tree
└── reports/
    └── (generated HTML reports)
```

## How to create a new agent

1. Copy `agents/template.md` → `agents/my-new-agent.md`
2. Fill in the sections (Purpose, Trigger, Checks, Output)
3. Test it by invoking it from a project
4. Iterate

## Current agents

| Agent | Status | Purpose |
|-------|--------|---------|
| **DILS Quality Checker** | ✅ Ready | Pre-handoff QA gate — security, perf, docs, conventions |
| **Security Auditor** | 🟡 In design | OWASP scan, RLS audit, dependency check |
| **Learning Tracker** | 🟡 In design | Tracks Noah's skill progression against architect goal |
| **Collaboration Manager** | 📋 Planned | Tracks topics to discuss per colleague |
| **CRM Connector** | 📋 Planned | Wires DILS CRM into Claude context for CRM-aware builds |

## Running philosophy — the orchestration model

```
Noah describes the goal
    ↓
Main Claude (orchestrator) plans architecture
    ↓
Claude invokes agents as needed:
    • Explore agents  → read-only analysis
    • Plan agents     → design approach
    • General agents  → write code
    • QA agents       → test + audit
    ↓
Main Claude verifies agent output
    ↓
Noah tests live
    ↓
DILS Quality Checker runs before CTO handoff
    ↓
Production
```

## Cross-project scope

Agents live OUTSIDE any single project. They can scan:
- `C:/Automation/Github/my-projects/investment-tracker/`
- `C:/Automation/Github/my-projects/dnd-tracker/`
- Any future project in `my-projects/`

Reports are written to `dils-agents/reports/` with project name + timestamp.

## Next steps

1. Implement DILS Quality Checker (see `agents/dils-quality-checker.md`)
2. Run it against Investment Tracker as first real test
3. Share with CTO for DILS standards input
4. Eventually wire up CRM connector

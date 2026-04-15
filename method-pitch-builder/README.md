# method-pitch-builder

**Status:** 📋 scoped — ready to start in a fresh Claude session.

## What this is
A dedicated pitch-builder for DILS **marketing / methodology pitches** (e.g., "here's how we'll fill your vacancies" — process sales, not property sales).

Distinct from `pitch-builder/` (which handles property pitches — Verlengingspitch, acquisition, teaser).

## Why separate
Tried to force both use cases through one skill → content-strategy and template branching bloat. Clean separation = single-responsibility skills, shared engine library.

| | pitch-builder (existing) | method-pitch-builder (this) |
|---|---|---|
| Audience | Tenant / investor | Building owner / client commissioning DILS |
| Subject | A building | A process DILS offers |
| Content source | AI-drafted from market data + public APIs | Pre-written in source .docx — rendered as-is |
| Visuals | Section labels + hero images | Funnels, flows, org charts, timelines, Gantt |
| Template | `property.pptx` (Empty Page - Dils Style) | `methodology.pptx` (to be built) |

## Architecture (proposed — validate before building)

```
dils-agents/
├── scripts/
│   ├── pptx-engine.py          ← SHARED (extract from current pitch-builder)
│   └── method-layouts.py        ← NEW, methodology-specific diagram helpers
├── pitch-templates/
│   └── methodology.pptx         ← NEW, DILS-branded, reusable layouts
├── config/
│   └── method-section-catalog.json  ← NEW
└── method-pitch-builder/        ← this folder
    ├── README.md                ← this file
    └── (agent spec goes here)
```

The shared `pptx-engine.py` refactor extracts template cloning, slide duplication, text-token replacement, image replacement, XML packing into a reusable module imported by BOTH skills.

## First real input waiting
**`dils-agents/inputs/tenant-targeting-2.0.md`** — 14-slide brief from The Base marketeer. This is the first live test case. Marketeer has already written the content per slide (objective, core message, bullets, suggested visual). The skill just needs to render it.

## Required template layouts (from marketeer's suggestions)
1. **Title slide** — full-bleed aerial + overlay text
2. **Problem / funnel** — reactive vs intent-led comparison
3. **5-step horizontal flow** — Detect → Map → Connect → Engage → Convert
4. **4-quadrant graphic** — accessibility / amenities / community / sustainability
5. **2-column comparison** — company profile vs business triggers with icons
6. **Data-flow graphic** — signal source → company → trigger → priority
7. **Org chart / stakeholder map** — 5-6 DMU roles with "what matters" tags
8. **Message comparison** — generic-salesy vs consultative (mock LinkedIn thread)
9. **Asset library grid** — 5 cards with title + icon + audience
10. **Timeline** — 6-week journey
11. **Conversion funnel** — universe → signals → outreach → conversations
12. **3-column: Input → Process → Output**
13. **KPI scorecard** — RAG table
14. **Gantt / 4-week launch plan** — colour-coded blocks with milestones

## Starting the work — prompt for next session

> "Continue method-pitch-builder. Read `dils-agents/method-pitch-builder/README.md` for context, then:
> 1. Refactor shared pptx logic from pitch-builder into `scripts/pptx-engine.py`
> 2. Build `pitch-templates/methodology.pptx` with 10 reusable layouts matching the marketeer's suggested visuals
> 3. Generate the Tenant Targeting 2.0 deck as first proof from `inputs/tenant-targeting-2.0.md`"

## Notes from today's session (April 15, 2026)

- pitch-builder for property is stable at v6 (pitch-basisweg-61a-2026-04-15.pptx in OneDrive)
- building-lookup.py works — gets BAG data + broker-aggregator facts from any Dutch address
- Decision to separate into two skills locked in by Noah — clean, not overloaded
- Fresh session recommended so context is focused on methodology-pitch concerns only

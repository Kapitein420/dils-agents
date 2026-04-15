# Pitch Brief Format

The pitch-builder agent accepts briefs in this format. Pasted into the Claude Code invocation or (Phase 1b) received via email.

## Minimum required

```
Client: <client or building name>
City: <city>
Sections:
- <section name>
- <section name>
- ...
```

## Full example (what colleagues would email)

```
Client: Zuidas Tower
City: Amsterdam
Deadline: 2026-04-20
Language: Dutch

Sections:
- Key Facts
- Marktanalyse
- Locatieanalyse
- Concurrentieanalyse
- Huurdersprofiel
- Marketingstrategie
- Commercieel Advies

Notes:
Client is focused on Grade A office, Q3 2026 delivery.
```

## Accepted section titles
Either Dutch or English — the title-map resolves variants. Full list in `config/pitch-title-map.json`.

| English | Dutch |
|---|---|
| Key Facts | Key Facts |
| Market Analysis | Marktanalyse |
| Location Analysis | Locatieanalyse |
| Competitor Analysis | Concurrentieanalyse |
| Sub-area | Subgebied |
| Tenant Profile | Huurdersprofiel |
| Target Audience | Doelgroep |
| Building Adjustments | Gebouw Aanpassingen |
| Marketing Strategy | Marketingstrategie |
| Commercial Advice | Commercieel Advies |

## What the agent produces
1. `.pptx` file saved to `OneDrive - Dils SpA/generated-pitches/pitch-<client-slug>-<YYYY-MM-DD>.pptx`
2. Metadata JSON saved to `dils-agents/reports/pitch-builder/pitch-<client-slug>-<YYYY-MM-DD>.json` — contains the brief, slide list, file path, timestamp
3. Each content slide populated with:
   - Correct title from the DILS template
   - Section label (02, 03, …) based on position
   - Body: `[Wordt door Noah ingevuld — to be filled]` placeholder

## Unknown section handling
If a brief requests a section not in the catalog, the agent clones slide 12 (generic content layout) and uses the custom title. This won't happen often since colleagues tend to stick to the standard sections.

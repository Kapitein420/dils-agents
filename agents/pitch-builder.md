---
name: Pitch Builder
layer: Business — Client Management
purpose: Template-driven pitch decks — take the email brief with slide structure, produce branded .pptx matching that exact structure every time
trigger: Manual (Noah forwards email/brief)
output: PPTX
---

# Pitch Builder

## How this actually works in Noah's role

Clients/colleagues send email pitch requests that **already contain the slide structure** — specific slide titles, order, sometimes hints at content per slide. What Noah needs is:

- Same structure preserved every time (never reorder, never skip)
- Each slide populated with content that matches the request
- Branded DILS look applied automatically
- Deck ready to review + refine, not from scratch

The agent is **template-executor first, creative-filler second**. AI-assisted content generation is Phase 2 — Phase 1 is reliable structure replication.

## Phases

### Phase 1 (FIRST BUILD) — Structure Replicator
Input:
- Raw email / brief text (Noah pastes)
- DILS brand assets (logo, palette, typography)

Agent:
1. Parse the brief to extract slide titles in order
2. Validate structure is complete (ask Noah if any slide feels ambiguous)
3. Generate a .pptx with:
   - Cover slide (client name, pitch topic, date, DILS logo)
   - One slide per detected title, DILS-branded layout
   - Each slide has: title, placeholder body text indicating what goes here ("[Market overview — to be filled]"), suggested layout (bullets / table / chart / image)
   - Closing slide with DILS team contacts placeholder
4. Output to `dils-agents/reports/pitch-[client-slug]-[date].pptx`
5. Report to dashboard: slides count, placeholders remaining

### Phase 2 (LATER) — AI Content Filler
Once Phase 1 is solid:
- For each slide placeholder, agent proposes filled content based on:
  - DILS sector intelligence (once CRM connector live)
  - Client context from email
  - Market intelligence scanner outputs
- Noah reviews + approves per slide
- Agent writes final version

### Phase 3 (FUTURE) — Email Watcher
- Agent monitors inbox for pitch requests
- Auto-triggers Phase 1 on detection
- Noah opens dashboard → finds deck already drafted

## Config needed
`config/pitch-builder.json`:
```json
{
  "brandAssets": {
    "logoPath": "assets/dils-logo.png",
    "palette": { "primary": "#c9a86a", "dark": "#2a1f14", "cream": "#f5ecd7" },
    "fonts": { "heading": "Serif", "body": "Sans" }
  },
  "templateSlides": {
    "coverLayout": "title + subtitle + logo bottom-right",
    "contentLayout": "title top + body left + optional image right",
    "closingLayout": "contacts 3-col"
  },
  "defaultFooter": "DILS · [client] · [date]"
}
```

## Inputs for each run
1. Email/brief text (pasted)
2. Client name
3. Pitch topic
4. Deadline (optional, drives priority)

## Output
- `.pptx` file at `dils-agents/reports/pitch-[client-slug]-[date].pptx`
- Status entry for dashboard (see agent-hq contract)
- Summary: `N slides generated, M placeholders`

## Uses
- Anthropic `pptx` skill for file generation
- DILS brand config for styling

## Notes
- NEVER improvise structure. If the email says 7 slides, output 7.
- Flag structural ambiguity to Noah, don't guess.
- Phase 1 is the workhorse — get it reliable before adding AI filling.

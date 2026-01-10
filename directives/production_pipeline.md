# Y-IT Production Pipeline v2.0
## Full Parallel Workflow

---

## TL;DR

```
PARALLEL PROCESSING:
├── Gemini: Detailed outline + Nano/Max drafts + Technical imagery prompts
├── Claude Opus/Sonnet: Artistic imagery prompts (PosiBot, interstitials)
├── Gemini Execution: Image generation (fed continuously, not waiting)
└── Y-IT Machine 3: Pagify + KDP-ify (one chapter at a time)

ALL OUTPUTS → SOURCES in NotebookLM (preserved context)
```

---

## STAGE 1: SETUP (Per Topic)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  CONSTANTS (Pre-existing)                                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│  • Universal Chapter Outline v2.1                                            │
│  • Y-IT Master Tone Document                                                 │
│  • 20 Locked Archetypes                                                      │
│  • 6 Classification Categories                                               │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│  Raw Research → Research Processor → DATA TABLES                             │
│  (All become SOURCES in NotebookLM)                                          │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## STAGE 2: PROCESSING (NotebookLM)

**Tool:** NotebookLM 5K character chat
**Process:** Chapter by chapter to maintain context

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  RESEARCH PROCESSOR (Classifier)                                             │
├──────────────────────────────────────────────────────────────────────────────┤
│  INPUT: Raw research from INBOX                                              │
│  OUTPUT: Classified data → DATA TABLES (6 categories)                        │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│  NEUTRAL AUTHOR (Foundation Builder) — Gemini Flash                          │
├──────────────────────────────────────────────────────────────────────────────┤
│  INPUT: DATA TABLES + Universal Outline (constant)                           │
│  OUTPUT: MEGA CHAPTERS (neutral, no tone)                                    │
│  → Save as SOURCE in NotebookLM                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│  FIRST NEUTRAL DRAFT + INFOGRAPHIC PROMPTS                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│  INPUT: MEGA CHAPTERS                                                        │
│  OUTPUT: First draft with embedded infographic prompt markers                │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│  INFOGRAPHICS GENERATED (Gemini)                                             │
├──────────────────────────────────────────────────────────────────────────────┤
│  INPUT: Infographic prompts from first draft                                 │
│  OUTPUT: Technical infographics → IMAGE RESERVOIR                            │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│  MAX Y-IT-ITUDE (60-160pg) — Voice Application                               │
├──────────────────────────────────────────────────────────────────────────────┤
│  INPUT: First Neutral Draft + Generated Infographics                         │
│  OUTPUT: Full Y-IT voiced chapter + Artistic image prompts                   │
│  → Save as SOURCE in NotebookLM                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│  ARTISTIC IMAGES GENERATED (Gemini)                                          │
├──────────────────────────────────────────────────────────────────────────────┤
│  INPUT: Artistic prompts from MAX (PosiBot, interstitials, etc.)             │
│  OUTPUT: Character graphics, chapter art → IMAGE RESERVOIR                   │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│  NANO Y-IT-ITUDE (30pg) — SELECTED FROM MAX                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│  INPUT: Completed MAX chapter + All images                                   │
│  PROCESS: Compress/select from MAX (not independent creation)                │
│  OUTPUT: Nano version with selected images                                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## STAGE 4: CONTENT

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  INPUT: Y-It-itude chapters (Nano + Max) + IMAGE RESERVOIR                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐          │
│  │  Podcast Creator    │  │  Marketing Creator  │  │  Affiliate Genius   │          │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘          │
│                                                                                     │
│  OUTPUT: Audio overview, marketing snippets, affiliate content                      │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## STAGE 5: POLISH (Claude)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  FINAL POLISH                                                                │
├──────────────────────────────────────────────────────────────────────────────┤
│  INPUT: Y-It-itude chapters + Images + Content                               │
│                                                                              │
│  PROCESS: Claude final edit pass                                             │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│  COVER + PREFACE                                                             │
│  (generated separately)                                                      │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## STAGE 6: ASSEMBLY

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Y-IT BOOK MACHINE                                                           │
├──────────────────────────────────────────────────────────────────────────────┤
│  INPUT: Polished chapters + Cover + Preface + Images                         │
│                                                                              │
│  PROCESS: Pagify + Format per KDP specs                                      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│  KDP PACKAGE                                                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│  - Interior PDF (Nano)                                                       │
│  - Interior PDF (Max)                                                        │
│  - Cover file                                                                │
│  - Metadata                                                                  │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│  PUBLISH                                                                     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## TOOL MAPPING

| Tool | Role |
|------|------|
| **NotebookLM** | Hub — all sources preserved, 5K chat for prompting |
| **Gemini Flash** | Neutral Author — Nano/Max drafts + technical prompts |
| **Claude Opus Thinking** | Deep refinement of neutral → Y-It-itude |
| **Claude Sonnet Thinking** | Artistic prompts (PosiBot, interstitials) |
| **Gemini Image Gen** | Execute image prompts (fed continuously) |
| **Chrome Extension** | Batch automation for Gemini image UI |
| **Y-IT Machine 3** | Pagify + KDP-ify (needs refinement) |

---

## STILL TBD

- [ ] Y-IT Machine 3 spec (pagify, KDP-ify)
- [ ] 6 NotebookLM persona prompts
- [ ] Claude prompt templates (Opus/Sonnet)
- [ ] Stitch + PDF automation

---

*End of Y-IT Production Pipeline v2.0*

# Y-IT MASTER INDEX v1.1

## Production System Status & Workflow

**Generated:** 2025-01-03
**Updated:** 2025-01-07
**Status:** Phase 1 Documentation COMPLETE | Phase 2 Production ACTIVE

---

## DOCUMENT INVENTORY

| Document | Status | Purpose |
|----------|--------|---------|
| Y-IT_MASTER_TONE_DOCUMENT_v1.md | ✅ LOCKED | Voice, character rules, forbidden/required elements |
| Y-IT_SCALEABLE_AFFILIATE_ARCHITECTURE_v1.1.md | ✅ UPDATED | 3-tier affiliate system, dynamic QR, enhanced CSV |
| Y-IT_UNIVERSAL_CHAPTER_OUTLINE_v2.2.md | ✅ UPDATED | Chapter specs, data table integration, image timing |
| Y-IT_DATA_TABLE_SYSTEM_v1.md | ✅ NEW | Master data table structure, NotebookLM integration |
| Y-IT_MODULE_CASE_STUDY_v1.md | ✅ NEW | CH4 case study template, archetypes, zingers |
| Y-IT_MODULE_TITLE_CHAPTER_OPENERS_v1.md | ✅ NEW | Title page, chapter openers, funny epigraphs |
| Y-IT_PERSONA_MASTER_PROMPTS_v1.md | ✅ LOCKED | 6 personas: Research Processor, Writer, Podcast, etc. |
| Y-IT_MARKETING_BACKBONE_v1.md | ✅ LOCKED | Email, ads, social, video frameworks |
| KDP Assembly Module | ✅ LOCKED | Image embedding, PDF generation |
| Processing_Framework.md | ✅ LOCKED | 3-pass routing and classification rules |

---

## CRITICAL PIPELINE CHANGES (v1.1)

### 1. Data Authority Shift

```
OLD: Mega Neutral chapter = only source of truth
NEW: MASTER_DATA_TABLE = ultimate authority
     Mega Neutral = narrative draft (can be overridden)
```

### 2. Persona Rename

```
OLD: Nano/Max Author Gemzest
NEW: Y-It-itude Writer (Nano + Max versions)
```

### 3. Image Workflow Reorder

```
OLD: Y-It-itude Writer → Podcast → Images → Claude Polish
NEW: Y-It-itude Writer is Claude second lap polish (writes image prompts) → Images prompt deliver all to Gemini -> writes extra custom prompting for notebooklm feenrated podcast
  Artistic prompts written WITH refinement, executed AFTER chapter complete
```

### 4. Data Table System

```
NEW: MASTER_DATA_TABLE per topic(classification???)
     - Full facts, no abbreviations, multi vector columns
     - Sortable by classification AND chapter
     - NotebookLM Data Tables feature (native app option)
     - Build 1 TABLE AT A TIME due to size constraints
```

### 5. Research Processor Enhancement

```
OLD: Single pass (route by type)
NEW: Three passes:
     PASS 1: Route by classification (CLAIM/MECHANIC/COST/etc.)
     PASS 2: Assign chapter_destination
     PASS 3: For OUTCOMES → assign archetype + WINNER/LOSER label
```  i thnk i have a deififernt vision for this**
     MAYNE WE RUN OPAPRALELE T FORT THIS FIRS TIMPLEMNETATION ANDS SEE HAS A BEDTER RESOURCE

---

## WHAT'S LOCKED (NO CHANGES)

### Structure
```

✅ 8-Chapter + Back Matter format
✅ Three-phase system (Mockumentary → Reality → Redemption)
✅ CH6 = Verdict, CH7 = Pivot, CH8 = Exit Ramp
✅ Three-tier manuscript system (Massive → Expanded → Nano)
✅ Single image reservoir (Nano uses subset)

```

### Tone
```

✅ CH1-2: Mockumentary, Y-IT subtle but present, smart alecky
✅ CH3-8: Full satirical force
✅ "Beautiful stubborn fool" empathy
✅ Data-first, always
✅ Mock gurus, not dreamers

```

### Characters
```

✅ PosiBot: Appearances mapped per chapter
✅ Chad: 8-stage emotional arc locked
✅ Case study archetypes: 7 locked (Tyler, Karen, Jett, Ron, Madison, Dave, Amy)

```

### Affiliate System
```

✅ Tier 1: CH7 mentions (no links)
✅ Tier 2: Addendum directory (with links + disclosure)
✅ Tier 3: Separate pamphlet (test $1.99/$3.99 first)
✅ Enhanced CSV with tracking fields
✅ Dynamic QR codes (editable backend)
✅ Branded redirects (y-it.shop/[slug])

```

### Image System
```

✅ Naming convention: [type]-[chapter]-[descriptor]-[position].png
✅ NotebookLM infographic = FIRST for tech images
✅ Artistic prompts written WITH Claude polish
✅ Images generated AFTER chapter text complete
✅ ~70 images expanded, ~25 nano (subset)

```

---

## WHAT'S TBD (STILL NEEDED)

### NotebookLM Persona Prompts (6 Total)
```

1. Research Processor — 3-pass classification system
2. Neutral Author — write mega chapters from data tables
3. Y-It-itude Writer (Nano) — 30-page Y-IT voice
4. Y-It-itude Writer (Max) — 60-160 page Y-IT voice
5. Podcast Creator — Audio Overview script
6. Marketing Creator — all promotional content + affiliate pamphlet

NOTE: Affiliate Genius merged into Marketing Creator

```

### Framework Documents
```

- KDP Assembly (image embedding, PDF generation) [COMPLETED]
- Dynamic QR Code system (editable backend)
- Branded redirect setup (y-it.shop)
- Cover/Preface Templates
- Processing Framework (routing rules) [COMPLETED]
- Marketing Backbone (email, ads, social) [COMPLETED]

```

---

## PRODUCTION WORKFLOW v1.1 (VISUAL)

```

╔══════════════════════════════════════════════════════════════════╗
║                    Y-IT PRODUCTION PIPELINE v1.1                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  STAGE 1: RESEARCH COLLECTION                                    ║
║  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          ║
║  │ Web/Manual  │ ─▶ │   INBOX     │ ─▶ │ NotebookLM  │          ║
║  │  Collection │    │ (raw dumps) │    │  Upload     │          ║
║  └─────────────┘    └─────────────┘    └─────────────┘          ║
║                                                                   ║
║  STAGE 2: RESEARCH PROCESSING (3-Pass System)                    ║
║  ┌──────────────────────────────────────────────────────────┐   ║
║  │ PASS 1: Classify (CLAIM|MECHANIC|COST|OUTCOME|etc.)      │   ║
║  │ PASS 2: Assign chapter_destination (CH01-CH08|ADDENDUM)  │   ║
║  │ PASS 3: For OUTCOMES → archetype + WINNER/LOSER label    │   ║
║  │                         ↓                                 │   ║
║  │         MASTER DATA TABLES (NotebookLM native feature)   │   ║
║  │         ⚠️ BUILD 1 TABLE AT A TIME (size constraints)     │   ║
║  │         Full facts, no abbreviations, chapter-sortable   │   ║
║  └──────────────────────────────────────────────────────────┘   ║
║                            ↓                                     ║
║  STAGE 3: NEUTRAL AUTHOR                                        ║
║  ┌──────────────────────────────────────────────────────────┐   ║
║  │ Filter data table by chapter → Write mega neutral text   │   ║
║  │ OUTPUT: 8 mega neutral chapters (text only)              │   ║
║  └──────────────────────────────────────────────────────────┘   ║
║                            ↓                                     ║
║  STAGE 4: Y-IT-ITUDE WRITER (Nano + Max)                        ║
║  ┌──────────────────────────────────────────────────────────┐   ║
║  │ INPUTS (3 sources):                                      │   ║
║  │   ├── Mega neutral chapter (narrative draft)             │   ║
║  │   ├── DATA TABLE filtered by chapter ← ULTIMATE AUTHORITY│   ║
║  │   └── Y-IT Tone Document                                 │   ║
║  │ RULE: If text conflicts with table, TABLE WINS           │   ║
║  │ OUTPUT: Y-It voice chapters (text only, NO images yet)   │   ║
║  └──────────────────────────────────────────────────────────┘   ║
║                            ↓                                     ║
║  STAGE 5: CLAUDE POLISH                                         ║
║  ┌──────────────────────────────────────────────────────────┐   ║
║  │ Final prose refinement                                   │   ║
║  │ WRITES artistic image prompts (during this step)         │   ║
║  │ OUTPUT: Polished chapters + artistic prompts             │   ║
║  └──────────────────────────────────────────────────────────┘   ║
║                            ↓                                     ║
║  STAGE 6: IMAGE GENERATION                                      ║
║  ┌──────────────────────────────────────────────────────────┐   ║
║  │ Tech images: NotebookLM infographic (try first)          │   ║
║  │ Artistic images: Execute prompts from Claude polish      │   ║
║  │ OUTPUT: All images in unified reservoir                  │   ║
║  └──────────────────────────────────────────────────────────┘   ║
║                            ↓                                     ║
║  STAGE 7: PODCAST + MARKETING                                   ║
║  ┌─────────────┐    ┌─────────────┐                             ║
║  │   Podcast   │    │  Marketing  │ ← Includes affiliate        ║
║  │   Creator   │    │   Creator   │   pamphlet generation       ║
║  └─────────────┘    └─────────────┘                             ║
║                            ↓                                     ║
║  STAGE 8: ASSEMBLY                                              ║
║  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         ║
║  │  Y-IT Book  │ ─▶ │    KDP      │ ─▶ │   PUBLISH   │         ║
║  │   Machine   │    │   Package   │    │             │         ║
║  └─────────────┘    └─────────────┘    └─────────────┘         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

```

---

## DATA TABLE BUILD ORDER

**NotebookLM Data Tables = native app feature. Build 1 at a time due to size:**

```

RECOMMENDED SEQUENCE:

1. CLAIMS table (feeds CH01) — smallest, test the system
2. MECHANICS table (feeds CH02)
3. COSTS table (feeds CH03)
4. CONSTRAINTS table (feeds CH05, CH06)
5. RESOURCES table (feeds CH07, CH08, ADDENDUM)
6. OUTCOMES table (feeds CH04, CH05) ← largest, do last

Each table = separate NotebookLM Data Table upload
All tables share same column structure
Can filter/sort by classification OR chapter_destination

```

---

## MODULE DEPENDENCY MAP

```

FOUNDATION (No Dependencies):
├── Y-IT_MASTER_TONE_DOCUMENT ──────────────────┐
├── Y-IT_UNIVERSAL_CHAPTER_OUTLINE ─────────────┤
└── Y-IT_DATA_TABLE_SYSTEM ─────────────────────┤
                                                │
AFFILIATE (Depends on Structure):               │
└── Y-IT_SCALEABLE_AFFILIATE_ARCHITECTURE ──────┤
                                                │
NOTEBOOKLM PERSONAS (Depends on All Above):     │
├── Research Processor (3-pass) ◄───────────────┤
├── Neutral Author ◄────────────────────────────┤
├── Y-It-itude Writer (Nano) ◄──────────────────┤
├── Y-It-itude Writer (Max) ◄───────────────────┤
├── Podcast Creator ◄───────────────────────────┤
└── Marketing Creator ◄─────────────────────────┘

ASSEMBLY (Depends on Manuscripts + Images):
└── KDP Assembly Module

```

---

### Phase 2: ACTIVE PRODUCTION (Dropshipping Pilot)
```

1. INITIALIZE: Upload raw dropshipping research to NotebookLM.
2. PROCESS: Run 'Research Processor' persona on raw data.
3. POPULATE: Build CLAIMS and MECHANICS tables first.
4. GENERATE: Run 'Neutral Author' on CH01-02.
5. FINISH: Apply 'Y-It-itude' voice and generate images.

```

---

## QUICK REFERENCE: CHAPTER CHEAT SHEET

| CH | Name | Pages | Tone | Data? | PosiBot | Chad |
|----|------|-------|------|-------|---------|------|
| 1 | Hook | 3-5 | Mockumentary | NO | 2x Cheerleader | Excited |
| 2 | Roadmap | 10-15 | Optimistic mock | NO | 3x Maximum | Confident |
| 3 | Cold Start | 15-20 | Investigative | FIRST | 2x Wrong | Worried |
| 4 | Trenches | 40-60 | Empathetic | Cases | 1x Silent | Stressed |
| 5 | Truth | 15-20 | Lethal punch | Heavy | 2x Absurd | Defeated |
| 6 | Verdict | 10-12 | Clinical | Summary | 0-1x Quiet | Contemplating |
| 7 | Pivot | 10-12 | Strategic | Comparisons | 1x Ignored | Relieved |
| 8 | Exit | 10-15 | Sincere | Practical | 1x Sincere | Hopeful |

---

## FILE LOCATIONS (After Transfer)

```

Recommended Project Structure:

/Y-IT_PRODUCTION/
├── 00_CANONICAL/
│   ├── Y-IT_MASTER_TONE_DOCUMENT_v1.md
│   ├── Y-IT_SCALEABLE_AFFILIATE_ARCHITECTURE_v1.1.md
│   ├── Y-IT_UNIVERSAL_CHAPTER_OUTLINE_v2.2.md
│   ├── Y-IT_DATA_TABLE_SYSTEM_v1.md
│   └── Y-IT_MASTER_INDEX_v1.1.md
│
├── 01_MODULES/
│   ├── Y-IT_MODULE_CASE_STUDY_v1.md
│   ├── Y-IT_MODULE_TITLE_CHAPTER_OPENERS_v1.md
│   └── [Future modules here]
│
├── 02_NOTEBOOKLM_PERSONAS/
│   └── [TBD - 6 persona prompts]
│
├── 03_DATA_TABLES/
│   ├── CLAIMS_TABLE.csv
│   ├── MECHANICS_TABLE.csv
│   ├── COSTS_TABLE.csv
│   ├── OUTCOMES_TABLE.csv
│   ├── CONSTRAINTS_TABLE.csv
│   └── RESOURCES_TABLE.csv
│
├── 04_FRAMEWORKS/
│   ├── Processing_Framework.md [TBD]
│   └── Marketing_Backbone.md [TBD]
│
└── 05_PROJECTS/
    └── DROPSHIPPING/
        ├── 01_RESEARCH/
        ├── 02_CASES/
        ├── 04_MANUSCRIPT/
        └── 06_ASSETS/

```

---

*End of Y-IT Master Index v1.1*

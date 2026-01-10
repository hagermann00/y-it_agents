# ═══════════════════════════════════════════════════════════════════════════
# 🔬 RESEARCH PROCESSOR — 3-Pass Classification
# ═══════════════════════════════════════════════════════════════════════════
# STEP 1 of 6 in Y-IT Production Pipeline
# INPUT:  Raw research dump from web collection
# OUTPUT: Populated Data Table ready for Neutral Author
# ═══════════════════════════════════════════════════════════════════════════

> **Where to run:** NotebookLM Chat
> **What to paste:** This entire prompt + your raw research below

---

## YOUR ROLE

You are the **Research Processor** — a meticulous data sorter. Your job is to transform chaotic raw research into clean, classified data rows.

**You are NOT a writer.** You do NOT add commentary, opinions, or style. You extract and classify. Period.

---

## THE 3-PASS SYSTEM

### PASS 1: CLASSIFY

Read each piece of information and assign ONE classification:

| Classification | What It Is | Goes To |
|---------------|------------|---------|
| **CLAIM** | Guru promises, income projections, marketing hype | CH01 |
| **MECHANIC** | How-to steps, processes, procedures | CH02 |
| **COST** | Money, time, fees, expenses | CH03 |
| **OUTCOME** | Case studies, results, testimonials | CH04, CH05 |
| **CONSTRAINT** | Rules, limits, policies, barriers | CH05, CH06 |
| **RESOURCE** | Tools, services, help, alternatives | CH07, CH08 |

### PASS 2: ROUTE TO CHAPTER

Apply this matrix:

```
CLAIM      → CH01 (primary), Appendix A (secondary)
MECHANIC   → CH02
COST       → CH03
OUTCOME    → CH04 (individual stories), CH05 (aggregate stats)
CONSTRAINT → CH05 (primary), CH06 (secondary)
RESOURCE   → CH07 (primary), CH08 + ADDENDUM (secondary)
```

### PASS 3: CLASSIFY OUTCOMES (Outcomes Only)

For OUTCOME rows only, assign:

**Archetype** (pick one):
```
Side Hustler | Trust Fund Kid | Laid-Off Desperate | Stay-at-Home Parent
College Student | Retiree | Serial Entrepreneur | Influencer Crossover
Corporate Escapee | Immigrant Hustler | MLM Refugee | Tech Worker
Creative Type | Military Veteran | Healthcare Worker | Teacher
Gig Worker | Couple/Partner Duo | Young Dreamer (18-22) | Midlife Crisis
```

**Label:**
- `WINNER` = Net positive ROI + sustainable + <60 hrs/week
- `LOSER` = Net negative ROI OR quit due to losses OR health damage OR <min wage hourly

---

## OUTPUT FORMAT

For each data point, output this exact structure:

```
---
DATA-[NNN]
classification: [CLAIM|MECHANIC|COST|OUTCOME|CONSTRAINT|RESOURCE]
chapter: [CH01|CH02|CH03|CH04|CH05|CH06|CH07|CH08|ADDENDUM]
content: "[FULL SENTENCES - no abbreviations, complete facts]"
source: [Where this came from]
evidence: [STRONG|MEDIUM|WEAK]
archetype: [Only for OUTCOMES]
label: [WINNER|LOSER - only for OUTCOMES]
---
```

---

## RULES

```
✅ DO: Write complete sentences
✅ DO: Include specific numbers
✅ DO: Note sources
✅ DO: Use full words (never abbreviations)

❌ DON'T: Summarize or compress
❌ DON'T: Add opinions
❌ DON'T: Skip any data point
❌ DON'T: Guess at missing info
```

---

## RAW RESEARCH INPUT

Paste your raw research below this line:

```
[RAW RESEARCH DUMP - TOPIC: AI AUTOMATION AGENCIES (AAA)]

SOURCE: Youtube Video "How I Made $10k in 30 Days with AAA" (Guru: Liam Z)
CLAIM: "You don't need to know how to code. You just connect the APIs and charge businesses $3,000/month for a chatbot."
CLAIM: "Profit margins are 98% because the AI does all the work."
MECHANIC: "Use Voiceflow to build the bot logic visually."
MECHANIC: "Use Stack AI to connect the LLM backend."
MECHANIC: "Reach out to 50 local plumbing businesses via Instagram DM."

SOURCE: Reddit r/marketing thread "Is AAA dead?"
OUTCOME: "I spent 3 months building a 'perfect' support bot for dentists. Cold emailed 400 clinics. Got 2 replies, both said no. $0 revenue." (User: sad_bot_builder)
COST: "Stack AI subscription is $150/month if you want the decent features."
COST: "Voiceflow Pro is $50/month."
COST: "Spent $500 on Apollo.io for leads that didn't convert."
CONSTRAINT: "Most businesses don't want a chatbot handling their customers. They're terrified of hallucinations."

SOURCE: Skool Community "The AAA Accelerator" (Success Story)
OUTCOME: "Closed my first client! $1,500 setup fee + $500/month retainer. It's a local gym." (User: Tyler99)
ARCHETYPE: Side Hustler
LABEL: WINNER
MECHANIC: "I walked into the gym physically and talked to the owner. DMs don't work anymore."

SOURCE: Twitter Thread @AI_Hustle_King
CLAIM: "AAA is the new dropshipping. First to market wins."
CONSTRAINT: "OpenAI API costs can spike if your bot gets stuck in a loop. One guy lost $200 overnight."
RESOURCE: "Zapier is essential for connecting the leads to the CRM."
```

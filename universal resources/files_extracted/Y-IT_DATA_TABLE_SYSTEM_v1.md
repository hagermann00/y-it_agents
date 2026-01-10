# Y-IT DATA TABLE SYSTEM v1.0
## Master Data Architecture for NotebookLM

**Created:** 2025-01-07
**Status:** LOCKED

---

## TL;DR

```
ONE MASTER DATA TABLE PER TOPIC
├── Full facts, no abbreviations
├── Sortable by classification AND chapter
├── NotebookLM Data Tables = native app feature
├── ⚠️ BUILD 1 TABLE AT A TIME (size constraints)
└── DATA TABLE = ULTIMATE AUTHORITY (overrides mega neutral text)
```

---

## WHY DATA TABLES?

### Problem Solved
```
OLD SYSTEM:
Raw Research → Mega Neutral (only source) → Nano/Max Writers
                     ↑
            SINGLE POINT OF FAILURE
            If Neutral Author misinterprets data,
            error cascades through 50 books

NEW SYSTEM:
Raw Research → DATA TABLES (verified facts) → Mega Neutral (draft)
                     ↓                              ↓
              ULTIMATE AUTHORITY          NARRATIVE DRAFT
              Y-It-itude Writers check BOTH sources
              If conflict → TABLE WINS
```

### Key Benefits
- Facts verified ONCE, used everywhere
- No data dilution across personas
- Explicit archetype/label classification (auditable)
- Chapter routing built-in
- Scalable across 50+ topics

---

## NOTEBOOKLM DATA TABLES

### What It Is
NotebookLM now has a native Data Tables feature that allows structured data upload and querying. This replaces scattered CSVs.

### Size Constraint
```
⚠️ CRITICAL: Build 1 table at a time
Large tables may hit context limits
Split by classification if needed
Merge later or keep separate by type
```

### Build Order (Recommended)
```
1. CLAIMS table (feeds CH01) — smallest, test system
2. MECHANICS table (feeds CH02)
3. COSTS table (feeds CH03)
4. CONSTRAINTS table (feeds CH05, CH06)
5. RESOURCES table (feeds CH07, CH08, ADDENDUM)
6. OUTCOMES table (feeds CH04, CH05) — largest, do last
```

---

## MASTER TABLE STRUCTURE

### Column Definitions

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| data_id | STRING | YES | Unique identifier (DATA-001, DATA-002, etc.) |
| classification | ENUM | YES | CLAIM \| MECHANIC \| COST \| OUTCOME \| CONSTRAINT \| RESOURCE |
| chapter_destination | ENUM | YES | CH01 \| CH02 \| CH03 \| CH04 \| CH05 \| CH06 \| CH07 \| CH08 \| ADDENDUM |
| full_content | TEXT | YES | Complete fact in full sentences (NO abbreviations) |
| source | STRING | YES | Where the information came from |
| source_url | STRING | NO | Link if available |
| evidence_grade | ENUM | YES | STRONG \| MEDIUM \| WEAK \| UNCLEAR |
| archetype | STRING | OUTCOMES only | One of 20 archetypes (Side Hustler, Trust Fund Kid, etc.) |
| label | ENUM | OUTCOMES only | WINNER \| LOSER |
| amount_min | NUMBER | COSTS only | Minimum dollar amount |
| amount_max | NUMBER | COSTS only | Maximum dollar amount |
| frequency | ENUM | COSTS only | one-time \| monthly \| annual |
| step_number | NUMBER | MECHANICS only | Which step in CH02 (1-10) |
| collected_date | DATE | YES | When captured |
| notes | TEXT | NO | Internal notes |

---

## CLASSIFICATION DEFINITIONS

### CLAIM
```
Definition: Guru promises, marketing claims, income projections
Chapter: CH01 (Hook) + Appendix A
Example: "Course creator promises students can earn $10,000 per month 
         within 90 days of starting their dropshipping store with no 
         prior experience required"
```

### MECHANIC
```
Definition: How-to steps, processes, procedures
Chapter: CH02 (Roadmap)
Example: "Step 3: Create Facebook Business Manager account by navigating 
         to business.facebook.com and clicking Create Account. Requires 
         valid email and phone number for verification. Approval typically 
         takes 24-48 hours but can take up to 7 days for new accounts."
```

### COST
```
Definition: Money, time, fees, expenses
Chapter: CH03 (Cold Start)
Example: "Shopify Basic Plan monthly subscription fee required to operate 
         an online store with up to 2 staff accounts and basic reporting 
         features. Cost: $29/month."
```

### OUTCOME
```
Definition: Case studies, results, testimonials (verified)
Chapter: CH04 (Trenches) + CH05 (aggregate)
Example: "Karen, 34-year-old marketing coordinator employed full-time, 
         invested $1,000 starting capital with 10-15 hours per week 
         available. Purchased $497 course, spent $2,900 on Facebook ads 
         over 4 months. Total revenue $431 from 11 sales with 4 returns. 
         Net loss of $3,223. Quit after month 4 due to stress and 
         unsustainable losses. Effective hourly rate: negative $49.58."
Archetype: Side Hustler
Label: LOSER
```

### CONSTRAINT
```
Definition: Rules, limits, policies, barriers
Chapter: CH05 (Truth) + CH06 (Verdict)
Example: "PayPal holds funds for 180 days on new merchant accounts with 
         high chargeback risk categories including dropshipping. Funds 
         remain inaccessible during hold period regardless of order 
         fulfillment status."
```

### RESOURCE
```
Definition: Tools, services, help, alternatives
Chapter: CH07 (Pivot) + CH08 (Exit) + ADDENDUM
Example: "SCORE.org provides free one-on-one mentoring from experienced 
         business professionals for small business owners and entrepreneurs. 
         No cost, nonprofit organization supported by SBA."
```

---

## CHAPTER ROUTING MATRIX

| Classification | Primary Chapter | Secondary Chapter |
|---------------|-----------------|-------------------|
| CLAIM | CH01 | Appendix A |
| MECHANIC | CH02 | — |
| COST | CH03 | — |
| OUTCOME | CH04 | CH05 (aggregate stats) |
| CONSTRAINT | CH05 | CH06 |
| RESOURCE | CH07 | CH08, ADDENDUM |

---

## EVIDENCE GRADING

### STRONG
```
Criteria:
- Receipts, screenshots, transaction logs
- Official documentation
- Multiple corroborating sources
- Verifiable by third party

Use for: All numerical claims, case study financials
```

### MEDIUM
```
Criteria:
- Coherent narrative but no receipts
- Single credible source
- Industry standard knowledge
- Expert opinion

Use for: Process descriptions, general guidance
```

### WEAK
```
Criteria:
- Anecdotal only
- Vague details
- Unverified claims
- Potential bias

Use for: Background context (flagged)
```

### UNCLEAR
```
Criteria:
- Contradictory sources
- Incomplete data
- Disputed facts

Use for: Noted but not relied upon
```

---

## ARCHETYPE ASSIGNMENT (OUTCOMES ONLY)

### The 20 Locked Archetypes

| # | Archetype | Description | Typical Pattern |
|---|-----------|-------------|-----------------|
| 1 | Side Hustler | Full-time job + nights/weekends | Time-poor, capital-limited |
| 2 | Trust Fund Kid | Starting capital advantage | Can afford to lose, often wins |
| 3 | Laid-Off Desperate | Needs income NOW | High pressure, rushed decisions |
| 4 | Stay-at-Home Parent | Kids + limited hours | Interrupted focus, slow progress |
| 5 | College Student | No capital, lots of time | Learns fast, can't scale |
| 6 | Retiree | Capital + time, no tech skills | Vulnerable to scams |
| 7 | Serial Entrepreneur | Prior business experience | Transfers skills, higher success |
| 8 | Influencer Crossover | Existing audience | Distribution advantage |
| 9 | Corporate Escapee | Savings + burnout | Motivated but impatient |
| 10 | Immigrant Hustler | Limited options, high drive | Works harder, systemic barriers |
| 11 | MLM Refugee | Already spent on "opportunities" | Skeptical but hopeful |
| 12 | Tech Worker | High income, automation skills | Can build tools, time-poor |
| 13 | Creative Type | Design/content skills | Good branding, weak on ads |
| 14 | Military Veteran | Discipline + benefits | Structured approach |
| 15 | Healthcare Worker | Stable income, burnout | Looking for escape |
| 16 | Teacher | Summers off, low pay | Time-rich in spurts |
| 17 | Gig Worker | Already self-employed | Understands hustle, capital-poor |
| 18 | Couple/Partner Duo | Combined resources | More capital, coordination issues |
| 19 | Young Dreamer (18-22) | No experience, all optimism | Learns hard lessons |
| 20 | Midlife Crisis | Age 40-55, "now or never" | Emotional decision-making |

### Label Assignment Rules
```
WINNER Criteria (must meet ALL):
- Net positive ROI
- Sustainable (still operating OR profitable exit)
- Reasonable time investment (< 60 hrs/week)

LOSER Criteria (meet ANY):
- Net negative ROI
- Quit due to losses
- Health/relationship damage
- Effective hourly rate below minimum wage

EDGE CASES:
- "Won the battle, lost the war" = LOSER (burned out)
- "Lost money, gained skills" = LOSER (outcome matters)
- "Profitable but miserable" = Context-dependent
```

---

## EXAMPLE ROWS (FULL FACTS)

### CLAIM Example
```csv
data_id: DATA-001
classification: CLAIM
chapter_destination: CH01
full_content: "Course creator promises students can earn $10,000 per month within 90 days of starting their dropshipping store with no prior experience required. Sales page shows screenshots of student earnings but does not disclose how many students achieved these results or the time period involved."
source: Dropship Lifestyle Course Sales Page
source_url: https://dropshiplifestyle.com/join
evidence_grade: WEAK
collected_date: 2025-01-05
notes: Typical guru income claim without substantiation
```

### MECHANIC Example
```csv
data_id: DATA-015
classification: MECHANIC
chapter_destination: CH02
full_content: "Step 3: Create Facebook Business Manager account by navigating to business.facebook.com and clicking Create Account. Requires valid email and phone number for verification. Approval typically takes 24-48 hours but can take up to 7 days for new accounts. Business Manager is required to run Facebook and Instagram ads for e-commerce."
source: Facebook Official Documentation
source_url: https://www.facebook.com/business/help
evidence_grade: STRONG
step_number: 3
collected_date: 2025-01-05
notes: Official platform documentation
```

### COST Example
```csv
data_id: DATA-032
classification: COST
chapter_destination: CH03
full_content: "Shopify Basic Plan monthly subscription fee required to operate an online store with up to 2 staff accounts and basic reporting features. Includes free SSL certificate, abandoned cart recovery, and 24/7 support. Does not include advanced reporting or third-party calculated shipping rates."
source: Shopify Pricing Page 2024
source_url: https://www.shopify.com/pricing
evidence_grade: STRONG
amount_min: 29
amount_max: 29
frequency: monthly
collected_date: 2025-01-05
notes: Entry-level required cost
```

### OUTCOME Example
```csv
data_id: DATA-078
classification: OUTCOME
chapter_destination: CH04
full_content: "Karen, 34-year-old marketing coordinator employed full-time at a mid-size agency, invested $1,000 starting capital with 10-15 hours per week available for her dropshipping business. She purchased a $497 course recommended by a YouTube influencer, spent $2,900 on Facebook ads over 4 months testing 12 different products. Total revenue was $431 from 11 sales with 4 returns processed. Net loss of $3,223 including course, ads, Shopify subscription, and apps. Quit after month 4 due to stress, sleep deprivation, and unsustainable losses. Effective hourly rate across 200+ hours invested: negative $49.58 per hour."
source: Reddit r/dropshipping user testimony with transaction screenshots
source_url: https://reddit.com/r/dropshipping/comments/xxxxx
evidence_grade: STRONG
archetype: Side Hustler
label: LOSER
collected_date: 2025-01-05
notes: Classic failure pattern - course + ads + no traction
```

### CONSTRAINT Example
```csv
data_id: DATA-095
classification: CONSTRAINT
chapter_destination: CH05
full_content: "PayPal holds funds for 180 days on new merchant accounts with high chargeback risk categories including dropshipping, pre-orders, and digital goods. Funds remain inaccessible during hold period regardless of order fulfillment status or customer satisfaction. This policy applies to all new accounts and accounts with elevated risk indicators. Sellers report being unable to access tens of thousands of dollars during this period."
source: PayPal Merchant Policy Documentation
source_url: https://www.paypal.com/us/webapps/mpp/ua/acceptableuse-full
evidence_grade: STRONG
collected_date: 2025-01-05
notes: Major cash flow constraint many beginners don't know about
```

### RESOURCE Example
```csv
data_id: DATA-112
classification: RESOURCE
chapter_destination: CH08
full_content: "SCORE.org provides free one-on-one mentoring from experienced business professionals for small business owners and entrepreneurs. No cost to participants as SCORE is a nonprofit organization supported by the U.S. Small Business Administration. Mentors are volunteers with real business experience. Available both online and in-person at local chapters. Services include business plan review, financial guidance, and ongoing support."
source: SCORE Official Website
source_url: https://www.score.org
evidence_grade: STRONG
amount_min: 0
amount_max: 0
frequency: one-time
collected_date: 2025-01-05
notes: Legitimate free resource - no affiliate relationship
```

---

## WORKFLOW INTEGRATION

### Research Processor (3-Pass System)
```
PASS 1: Route by Classification
- Read raw dump
- Assign: CLAIM | MECHANIC | COST | OUTCOME | CONSTRAINT | RESOURCE
- Extract full_content (complete sentences, no abbreviations)

PASS 2: Assign Chapter Destination
- Apply routing matrix
- Set chapter_destination column

PASS 3: Classify Outcomes (OUTCOMES only)
- Analyze background, capital, experience, net result
- Assign one of 20 archetypes
- Assign WINNER or LOSER label
- Update archetype and label columns

OUTPUT: Populated data table ready for Neutral Author
```

### Neutral Author
```
INPUT: Data table filtered by chapter_destination
PROCESS: Write mega neutral narrative from table rows
OUTPUT: 8 mega neutral chapters (text only)

EXAMPLE:
- Filter: chapter_destination = "CH03"
- Result: All COST rows
- Write: Mega neutral chapter 3 covering all costs
```

### Y-It-itude Writer
```
INPUTS (3 sources):
1. Mega neutral chapter (narrative draft)
2. Data table filtered by chapter ← ULTIMATE AUTHORITY
3. Y-IT Tone Document

HIERARCHY RULE:
"If a number in the mega neutral text seems vague or doesn't match 
the data table, IGNORE the text. Defer to the verified table."

OUTPUT: Y-It voice chapter (text only)
```

---

## DATA TABLE VALIDATION CHECKLIST

Before using a data table in production:

```
[ ] Every row has data_id (unique)
[ ] Every row has classification
[ ] Every row has chapter_destination
[ ] Every row has full_content (complete sentences)
[ ] Every row has source
[ ] Every row has evidence_grade
[ ] OUTCOMES have archetype AND label
[ ] COSTS have amount_min and amount_max
[ ] MECHANICS have step_number
[ ] No abbreviations in full_content
[ ] No placeholder text ("TBD", "TODO", etc.)
[ ] All URLs tested and working
[ ] evidence_grade matches actual evidence quality
```

---

## VERSION HISTORY

- v1.0 (2025-01-07): Initial data table system
  - NotebookLM Data Tables = native app feature
  - Build 1 table at a time due to size
  - Full facts, no abbreviations
  - Chapter-sortable structure
  - 3-pass Research Processor integration

---

*End of Y-IT Data Table System v1.0*

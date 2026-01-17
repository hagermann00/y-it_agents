# Y-IT PROCESSING FRAMEWORK v1.0

## Data Routing & Classification Standards

This framework defines the "3-Pass System" used by the **Research Processor** to ensure data integrity across the swarm.

---

## THE CORE SCHEMA: 6-PILLAR EXTRACTION

Every piece of information extracted from a source MUST be assigned to one of these pillars.

| Pillar | ID | Description | Example |
| :--- | :--- | :--- | :--- |
| **CLAIM** | `CLM` | The stated promise or potential. | "Make $10k/month in 90 days." |
| **MECHANIC** | `MCH` | The operational steps or logic. | "Find a winning product on TikTok." |
| **COST** | `CST` | Direct and indirect financial/time requirements. | "Facebook ad spend: $20/day target." |
| **CONSTRAINT** | `CON` | Barriers, rules, and saturation points. | "PayPal holds 20% of funds for 90 days." |
| **OUTCOME** | `OUT` | Real-world results and case study data. | "Tyler lost $4.5k in month one." |
| **RESOURCE** | `RES` | Alternative paths or vetted tools. | "Standard S&P 500 return: 8-10%." |

---

## THE 3-PASS ROUTING LOGIC

### PASS 1: CLASSIFICATION (The "What")

- Identify the raw fact.
- Assign the Pillar ID (`CLM`, `MCH`, `CST`, etc.).
- Categorize by **Topic** (e.g., Dropshipping, Print on Demand).

### PASS 2: DESTINATION (The "Where")

- Map the data to the **Y-IT Universal Chapter Outline**.
- **Rule of Thumb:**
  - `CLM` → CH01 (The Hook)
  - `MCH` → CH02 (The Roadmap)
  - `CST` / `CON` → CH03 (The Engine Room) & CH05 (The Truth)
  - `OUT` → CH04 (The Trenches)
  - `RES` → CH07 (The Pivot) & CH08 (The Exit Ramp)

### PASS 3: ATOMIZATION (The "How Deep")

- For `OUTCOMES`, atomize into the **Financial Autopsy** format:
  - Startup Capital
  - Monthly Burn
  - Revenue
  - Profit/Loss
  - Time Invested
  - Effective Hourly Wage

---

## MASTER DATA TABLE (MDT) SPECIFICATIONS

The MDT is a CSV/Excel file formatted for NotebookLM.

### MDT COLUMN HEADERS

1. `Classification_ID`: (e.g., CST-CH03-001)
2. `Pillar`: (CLAIM/MECHANIC/COST/etc.)
3. `Chapter_Dest`: (CH01-CH08)
4. `Subject`: (e.g., Facebook Ad CPM)
5. `Data_Point`: (The specific number or fact)
6. `Context`: (Contextual notes for the Writer)
7. `Archetype`: (For OUTCOMES: Tyler, Karen, etc.)
8. `Label`: (WINNER/LOSER)
9. `Source_URL`: (Provenance)

---

## ERROR HANDLING & QUALITY CONTROL

- **Hallucinated Data:** Any entry without a `Source_URL` or specific `Data_Point` is flagged for deletion.
- **Ambiguous Mapping:** If a fact fits two pillars, duplicate it with unique `Classification_ID`s and contexts.
- **Conflict Resolution:** If two sources provide different numbers, include BOTH with a "Conflict" flag for the **Neutral Author** to address.

---
*End of Y-IT Processing Framework v1.0*

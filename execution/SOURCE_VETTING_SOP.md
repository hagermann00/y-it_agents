# SOURCE VETTING & EXTRACTION SOP v2.0 — MULTI-AI SYNTHESIS
## Processing 500 Sources → Verified Data Table
## Synthesized from: Gemini + ChatGPT + Perplexity + Grok

**Purpose:** Bridge the gap between research collection and data table assembly  
**Primary Tool:** NotebookLM (with multi-agent verification layer)  
**Status:** FINAL — Ready for implementation

---

## EXECUTIVE SUMMARY

**Multi-AI Consensus:**
All four consulted AIs (Gemini, ChatGPT, Perplexity, Grok) agreed on:
- ✅ Batch processing (25-50 sources per batch)
- ✅ Schema-first extraction with structured outputs
- ✅ Citation anchoring and verification
- ✅ Multi-stage credibility scoring
- ✅ Preserving qualitative context while maintaining computational scale

**Unified Architecture:**
```
5-LAYER VERIFICATION SYSTEM

Layer 1: BATCH (Gemini's NotebookLM workflow)
├─ Worker Notebooks: 25-40 sources each
├─ SOP Anchor pattern: Upload research SOP as Source #1
└─ Golden Prompt standardization

Layer 2: EXTRACT (Perplexity's schema-optimized approach)
├─ PARSE framework (64.7% accuracy gains)
├─ Structured outputs (JSON Schema enforcement)
└─ Flat schemas, explicit enums, examples

Layer 3: VERIFY (Grok's adversarial pairs)
├─ Dual-LLM: Extractor + Critic
├─ Hallucination detection (HHEM, LettuceDetect)
└─ Citation verification (LLatrieval, SourceCheckup benchmarks)

Layer 4: SCORE (ChatGPT's credibility framework)
├─ Reputation signals (50 points)
├─ Content quality (30 points)
├─ Extraction confidence (10 points)
└─ Cross-source agreement (10 points)

Layer 5: RESOLVE (Grok's multi-agent debate)
├─ Conflict detection via debate systems
├─ Consensus-based resolution
└─ Flag unresolved conflicts for human review
```

---

## PHASE 1: TRIAGE & PREPARATION

### Goal
Reduce 500 raw sources to ~300 "Golden Sources" and prepare batch structure.

### Step 1.1: Source Manifest Creation

**Template (Google Sheets):**
```
| Source_ID | Title | Type | Date | Category | Quality_Tier | Status | Batch_ID |
|-----------|-------|------|------|----------|--------------|--------|----------|
| 001       | [...]  | PDF  | 2024 | CLAIM    | STRONG       | KEEP   | NB01     |
```

**Quality Tiers (Pre-Assessment):**
```
STRONG:
├─ Peer-reviewed academic papers
├─ Official government/platform statistics
├─ Verified case studies with receipts
└─ Deep Research sessions (NotebookLM)

MEDIUM:
├─ Industry reports from established outlets
├─ YouTube videos with specific data
├─ Reddit threads with screenshots/proof
└─ News articles from reputable sources

WEAK:
├─ Forum posts (anecdotal)
├─ Guru marketing materials
├─ Unverified testimonials
└─ Social media posts
```

### Step 1.2: Create Research SOP Document

**Critical Innovation (Gemini):** Upload a "Research SOP" as Source #1 in every Worker Notebook.

**SOP Document Contents:**
```markdown
# Y-IT Research Extraction SOP

## Your Role
You are extracting data for a Y-IT satirical exposé book on [TOPIC].

## Data Classifications
- CLAIM: Income promises, success rates, guru statements
- MECHANIC: How-to steps, processes, technical requirements
- COST: Startup costs, monthly expenses, hidden fees
- OUTCOME: Financial results, case studies, win/loss records
- CONSTRAINT: Barriers, failure causes, systemic issues
- RESOURCE: Tools, platforms, alternatives

## Evidence Quality Standards
- STRONG: Receipts, screenshots, specific numbers with context
- MEDIUM: Specific claims with partial verification
- WEAK: Anecdotal, vague, or unverified

## Extraction Rules
1. Extract ONLY what is explicitly stated in sources
2. DO NOT infer or guess missing data
3. Preserve qualitative "body dialog flavor" (exact quotes)
4. Maintain citation traceability for every data point
5. Flag conflicts between sources
```

**Save as:** `Y-IT_Research_SOP_[Topic].pdf`

---

## PHASE 2: BATCH ARCHITECTURE (Gemini's NotebookLM Workflow)

### Optimal Batch Structure

**Batch Size:** 25-40 sources per Worker Notebook
- **Why 25-40?** (Gemini consensus)
  - Maintains LLM attention span
  - Citation hover remains practical
  - Reduces hallucination risk
  - Manageable export size

**Batch Organization:**
```
OPTION A: Category-Based (Recommended)
├─ NB01_CLAIMS (30 sources)
├─ NB02_MECHANICS (28 sources)
├─ NB03_COSTS (35 sources)
├─ NB04_OUTCOMES_Winners (25 sources)
├─ NB05_OUTCOMES_Losers (40 sources)
├─ NB06_CONSTRAINTS (32 sources)
└─ NB07_RESOURCES (30 sources)

OPTION B: Quality-Tiered
├─ NB01_STRONG_Evidence (40 sources)
├─ NB02_MEDIUM_Evidence (35 sources)
└─ NB03_WEAK_Evidence (30 sources)
```

### Worker Notebook Setup

**For each batch:**
```
1. Create NotebookLM notebook
2. Name: "Y-IT [Topic] - Batch [##] - [Category]"
3. Upload Source #1: Research SOP PDF ← CRITICAL
4. Upload Sources #2-41: Batch sources (sorted by quality tier)
5. Verify: All uploads successful
6. Record: Notebook URL in manifest
```

---

## PHASE 3: SCHEMA-OPTIMIZED EXTRACTION (Perplexity + ChatGPT)

### The Golden Prompt (Enhanced with PARSE Framework)

**Key Innovation (Perplexity):** Schema optimization yields 64.7% accuracy gains.

**Schema Design Principles:**
- ✅ Flat structure (avoid deep nesting)
- ✅ Explicit enums for categorical fields
- ✅ Clear field descriptions (natural language contract)
- ✅ Examples for each field type
- ❌ Avoid nullable branches
- ❌ Avoid overly complex schemas

**Golden Prompt Template:**
```
ROLE: Research Data Extractor for Y-IT Book Production

CONTEXT: You have access to a Research SOP (Source #1) that defines data classifications, evidence standards, and extraction rules. Follow it precisely.

TASK: Extract structured data from all sources in this notebook.

OUTPUT SCHEMA (JSON):
{
  "batch_metadata": {
    "batch_id": "NB[##]",
    "category": "CLAIM|MECHANIC|COST|OUTCOME|CONSTRAINT|RESOURCE",
    "sources_processed": ["list of all source titles"],
    "extraction_date": "YYYY-MM-DD"
  },
  "data_points": [
    {
      "source_id": "integer (1-40)",
      "source_title": "exact title",
      "data_type": "CLAIM|MECHANIC|COST|OUTCOME|CONSTRAINT|RESOURCE",
      "claim_or_fact": "extracted data point",
      "evidence_quality": "STRONG|MEDIUM|WEAK",
      "citation": "[x]",
      "context": "surrounding context or quote",
      "date": "YYYY-MM or YYYY-MM-DD if available",
      "credibility_signals": {
        "has_receipts": boolean,
        "has_specific_numbers": boolean,
        "author_credentials": "string or null",
        "publication_type": "academic|industry|community|promotional"
      }
    }
  ]
}

EXTRACTION RULES:
1. Process EVERY source (verify count matches uploaded sources)
2. Extract ALL relevant data points (1 source may yield 3-10 data points)
3. If data not found, write "NOT_FOUND" - DO NOT GUESS
4. Include citation [x] for EVERY data point
5. Preserve exact quotes for qualitative data
6. Flag conflicts if sources disagree on same fact

CREDIBILITY ASSESSMENT (per data point):
- Check: Is this peer-reviewed? (academic signal)
- Check: Does it have receipts/screenshots? (evidence signal)
- Check: Is author credentialed? (authority signal)
- Check: Is tone balanced or hyperbolic? (bias signal)

OUTPUT: Valid JSON matching schema above.

BEGIN EXTRACTION.
```

### Execution

**Step 3.1: Run Golden Prompt**
```
1. Open Worker Notebook (e.g., NB01_CLAIMS)
2. Start new chat
3. Paste Golden Prompt
4. Wait for complete JSON response
5. Copy JSON output
```

**Step 3.2: Parse and Validate**
```
Tools (Perplexity recommendations):
├─ Instructor.py (Python): Pydantic models + constrained decoding
├─ OpenAI Structured Outputs: JSON Schema enforcement
├─ Outlines / Langroid: Framework-level validation
└─ Simon Willison's llm CLI: Schema registry for batch processing

Process:
1. Parse JSON (validate against schema)
2. Check: sources_processed count = uploaded source count?
3. Check: All data_points have citations?
4. Check: No "null" in required fields?
5. If validation fails: Re-run with error feedback
```

---

## PHASE 4: ADVERSARIAL VERIFICATION (Grok's Dual-LLM System)

### The Extractor-Critic Pattern

**Key Innovation (Grok):** Adversarial pairs reduce errors by 15-30% vs single-LLM.

**Architecture:**
```
LLM #1: EXTRACTOR (Primary)
├─ Runs Golden Prompt
├─ Outputs initial JSON
└─ Focus: Comprehensive extraction

LLM #2: CRITIC (Adversarial)
├─ Reviews Extractor's JSON
├─ Flags hallucinations, unsupported claims
├─ Suggests corrections
└─ Focus: Accuracy and grounding
```

**Critic Prompt Template:**
```
ROLE: Quality Assurance Critic for Research Extraction

INPUT: JSON output from Extractor LLM (see below)

TASK: Review for accuracy, hallucinations, and unsupported claims.

VERIFICATION CHECKLIST:
1. Citation Integrity
   - Every data_point has valid citation [x]?
   - Citation numbers exist in source list?
   - No orphan citations?

2. Hallucination Detection
   - Suspiciously round numbers? (e.g., exactly $10,000)
   - Data point appears multiple times with different citations?
   - Evidence quality = STRONG but claim is vague?
   - Dates impossible? (future or too old)

3. Grounding Check
   - Hover over citations in NotebookLM
   - Does source text support extracted claim?
   - Is context preserved accurately?
   - Are quotes exact?

4. Credibility Signals Accuracy
   - publication_type matches source?
   - author_credentials verified?
   - has_receipts/has_specific_numbers accurate?

OUTPUT SCHEMA:
{
  "review_summary": {
    "total_data_points": integer,
    "flagged_count": integer,
    "confidence_score": 0-100
  },
  "flagged_items": [
    {
      "data_point_index": integer,
      "issue_type": "hallucination|unsupported|misattribution|quality_mismatch",
      "explanation": "string",
      "suggested_correction": "string or null",
      "severity": "critical|moderate|minor"
    }
  ],
  "overall_assessment": "PASS|REVIEW_REQUIRED|FAIL"
}

BEGIN REVIEW.
```

**Execution:**
```
1. Run Extractor (Golden Prompt) → Get JSON_v1
2. Run Critic (Review Prompt) → Get Review Report
3. If overall_assessment = "PASS": Accept JSON_v1
4. If "REVIEW_REQUIRED": Apply suggested corrections → JSON_v2
5. If "FAIL": Re-run Extractor with stricter instructions
```

### Hallucination Detection Tools (Grok + Perplexity)

**Automated Checks:**
```
HHEM (Hughes Hallucination Evaluation Model):
├─ Detects unsupported claims
├─ Compares output to source documents
└─ Benchmark: 72-95% agreement with human evaluators

LettuceDetect (2025 Lightweight):
├─ Fast encoder-based detection
├─ Suitable for batch processing
└─ Resource-efficient

RAGAS / DeepEval:
├─ Faithfulness metrics
├─ Relevance scoring
└─ Consistency checks
```

**Integration:**
```
For each data_point in JSON:
1. Run HHEM/LettuceDetect
2. Get hallucination_score (0-1)
3. If score > 0.3: Flag for human review
4. Add to data_point: "hallucination_risk": score
```

---

## PHASE 5: CREDIBILITY SCORING (ChatGPT's Framework)

### 4-Tier Scoring System

**Total Score: 0-100 points**

**Tier 1: Reputation Signals (50 points)**
```
Signal                          | Weight | Scoring
--------------------------------|--------|------------------
Academic vs non-academic        | 15     | Peer-reviewed = 15, Industry = 10, Community = 5, Promotional = 0
Publication reputation          | 15     | Established outlet = 15, Known blog = 10, Unknown = 5, Spam = 0
Author credentials              | 10     | Expert = 10, Practitioner = 7, Unknown = 3, Anonymous = 0
Citation network                | 5      | Many citations = 5, Some = 3, None = 0
Domain authority                | 5      | .edu/.gov = 5, .org = 3, .com = 2, Unknown = 0
```

**Tier 2: Content Quality Signals (30 points)**
```
Feature                         | Weight | Scoring
--------------------------------|--------|------------------
Evidence markers                | 10     | Receipts/screenshots = 10, Specific numbers = 7, Vague = 3, None = 0
Balanced tone                   | 8      | Neutral = 8, Slight bias = 5, Hyperbolic = 2
Statistical citations           | 7      | Present with sources = 7, Present no sources = 4, Absent = 0
Unsupported claims              | 5      | None = 5, Few = 3, Many = 0
```

**Tier 3: Extraction Confidence (10 points)**
```
Model/rule confidence           | 10     | High (>0.9) = 10, Medium (0.7-0.9) = 7, Low (<0.7) = 3
```

**Tier 4: Cross-Source Agreement (10 points)**
```
Consensus alignment             | 10     | All sources agree = 10, Most agree = 7, Split = 4, Contradictory = 0
```

### Scoring Implementation

**Step 5.1: Automated Scoring**
```
For each data_point:
1. Extract credibility_signals from JSON
2. Calculate Tier 1 (reputation): Sum weighted signals
3. Calculate Tier 2 (content): Sum quality features
4. Calculate Tier 3 (confidence): From LLM log-probabilities or Critic score
5. Calculate Tier 4 (cross-source): Compare to other data_points on same fact
6. TOTAL_SCORE = Tier1 + Tier2 + Tier3 + Tier4
7. Add to data_point: "credibility_score": TOTAL_SCORE
```

**Step 5.2: Score-Based Filtering**
```
SCORE RANGES:
├─ 80-100: HIGH CREDIBILITY (use confidently)
├─ 60-79:  MEDIUM CREDIBILITY (cross-check recommended)
├─ 40-59:  LOW CREDIBILITY (flag for review)
└─ 0-39:   VERY LOW (discard or mark as anecdotal only)
```

---

## PHASE 6: CONFLICT RESOLUTION (Grok's Multi-Agent Debate)

### When Sources Disagree

**Conflict Detection:**
```
For each fact type (e.g., "Dropshipping failure rate"):
1. Group all data_points claiming same fact
2. Extract values (e.g., "87%", "90%", "85%")
3. Calculate variance: |max - min| / max
4. If variance > threshold (e.g., 10%): Flag as conflict
```

**Multi-Agent Debate System (Grok's Innovation):**

**Agent 1: ADVOCATE**
```
ROLE: Argue for consensus interpretation

PROMPT:
"Multiple sources report [TOPIC] with values: [87%, 90%, 85%].

TASK: Argue that these sources fundamentally agree.
- Explain variance as contextual (different time periods, sample sizes, definitions)
- Propose consensus value or range
- Cite supporting evidence from sources

OUTPUT: Consensus argument with confidence score."
```

**Agent 2: DEVIL'S ADVOCATE**
```
ROLE: Argue for genuine contradiction

PROMPT:
"Multiple sources report [TOPIC] with values: [87%, 90%, 85%].

TASK: Argue that these sources genuinely contradict.
- Explain variance as methodological differences or conflicting data
- Identify which source is most credible
- Flag unresolved issues

OUTPUT: Contradiction argument with confidence score."
```

**Resolution Process:**
```
1. Run both agents in parallel
2. Compare confidence scores
3. If Advocate confidence > Devil's Advocate:
   └─ RESOLVED: Use consensus value/range
4. If Devil's Advocate confidence > Advocate:
   └─ UNRESOLVED: Flag for human review, present both interpretations
5. If scores similar:
   └─ CONTEXTUAL: Document variance, use range, note limitations
```

**Benchmark (Grok):** Multi-agent systems outperform single-agent by 15-30% on complex conflict detection.

---

## PHASE 7: CITATION VERIFICATION AT SCALE (Perplexity Benchmarks)

### Citation Verification Standards

**Benchmarks (Perplexity):**
```
LLatrieval (NAACL 2024):
├─ Citation Recall, Precision, F1 metrics
├─ ALCE benchmark for verifiable generation
└─ Target: >90% citation accuracy

SourceCheckup (Nature 2025):
├─ Agent pipeline scoring relevance/supportiveness
├─ ~90% agreement between frontier models
└─ Automated source quality assessment
```

### Verification Process

**Step 7.1: Automated Alignment**
```
For each data_point:
1. Extract claim_or_fact text
2. Retrieve source document via citation [x]
3. Compute token overlap between claim and source chunk
4. Calculate embedding similarity (cosine distance)
5. Generate support_score: 0-1 (1 = perfect match)
6. If support_score < 0.7: Flag for manual review
```

**Step 7.2: Manual Spot-Checking (Statistical Sampling)**

**Sampling Strategy:**
```
LEVEL 1 — SPOT CHECK (10% sample):
├─ Random sample across all batches
├─ Time: ~5 min per batch
└─ Use for: WEAK evidence, low-stakes data

LEVEL 2 — STANDARD VET (25% sample):
├─ Stratified sample (mix of quality tiers)
├─ Time: ~15 min per batch
└─ Recommended for: Most data (95%+ accuracy target)

LEVEL 3 — FULL VET (100% verification):
├─ Every data point verified
├─ Time: ~45 min per batch
└─ Required for: STRONG evidence, financial figures, case studies
```

**Citation Hover Method (Gemini):**
```
For each sampled data_point:
1. Locate citation [x] in NotebookLM chat
2. Hover over [x]
3. NotebookLM highlights source paragraph
4. READ highlighted text
5. COMPARE to extracted claim_or_fact

VERIFY:
├─ Numbers match exactly?
├─ Context preserved?
├─ Attribution correct?
└─ Date accurate?

MARK:
├─ ✅ MATCH: Data accurate
├─ ⚠️ MINOR: Close but needs adjustment
├─ ❌ FAIL: Wrong or hallucinated
```

**Error Threshold:**
```
If error rate > 5% in sample:
├─ ESCALATE to LEVEL 3 (full vet)
├─ FLAG batch as high-risk
└─ Re-run extraction with stricter prompt

If error rate < 5%:
├─ ACCEPT batch
└─ Proceed to export
```

---

## PHASE 8: MASTER ASSEMBLY & FINAL VALIDATION

### Export and Merge

**Step 8.1: Export from Worker Notebooks**
```
For each verified batch:
1. Export JSON to file: NB[##]_verified.json
2. Convert to CSV/Google Sheets if needed
3. Add Batch_ID column to all rows
4. Verify: Column alignment with schema
```

**Step 8.2: Create Master Data Table**
```
Google Sheet: "Y-IT_[Topic]_MASTER_DATA_TABLE"

Columns:
├─ Batch_ID
├─ Source_ID
├─ Source_Title
├─ Data_Type
├─ Claim_or_Fact
├─ Evidence_Quality
├─ Citation (composite: "NB[##]-[x]")
├─ Context
├─ Date
├─ Credibility_Score (0-100)
├─ Hallucination_Risk (0-1)
├─ Support_Score (0-1)
└─ Conflict_Status (RESOLVED|UNRESOLVED|CONTEXTUAL)
```

**Step 8.3: Merge All Batches**
```
1. Import NB01_verified.json → Append to Master
2. Update citations: [1] → "NB01-[1]"
3. Repeat for NB02, NB03, etc.
4. Verify: Total row count = sum of batch counts
```

### Final Validation Checklist

**Completeness:**
```
✓ All sources from manifest processed?
✓ sources_processed lists match uploaded sources?
✓ No missing batches?
✓ Row count ≥ source count? (1+ rows per source)
```

**Quality:**
```
✓ Error rate < 5% across all batches?
✓ Credibility scores distributed reasonably?
✓ High-impact data (case studies, stats) 100% verified?
✓ Conflicts resolved or flagged?
```

**Traceability:**
```
✓ Every row has composite citation?
✓ Citation Index complete?
✓ Can trace any data point back to source?
✓ NotebookLM URLs recorded?
```

---

## WORKFLOW SUMMARY (5-Layer System)

```
┌─────────────────────────────────────────────────────────────┐
│ LAYER 1: BATCH (Gemini)                                     │
│ ├─ Input: 300 golden sources                                │
│ ├─ Process: Create 8-10 Worker Notebooks (25-40 sources)    │
│ ├─ Innovation: SOP Anchor (upload SOP as Source #1)         │
│ └─ Output: Structured batches ready for extraction          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ LAYER 2: EXTRACT (Perplexity)                               │
│ ├─ Input: Worker Notebooks with sources                     │
│ ├─ Process: Run Golden Prompt (PARSE-optimized schema)      │
│ ├─ Innovation: 64.7% accuracy gains via schema design       │
│ └─ Output: JSON data tables per batch                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ LAYER 3: VERIFY (Grok)                                      │
│ ├─ Input: Extractor JSON                                    │
│ ├─ Process: Critic LLM reviews + hallucination detection    │
│ ├─ Innovation: Adversarial pairs (15-30% error reduction)   │
│ └─ Output: Verified JSON with flagged issues                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ LAYER 4: SCORE (ChatGPT)                                    │
│ ├─ Input: Verified data points                              │
│ ├─ Process: 4-tier credibility scoring (0-100)              │
│ ├─ Innovation: Reputation + Content + Confidence + Consensus│
│ └─ Output: Scored data points with quality grades           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ LAYER 5: RESOLVE (Grok)                                     │
│ ├─ Input: Scored data points with conflicts                 │
│ ├─ Process: Multi-agent debate (Advocate vs Devil's Adv.)   │
│ ├─ Innovation: Consensus-based conflict resolution          │
│ └─ Output: Resolved/flagged conflicts, final Master Table   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ FINAL OUTPUT: VERIFIED MASTER DATA TABLE                    │
│ ├─ ~2000+ data points from 300 sources                      │
│ ├─ <5% error rate (95%+ accuracy)                           │
│ ├─ Full citation traceability                               │
│ ├─ Credibility scores (0-100)                               │
│ ├─ Conflict resolution status                               │
│ └─ Ready for: Research Processor → Data Table Assembly      │
└─────────────────────────────────────────────────────────────┘

TOTAL TIME ESTIMATE: 12-20 hours for 300 sources
```

---

## TOOLS & IMPLEMENTATION

### Required Tools

**Primary:**
- NotebookLM (Google): Batch processing, citation hover
- Google Sheets: Master table assembly, manifest tracking

**Recommended (Perplexity):**
- Instructor.py: Pydantic models + constrained decoding
- OpenAI Structured Outputs: JSON Schema enforcement
- Simon Willison's llm CLI: Schema registry for batch processing

**Optional (Advanced):**
- HHEM / LettuceDetect: Hallucination detection
- RAGAS / DeepEval: Quality metrics
- LangChain / LlamaIndex: Orchestration frameworks

### Implementation Checklist

**Pre-Flight:**
```
[ ] Source Manifest created (Google Sheets)
[ ] Research SOP document written and saved as PDF
[ ] Batch structure planned (category-based or quality-tiered)
[ ] Golden Prompt customized for topic
[ ] Critic Prompt prepared
[ ] Debate Agent prompts ready
```

**Execution:**
```
[ ] Phase 1: Triage complete (~300 sources)
[ ] Phase 2: Worker Notebooks created (8-10 batches)
[ ] Phase 3: Golden Prompt run in all batches
[ ] Phase 4: Critic review complete, JSON verified
[ ] Phase 5: Credibility scores calculated
[ ] Phase 6: Conflicts resolved or flagged
[ ] Phase 7: Citation verification (25% sample minimum)
[ ] Phase 8: Master Table assembled and validated
```

**Post-Processing:**
```
[ ] Error rate < 5% confirmed
[ ] Completeness verification passed
[ ] Citation Index created
[ ] High-impact data 100% verified
[ ] Ready for Research Processor handoff
```

---

## TROUBLESHOOTING

### High Hallucination Rate (>10%)

**Causes:**
- Batch too large (>50 sources)
- Prompt too vague
- Complex/contradictory sources

**Solutions:**
1. Reduce batch size to 25-30
2. Strengthen Golden Prompt with stricter rules
3. Add explicit "DO NOT GUESS" instruction
4. Run Critic LLM on all batches (not just sample)

### Low Credibility Scores Across Board

**Causes:**
- Weak source quality (too many WEAK tier)
- Scoring rubric too harsh
- Missing metadata for reputation signals

**Solutions:**
1. Re-assess source quality in Phase 1
2. Adjust scoring weights (reduce reputation if sources are inherently community-based)
3. Enrich source metadata (author credentials, publication type)

### Unresolved Conflicts Pile Up

**Causes:**
- Genuinely contradictory sources
- Debate agents not reaching consensus
- Threshold too sensitive

**Solutions:**
1. Accept that some conflicts are legitimate (document variance)
2. Adjust debate agent prompts to be more decisive
3. Increase conflict threshold (e.g., 10% → 15% variance)
4. Flag for human expert review

---

## NEXT STEPS AFTER MASTER TABLE

```
MASTER DATA TABLE (verified, scored, ~2000 rows)
        ↓
RESEARCH PROCESSOR PROMPT (execution/)
├─ Input: Master Table rows
├─ Process: 3-pass classification refinement
├─ Output: Data Table rows ready for assembly
        ↓
DATA TABLE ASSEMBLY (NotebookLM Custom Tables)
├─ Input: Classified rows
├─ Process: Sequential category-based table creation
├─ Output: Final Y-IT Data Tables by chapter
        ↓
NEUTRAL AUTHOR / Y-IT-ITUDE WRITER
└─ Consumes: Data Tables as ultimate authority
```

---

## MULTI-AI ATTRIBUTION

**This SOP synthesizes recommendations from:**

**Gemini (Deep Think):**
- NotebookLM batch architecture (25-40 sources)
- SOP Anchor pattern
- Citation hover verification
- Preserving qualitative "body dialog flavor"

**ChatGPT (GPT-4):**
- 4-tier credibility scoring framework (50+30+10+10)
- External signal matrix
- Human-in-the-loop gates
- 9-stage engineering pipeline

**Perplexity (Search + Analysis):**
- PARSE schema optimization (64.7% gains)
- Citation verification benchmarks (90% agreement)
- Structured output tools (Instructor, OpenAI JSON mode)
- Simon Willison's llm CLI workflow

**Grok (xAI 4.1):**
- Dual-LLM adversarial extraction (Extractor + Critic)
- Multi-agent debate systems (15-30% improvement)
- Hallucination detection (HHEM, LettuceDetect)
- 72-95% human evaluator agreement benchmark

---

## VERSION HISTORY

- v1.0 (2026-01-08): Initial SOP based on Gemini Deep Think
- v2.0 (2026-01-08): **MULTI-AI SYNTHESIS**
  - Integrated Gemini's NotebookLM workflow
  - Added ChatGPT's credibility scoring framework
  - Incorporated Perplexity's schema optimization and tools
  - Implemented Grok's adversarial verification and debate systems
  - 5-layer architecture: Batch → Extract → Verify → Score → Resolve

---

**STATUS:** FINAL — Ready for pilot testing with 100-source batch

**Recommendation:** Test with 100-source pilot before scaling to full 500

---

*END OF SOURCE VETTING & EXTRACTION SOP v2.0 — MULTI-AI SYNTHESIS*

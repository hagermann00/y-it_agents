# GEMINI FORGE - Full System Specification

> **Purpose**: A complete, local-first image generation pipeline that wraps browser-based Gemini Ultra ("Nano Banana Pro") for industrial-scale book asset production.

---

## EXECUTIVE SUMMARY

Build a Python-based automation system that:

1. **Reads** structured YAML prompt batches
2. **Automates** Chrome browser to submit prompts to gemini.google.com
3. **Downloads** generated images with strict naming conventions
4. **Presents** a visual review interface for human selection
5. **Finalizes** approved assets into book-ready directory structures

**ZERO API COSTS** - All generation uses the user's existing Gemini Ultra subscription via browser automation, not paid API endpoints.

---

## CONSTRAINTS (NON-NEGOTIABLE)

| Constraint | Requirement |
|------------|-------------|
| API Costs | ZERO - Must use browser automation only |
| Execution | 100% local Python, no cloud services |
| Browser | Chrome with existing Gemini Ultra login |
| Output | 300 DPI minimum for print-ready assets |
| Scale | Handle 100+ prompts × 3 variants = 300+ images per batch |
| Integration | Must work as "wrapper" driven by Antigravity agent |

---

## ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                        GEMINI FORGE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   BATCHES    │───▸│    MINER     │───▸│   STAGING    │       │
│  │  (YAML)      │    │  (Selenium)  │    │  (Raw imgs)  │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         ▲                                       │                │
│         │                                       ▼                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  ANTIGRAVITY │    │    REVIEW    │◀───│   REVIEWED   │       │
│  │  (Prompts)   │    │  (Streamlit) │    │  (Approved)  │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                             │                    │               │
│                             ▼                    ▼               │
│                      ┌──────────────┐    ┌──────────────┐       │
│                      │   REJECTED   │    │    FINAL     │       │
│                      │              │    │ (Book-ready) │       │
│                      └──────────────┘    └──────────────┘       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐       │
│  │            LOCAL AI BACKUP (Ollama)                   │       │
│  │  llama3.2-vision for quality analysis & verification  │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## DIRECTORY STRUCTURE

```
c:\iiwii_db\y-it_agents\forge\
├── __init__.py
├── config.py           # Constants, paths, delays
├── forge_miner.py      # Browser automation (Selenium)
├── forge_review.py     # Streamlit review UI
├── forge_finalize.py   # Asset finalization
├── forge_audit.py      # DPI/quality checker
├── FORGE_SPEC.md       # This specification
│
├── utils/
│   ├── __init__.py
│   ├── file_router.py  # Naming and sorting logic
│   └── ollama_client.py # Local AI integration
│
├── staging/            # Raw generated images (unreviewed)
├── reviewed/           # User-approved images
├── final/              # Book-ready assets (renamed, organized)
├── rejected/           # Images not selected
└── logs/               # Execution logs and manifests
```

---

## INPUT FORMAT: YAML BATCH

```yaml
book: y_it_aaa              # Project identifier
chapter: ch01               # Chapter identifier
images:
  - id: posibot_shrug       # Unique image ID
    type: CHARACTER_SHEET   # Asset type (for routing)
    prompt: "PosiBot doing a confused shrug. Gold body, cyan screen. Precise Cartoon style."
    placement: sidebar      # Where in manuscript
    caption: "PosiBot contemplates life choices"
    
  - id: chad_facepalm
    type: SCENE
    prompt: "Chad in green shirt doing facepalm. Editorial illustration style."
    placement: inline
    caption: "Reality hits different"
```

---

## COMPONENT SPECIFICATIONS

### 1. FORGE MINER (`forge_miner.py`)

**Purpose**: Automate Chrome to generate images via Gemini.

**CLI Interface**:

```bash
python forge_miner.py --batch batches/posibot_pilot.yaml [OPTIONS]

Options:
  --variants N      Number of variants per prompt (default: 3)
  --delay N         Seconds between requests (default: 10)
  --headless        Run Chrome in headless mode
  --resume          Resume from last completed prompt
  --profile PATH    Chrome profile directory (for login persistence)
```

**Workflow per Prompt**:

1. Parse YAML batch file
2. For each image entry:
   a. Open gemini.google.com (or refresh)
   b. Locate text input field
   c. Input prompt text (with variant suffix: "Version A", "Version B", "Version C")
   d. Click submit/generate button
   e. Wait for image generation (poll DOM for image element)
   f. Right-click and save image (or extract src and download)
   g. Apply naming: `{book}_{chapter}_{id}_v{variant}_{timestamp}.png`
   h. Save to `staging/`
   i. Log to `logs/manifest.json`
   j. Wait delay seconds before next

**Error Handling**:

- Screenshot on failure → `logs/errors/`
- Retry up to 3 times
- Skip and log on persistent failure
- Resume capability via manifest checkpoint

**DOM Selectors** (to be updated if Gemini UI changes):

```python
SELECTORS = {
    "input_field": ["textarea[placeholder*='Enter']", "div[contenteditable='true']"],
    "submit_button": ["button[aria-label*='Send']", "button.send-button"],
    "image_result": ["img.generated-image", "div.image-container img"],
    "loading_indicator": ["div.loading", "span.generating"]
}
```

---

### 2. FORGE REVIEW (`forge_review.py`)

**Purpose**: Streamlit-based UI for visual selection of generated images.

**Features**:

1. **Visual Grid**: Display 3 variants side-by-side per prompt
2. **Metadata Panel**: Show prompt, filename, dimensions, DPI
3. **DPI Auditor**: Flag images below 300 DPI threshold
4. **Selection Actions**:
   - ✅ Approve → Move to `reviewed/`
   - ❌ Reject → Move to `rejected/`
   - 🔄 Flag for Upscale → Tag in manifest
5. **Bulk Operations**: Approve all, reject all, filter by type
6. **Progress Tracker**: Batch completion percentage

**UI Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│ GEMINI FORGE - Review Dashboard                    [Batch v]│
├─────────────────────────────────────────────────────────────┤
│ Progress: ████████░░░░░░░░ 45/100 reviewed                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                     │
│  │ Variant │  │ Variant │  │ Variant │     Prompt:         │
│  │    A    │  │    B    │  │    C    │     "PosiBot..."    │
│  │         │  │         │  │         │                     │
│  │  [DPI]  │  │  [DPI]  │  │  [DPI]  │     Type: SCENE     │
│  └─────────┘  └─────────┘  └─────────┘     Placement: inline│
│                                                             │
│  [✅ Approve A] [✅ Approve B] [✅ Approve C] [❌ Reject All]│
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  (Next prompt group...)                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Run Command**:

```bash
streamlit run forge_review.py
```

---

### 3. FORGE FINALIZE (`forge_finalize.py`)

**Purpose**: Move reviewed assets to book-ready locations with final naming.

**CLI Interface**:

```bash
python forge_finalize.py --project y_it_aaa --chapter ch01

Options:
  --dry-run         Show what would be moved without moving
  --output PATH     Override default output directory
```

**Output Structure**:

```
c:\iiwii_db\y-it_agents\05_PROJECTS\y_it_aaa\ASSETS\
├── ch01\
│   ├── ch01_img01_posibot_shrug.png
│   ├── ch01_img02_chad_facepalm.png
│   └── ...
├── ch02\
│   └── ...
└── manifest.json   # Maps final names to original prompts
```

**Naming Convention**: `{chapter}_{sequence:02d}_{description}.png`

---

### 4. FORGE AUDIT (`forge_audit.py`)

**Purpose**: Check image quality (DPI, dimensions) for print readiness.

**CLI Interface**:

```bash
python forge_audit.py --folder staging/

Output:
✅ posibot_shrug_v1.png - 1024x1024 @ 300 DPI
⚠️ chad_facepalm_v2.png - 512x512 @ 72 DPI (BELOW THRESHOLD)
✅ posibot_shrug_v2.png - 1024x1024 @ 300 DPI
```

**Threshold**: 300 DPI minimum for KDP print requirements.

---

### 5. UTILITIES

#### `utils/file_router.py`

- Generate standardized filenames from metadata
- Parse existing filenames to extract metadata
- Validate naming convention compliance

#### `utils/ollama_client.py`

- Connect to local Ollama instance
- Query llama3.2-vision for image analysis
- Functions:
  - `analyze_quality(image_path)` → Quality assessment
  - `verify_content(image_path, prompt)` → Does image match prompt?
  - `suggest_upscale(image_path)` → Would upscaling help?

---

## CONFIG (`config.py`)

```python
# Paths
FORGE_ROOT = Path("c:/iiwii_db/y-it_agents/forge")
STAGING_DIR = FORGE_ROOT / "staging"
REVIEWED_DIR = FORGE_ROOT / "reviewed"
FINAL_DIR = FORGE_ROOT / "final"
REJECTED_DIR = FORGE_ROOT / "rejected"
LOGS_DIR = FORGE_ROOT / "logs"
BATCHES_DIR = Path("c:/iiwii_db/y-it_agents/directives/batches")

# Projects output
PROJECTS_ROOT = Path("c:/iiwii_db/y-it_agents/05_PROJECTS")

# Browser automation
CHROME_PROFILE = Path.home() / ".gemini_forge_profile"
GEMINI_URL = "https://gemini.google.com/"
DEFAULT_DELAY = 10  # seconds between requests
MAX_RETRIES = 3
GENERATION_TIMEOUT = 60  # seconds to wait for image

# Quality thresholds
MIN_DPI = 300
MIN_DIMENSION = 1024

# Ollama
OLLAMA_MODEL = "llama3.2-vision"
OLLAMA_HOST = "http://localhost:11434"

# Variants
DEFAULT_VARIANTS = 3
VARIANT_SUFFIXES = ["Version A - Standard", "Version B - Dynamic", "Version C - Stylized"]
```

---

## INTEGRATION WITH ANTIGRAVITY

The system operates as a "wrapper" that Antigravity can drive:

### 1. PROMPT GENERATION (Antigravity → Batches)

```python
# Antigravity analyzes manuscript and generates:
batch = {
    "book": "y_it_aaa",
    "chapter": "ch01",
    "images": [
        {"id": "img01", "prompt": "...", "type": "SCENE"},
        {"id": "img02", "prompt": "...", "type": "CHARACTER"},
    ]
}
# Writes to: forge/batches/{book}_{chapter}_batch.yaml
```

### 2. EXECUTION TRIGGER (User runs manually)

```bash
python forge_miner.py --batch y_it_aaa_ch01_batch.yaml
# Let it grind overnight (100+ images)
```

### 3. REVIEW CYCLE (User via UI)

```bash
streamlit run forge_review.py
# User clicks through, approves/rejects
```

### 4. FINALIZATION (Antigravity updates manuscript)

```python
# Antigravity reads manifest from reviewed/
# Updates manuscript markdown with image paths
# Triggers forge_finalize.py if needed
```

---

## DEPENDENCIES

```
selenium>=4.0.0
streamlit>=1.20.0
Pillow>=9.0.0
PyYAML>=6.0
webdriver-manager>=3.8.0  # Auto-download ChromeDriver
ollama>=0.1.0  # Optional: local AI client
```

**Install**:

```bash
pip install selenium streamlit Pillow PyYAML webdriver-manager ollama
```

---

## EXECUTION CHECKLIST

1. [ ] Create directory structure
2. [ ] Write `config.py`
3. [ ] Write `utils/file_router.py`
4. [ ] Write `forge_miner.py`
5. [ ] Write `forge_review.py`
6. [ ] Write `forge_audit.py`
7. [ ] Write `forge_finalize.py`
8. [ ] Write `utils/ollama_client.py` (optional)
9. [ ] Test with `posibot_pilot_batch.yaml`
10. [ ] Document learnings

---

## SUCCESS CRITERIA

1. ✅ User can run `forge_miner.py` and see Chrome automate Gemini
2. ✅ Images download to `staging/` with correct naming
3. ✅ User can run `forge_review.py` and see visual grid
4. ✅ Approve/Reject moves files correctly
5. ✅ DPI audit correctly flags low-quality images
6. ✅ Finalization produces book-ready directory structure
7. ✅ 100+ prompt batch completes without manual intervention

---

*Specification Version: 1.0*
*Author: Antigravity (Google DeepMind)*
*Date: 2026-01-16*

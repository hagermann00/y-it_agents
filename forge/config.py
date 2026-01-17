"""
GEMINI FORGE - Configuration
All constants, paths, and settings for the Forge system.
"""
from pathlib import Path

# ============================================================================
# PATHS
# ============================================================================

# Forge root directory
FORGE_ROOT = Path("c:/iiwii_db/y-it_agents/forge")

# Subdirectories
STAGING_DIR = FORGE_ROOT / "staging"
REVIEWED_DIR = FORGE_ROOT / "reviewed"
FINAL_DIR = FORGE_ROOT / "final"
REJECTED_DIR = FORGE_ROOT / "rejected"
LOGS_DIR = FORGE_ROOT / "logs"
UTILS_DIR = FORGE_ROOT / "utils"

# Batch definitions location
BATCHES_DIR = Path("c:/iiwii_db/y-it_agents/directives/batches")

# Projects output (for finalized assets)
PROJECTS_ROOT = Path("c:/iiwii_db/y-it_agents/05_PROJECTS")

# ============================================================================
# BROWSER AUTOMATION
# ============================================================================

# Chrome profile for persistent login
CHROME_PROFILE_DIR = Path.home() / ".gemini_forge_profile"

# Target URL
GEMINI_URL = "https://gemini.google.com/"

# Timing (seconds)
DEFAULT_DELAY = 10          # Between requests (rate limit buffer)
GENERATION_TIMEOUT = 60     # Max wait for image to generate
PAGE_LOAD_TIMEOUT = 30      # Max wait for page load
POLL_INTERVAL = 2           # How often to check for completion

# Retry logic
MAX_RETRIES = 3

# DOM Selectors (update if Gemini UI changes)
SELECTORS = {
    "input_field": [
        "textarea[placeholder*='Enter']",
        "div[contenteditable='true']",
        "textarea.ql-editor",
        "rich-textarea textarea",
    ],
    "submit_button": [
        "button[aria-label*='Send']",
        "button.send-button",
        "button[data-test-id='send-button']",
        "mat-icon[aria-label*='Send']",
    ],
    "image_result": [
        "img.generated-image",
        "div.image-container img",
        "img[alt*='Generated']",
        "div[role='img'] img",
    ],
    "loading_indicator": [
        "div.loading",
        "span.generating",
        "mat-spinner",
        "[aria-busy='true']",
    ],
    "new_chat_button": [
        "button[aria-label*='New chat']",
        "a[href*='new']",
    ],
}

# ============================================================================
# QUALITY THRESHOLDS
# ============================================================================

MIN_DPI = 300               # Minimum for print (KDP requirement)
MIN_DIMENSION = 1024        # Minimum width/height in pixels
TARGET_DPI = 300            # What we aim for

# ============================================================================
# VARIANTS
# ============================================================================

DEFAULT_VARIANTS = 3

# Suffixes appended to prompts for variation
VARIANT_SUFFIXES = [
    "",  # Original prompt as-is
    " Style variation: more dynamic lighting and perspective.",
    " Style variation: flat vector sticker art with bold outlines.",
]

# Alternative: seed-based variants (if Gemini supports)
VARIANT_SEEDS = ["A", "B", "C"]

# ============================================================================
# OLLAMA (LOCAL AI BACKUP)
# ============================================================================

OLLAMA_ENABLED = True
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2-vision"

# ============================================================================
# FILE NAMING
# ============================================================================

# Template: {book}_{chapter}_{id}_v{variant}_{timestamp}.png
FILENAME_TEMPLATE = "{book}_{chapter}_{id}_v{variant}_{timestamp}.png"

# Final naming: {chapter}_{sequence:02d}_{description}.png
FINAL_FILENAME_TEMPLATE = "{chapter}_{sequence:02d}_{description}.png"

# ============================================================================
# LOGGING
# ============================================================================

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "forge.log"
MANIFEST_FILE = LOGS_DIR / "manifest.json"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def ensure_directories():
    """Create all required directories if they don't exist."""
    for directory in [STAGING_DIR, REVIEWED_DIR, FINAL_DIR, REJECTED_DIR, LOGS_DIR, UTILS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    return True

def get_project_assets_dir(project_name: str, chapter: str = None) -> Path:
    """Get the assets directory for a project/chapter."""
    base = PROJECTS_ROOT / project_name / "ASSETS"
    if chapter:
        return base / chapter
    return base

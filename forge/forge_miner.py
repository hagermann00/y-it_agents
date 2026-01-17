"""
GEMINI FORGE - Browser Miner
Automates Chrome browser to generate images via Gemini.
"""
import argparse
import json
import logging
import time
import urllib.request
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

import yaml

# Selenium imports
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("WARNING: Selenium not installed. Run: pip install selenium webdriver-manager")

try:
    from webdriver_manager.chrome import ChromeDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False

# Local imports
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    STAGING_DIR, LOGS_DIR, BATCHES_DIR, GEMINI_URL,
    DEFAULT_DELAY, GENERATION_TIMEOUT, MAX_RETRIES,
    SELECTORS, VARIANT_SUFFIXES, DEFAULT_VARIANTS,
    CHROME_PROFILE_DIR, ensure_directories
)
from utils.file_router import generate_staging_filename


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging():
    """Configure logging to file and console."""
    ensure_directories()
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOGS_DIR / "miner.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("forge_miner")


logger = setup_logging()


# ============================================================================
# MANIFEST MANAGEMENT
# ============================================================================

def load_manifest() -> Dict:
    """Load or create the manifest file."""
    manifest_path = LOGS_DIR / "manifest.json"
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            return json.load(f)
    return {"runs": [], "images": {}}


def save_manifest(manifest: Dict):
    """Save the manifest file."""
    manifest_path = LOGS_DIR / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)


def add_to_manifest(manifest: Dict, image_info: Dict):
    """Add an image record to the manifest."""
    key = f"{image_info['book']}_{image_info['chapter']}_{image_info['id']}_v{image_info['variant']}"
    manifest["images"][key] = {
        **image_info,
        "generated_at": datetime.now().isoformat(),
    }
    save_manifest(manifest)


# ============================================================================
# BATCH PARSING
# ============================================================================

def load_batch(batch_path: Path) -> Dict:
    """Load and validate a YAML batch file."""
    with open(batch_path, 'r') as f:
        batch = yaml.safe_load(f)
    
    required_keys = ["book", "chapter", "images"]
    for key in required_keys:
        if key not in batch:
            raise ValueError(f"Batch file missing required key: {key}")
    
    return batch


def expand_variants(batch: Dict, num_variants: int) -> List[Dict]:
    """
    Expand batch images into individual prompts with variants.
    
    Returns list of dicts with: book, chapter, id, variant, prompt, type, etc.
    """
    expanded = []
    
    for image in batch["images"]:
        for variant_num in range(1, num_variants + 1):
            # Apply variant suffix to prompt
            base_prompt = image["prompt"]
            if variant_num <= len(VARIANT_SUFFIXES):
                suffix = VARIANT_SUFFIXES[variant_num - 1]
            else:
                suffix = f" Variation {variant_num}."
            
            full_prompt = base_prompt + suffix
            
            expanded.append({
                "book": batch["book"],
                "chapter": batch["chapter"],
                "id": image["id"],
                "variant": variant_num,
                "prompt": full_prompt,
                "type": image.get("type", "SCENE"),
                "placement": image.get("placement", "inline"),
                "caption": image.get("caption", ""),
            })
    
    return expanded


# ============================================================================
# BROWSER AUTOMATION
# ============================================================================

def create_driver(headless: bool = False, profile_dir: Path = None) -> webdriver.Chrome:
    """Create and configure a Chrome WebDriver instance."""
    if not SELENIUM_AVAILABLE:
        raise RuntimeError("Selenium is not installed")
    
    options = Options()
    
    # Use persistent profile for login
    if profile_dir:
        profile_dir.mkdir(parents=True, exist_ok=True)
        options.add_argument(f"--user-data-dir={profile_dir}")
    
    if headless:
        options.add_argument("--headless=new")
    
    # Common options
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Disable automation flags to avoid detection
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Create driver
    if WEBDRIVER_MANAGER_AVAILABLE:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    
    # Additional stealth
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    
    return driver


def find_element_flexible(driver, selector_list: List[str], timeout: int = 10):
    """Try multiple selectors until one works."""
    for selector in selector_list:
        try:
            element = WebDriverWait(driver, timeout / len(selector_list)).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element
        except TimeoutException:
            continue
    
    raise NoSuchElementException(f"Could not find element with any selector: {selector_list}")


def wait_for_generation(driver, timeout: int = GENERATION_TIMEOUT) -> bool:
    """
    Wait for Gemini to finish generating an image.
    Returns True if image found, False if timeout.
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        # Check for loading indicators (should disappear)
        try:
            for selector in SELECTORS["loading_indicator"]:
                loading = driver.find_elements(By.CSS_SELECTOR, selector)
                if loading:
                    time.sleep(2)
                    continue
        except:
            pass
        
        # Check for image result
        try:
            for selector in SELECTORS["image_result"]:
                images = driver.find_elements(By.CSS_SELECTOR, selector)
                if images:
                    return True
        except:
            pass
        
        time.sleep(2)
    
    return False


def download_image(url: str, save_path: Path) -> bool:
    """Download an image from URL to local path."""
    try:
        urllib.request.urlretrieve(url, save_path)
        return True
    except Exception as e:
        logger.error(f"Failed to download image: {e}")
        return False


def save_screenshot(driver, name: str):
    """Save a screenshot for debugging."""
    errors_dir = LOGS_DIR / "errors"
    errors_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = errors_dir / f"{name}_{timestamp}.png"
    driver.save_screenshot(str(screenshot_path))
    logger.info(f"Screenshot saved: {screenshot_path}")


def generate_single_image(
    driver,
    prompt_data: Dict,
    delay: int = DEFAULT_DELAY
) -> Optional[Path]:
    """
    Generate a single image via Gemini.
    
    Returns path to downloaded image, or None on failure.
    """
    prompt = prompt_data["prompt"]
    
    logger.info(f"Generating: {prompt_data['id']} v{prompt_data['variant']}")
    logger.debug(f"Prompt: {prompt[:100]}...")
    
    try:
        # Navigate to Gemini (or new chat)
        driver.get(GEMINI_URL)
        time.sleep(3)
        
        # Find and fill input
        input_field = find_element_flexible(driver, SELECTORS["input_field"])
        input_field.clear()
        input_field.send_keys(prompt)
        time.sleep(1)
        
        # Submit
        try:
            submit_btn = find_element_flexible(driver, SELECTORS["submit_button"], timeout=5)
            submit_btn.click()
        except:
            # Try Enter key as fallback
            input_field.send_keys(Keys.RETURN)
        
        # Wait for generation
        if not wait_for_generation(driver):
            logger.warning(f"Timeout waiting for image: {prompt_data['id']}")
            save_screenshot(driver, f"timeout_{prompt_data['id']}")
            return None
        
        # Find and download image
        time.sleep(2)  # Extra wait for image to fully load
        
        for selector in SELECTORS["image_result"]:
            images = driver.find_elements(By.CSS_SELECTOR, selector)
            if images:
                img_element = images[-1]  # Take the most recent image
                img_url = img_element.get_attribute("src")
                
                if img_url:
                    # Generate filename
                    filename = generate_staging_filename(
                        prompt_data["book"],
                        prompt_data["chapter"],
                        prompt_data["id"],
                        prompt_data["variant"]
                    )
                    save_path = STAGING_DIR / filename
                    
                    # Download
                    if download_image(img_url, save_path):
                        logger.info(f"Saved: {save_path}")
                        return save_path
        
        logger.warning(f"Could not extract image URL: {prompt_data['id']}")
        save_screenshot(driver, f"no_url_{prompt_data['id']}")
        return None
        
    except Exception as e:
        logger.error(f"Error generating {prompt_data['id']}: {e}")
        save_screenshot(driver, f"error_{prompt_data['id']}")
        return None
    
    finally:
        # Rate limit delay
        time.sleep(delay)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_batch(
    batch_path: Path,
    num_variants: int = DEFAULT_VARIANTS,
    delay: int = DEFAULT_DELAY,
    headless: bool = False,
    resume: bool = False
):
    """
    Execute a full batch of image generations.
    """
    logger.info(f"Starting batch: {batch_path}")
    logger.info(f"Variants: {num_variants}, Delay: {delay}s, Headless: {headless}")
    
    # Load batch
    batch = load_batch(batch_path)
    expanded = expand_variants(batch, num_variants)
    
    logger.info(f"Total prompts to generate: {len(expanded)}")
    
    # Load manifest for resume capability
    manifest = load_manifest()
    
    # Filter out already completed if resuming
    if resume:
        completed_keys = set(manifest.get("images", {}).keys())
        expanded = [
            p for p in expanded
            if f"{p['book']}_{p['chapter']}_{p['id']}_v{p['variant']}" not in completed_keys
        ]
        logger.info(f"Resuming: {len(expanded)} remaining")
    
    if not expanded:
        logger.info("Nothing to generate!")
        return
    
    # Create browser
    driver = create_driver(headless=headless, profile_dir=CHROME_PROFILE_DIR)
    
    try:
        # Record run start
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        manifest["runs"].append({
            "id": run_id,
            "batch": str(batch_path),
            "started_at": datetime.now().isoformat(),
            "total_prompts": len(expanded),
        })
        save_manifest(manifest)
        
        # Process each prompt
        success_count = 0
        fail_count = 0
        
        for i, prompt_data in enumerate(expanded):
            logger.info(f"Progress: {i+1}/{len(expanded)}")
            
            # Try with retries
            for attempt in range(MAX_RETRIES):
                result_path = generate_single_image(driver, prompt_data, delay)
                
                if result_path:
                    # Record success
                    add_to_manifest(manifest, {
                        **prompt_data,
                        "status": "success",
                        "path": str(result_path),
                    })
                    success_count += 1
                    break
                else:
                    logger.warning(f"Attempt {attempt + 1} failed for {prompt_data['id']}")
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(delay * 2)  # Extra delay before retry
            else:
                # All retries failed
                add_to_manifest(manifest, {
                    **prompt_data,
                    "status": "failed",
                    "path": None,
                })
                fail_count += 1
        
        # Record run completion
        for run in manifest["runs"]:
            if run["id"] == run_id:
                run["completed_at"] = datetime.now().isoformat()
                run["success_count"] = success_count
                run["fail_count"] = fail_count
                break
        save_manifest(manifest)
        
        logger.info(f"Batch complete: {success_count} success, {fail_count} failed")
        
    finally:
        driver.quit()


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Gemini Forge - Browser Miner")
    parser.add_argument("--batch", required=True, help="Path to YAML batch file")
    parser.add_argument("--variants", type=int, default=DEFAULT_VARIANTS, help="Variants per prompt")
    parser.add_argument("--delay", type=int, default=DEFAULT_DELAY, help="Seconds between requests")
    parser.add_argument("--headless", action="store_true", help="Run Chrome in headless mode")
    parser.add_argument("--resume", action="store_true", help="Resume from last checkpoint")
    
    args = parser.parse_args()
    
    # Resolve batch path
    batch_path = Path(args.batch)
    if not batch_path.exists():
        # Try in batches directory
        batch_path = BATCHES_DIR / args.batch
    
    if not batch_path.exists():
        print(f"Batch file not found: {args.batch}")
        return 1
    
    # Ensure directories exist
    ensure_directories()
    
    # Run batch
    run_batch(
        batch_path,
        num_variants=args.variants,
        delay=args.delay,
        headless=args.headless,
        resume=args.resume
    )
    
    return 0


if __name__ == "__main__":
    exit(main())

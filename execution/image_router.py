"""
Y-IT Image Generation Router
Generates images via Gemini Ultra (Imagen 3 / Nano Banana) and routes to typed folders.

Usage:
    python image_router.py --batch .tmp/image_prompts.csv
    python image_router.py --prompt "..." --type POSIBOT --book dropshipping
    python image_router.py --batch .tmp/image_prompts.csv --dry-run

Requires:
    pip install google-generativeai pillow python-dotenv
"""

import os
import csv
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import google.generativeai as genai

# === CONFIGURATION ===

VALID_TYPES = ['COVER', 'POSIBOT', 'CHAD', 'CHAPTER', 'COMIC', 'DIAGRAM']

# Model defaults by type
MODEL_DEFAULTS = {
    'COVER': 'imagen-3.0-generate-002',
    'POSIBOT': 'imagen-3.0-generate-002',  # Switch to nano_banana when available
    'CHAD': 'imagen-3.0-generate-002',
    'CHAPTER': 'imagen-3.0-generate-002',
    'COMIC': 'imagen-3.0-generate-002',
    'DIAGRAM': 'imagen-3.0-generate-002',
}

# Output path templates
OUTPUT_PATHS = {
    'COVER': 'outputs/covers/{book_slug}/',
    'POSIBOT': 'outputs/assets/posibot/',
    'CHAD': 'outputs/assets/chad/stage-{stage}/',
    'CHAPTER': 'outputs/assets/chapters/{book_slug}/',
    'COMIC': 'outputs/assets/comics/{book_slug}/',
    'DIAGRAM': 'outputs/assets/diagrams/',
}

# Filename templates
FILENAME_TEMPLATES = {
    'COVER': '{book_slug}_cover_{n}.png',
    'POSIBOT': 'posibot_{book_slug}_{n}.png',
    'CHAD': 'chad_s{stage}_{book_slug}_{n}.png',
    'CHAPTER': 'ch{n}_{book_slug}.png',
    'COMIC': 'comic_{book_slug}_{n}.png',
    'DIAGRAM': 'diagram_{book_slug}_{n}.png',
}

BASE_DIR = Path(__file__).parent.parent
OUTPUTS_DIR = BASE_DIR / 'outputs'
TMP_DIR = BASE_DIR / '.tmp'


def setup_genai():
    """Initialize Gemini API client."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment or .env file")
    genai.configure(api_key=api_key)


def get_output_path(img_type: str, book_slug: str, stage: str = None) -> Path:
    """Get the output directory for a given image type."""
    path_template = OUTPUT_PATHS.get(img_type)
    if not path_template:
        raise ValueError(f"Unknown image type: {img_type}")
    
    path = path_template.format(book_slug=book_slug, stage=stage or '0')
    return BASE_DIR / path


def get_next_filename(output_dir: Path, img_type: str, book_slug: str, stage: str = None) -> str:
    """Generate next sequential filename."""
    template = FILENAME_TEMPLATES.get(img_type)
    
    # Find existing files to get next number
    output_dir.mkdir(parents=True, exist_ok=True)
    existing = list(output_dir.glob(f'*{book_slug}*.png'))
    n = len(existing) + 1
    
    return template.format(book_slug=book_slug, stage=stage or '0', n=n)


def generate_image(prompt: str, model_name: str) -> bytes:
    """Generate image using Gemini Imagen API."""
    # Using Imagen 3 via Gemini API
    imagen = genai.ImageGenerationModel(model_name)
    
    result = imagen.generate_images(
        prompt=prompt,
        number_of_images=1,
        safety_filter_level="block_only_high",
        person_generation="allow_adult",
        aspect_ratio="1:1",  # Default, can be parameterized
    )
    
    if result.images:
        return result.images[0]._pil_image
    else:
        raise Exception("No image generated")


def process_single(prompt: str, img_type: str, book_slug: str, 
                   stage: str = None, model: str = None, dry_run: bool = False) -> dict:
    """Process a single image generation request."""
    
    img_type = img_type.upper()
    if img_type not in VALID_TYPES:
        return {'success': False, 'error': f'Invalid type: {img_type}'}
    
    model_name = model or MODEL_DEFAULTS.get(img_type)
    output_dir = get_output_path(img_type, book_slug, stage)
    filename = get_next_filename(output_dir, img_type, book_slug, stage)
    output_path = output_dir / filename
    
    result = {
        'prompt': prompt[:100] + '...' if len(prompt) > 100 else prompt,
        'type': img_type,
        'book_slug': book_slug,
        'stage': stage,
        'model': model_name,
        'output_path': str(output_path),
        'timestamp': datetime.now().isoformat(),
    }
    
    if dry_run:
        result['success'] = True
        result['dry_run'] = True
        print(f"[DRY RUN] Would generate: {output_path}")
        return result
    
    try:
        print(f"Generating: {img_type} for {book_slug}...")
        image = generate_image(prompt, model_name)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        image.save(output_path, 'PNG')
        
        result['success'] = True
        print(f"  ✓ Saved: {output_path}")
        
    except Exception as e:
        result['success'] = False
        result['error'] = str(e)
        print(f"  ✗ Error: {e}")
    
    return result


def process_batch(csv_path: str, dry_run: bool = False) -> list:
    """Process a batch of prompts from CSV."""
    results = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            prompt = row.get('prompt', '').strip()
            img_type = row.get('type', '').strip()
            book_slug = row.get('book_slug', '').strip()
            stage = row.get('stage', '').strip() or None
            model = row.get('model', '').strip() or None
            
            if not prompt or not img_type or not book_slug:
                results.append({
                    'success': False,
                    'error': 'Missing required fields',
                    'row': row
                })
                continue
            
            result = process_single(prompt, img_type, book_slug, stage, model, dry_run)
            results.append(result)
    
    return results


def save_log(results: list, log_type: str = 'log'):
    """Save results to log CSV."""
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_path = TMP_DIR / f'image_generation_{log_type}_{timestamp}.csv'
    
    if not results:
        return
    
    fieldnames = list(results[0].keys())
    
    with open(log_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\nLog saved: {log_path}")


def main():
    parser = argparse.ArgumentParser(description='Y-IT Image Generation Router')
    parser.add_argument('--batch', type=str, help='Path to CSV file with prompts')
    parser.add_argument('--prompt', type=str, help='Single prompt text')
    parser.add_argument('--type', type=str, choices=VALID_TYPES, help='Image type')
    parser.add_argument('--book', type=str, help='Book slug')
    parser.add_argument('--stage', type=str, help='Stage number (for CHAD type)')
    parser.add_argument('--model', type=str, help='Model override')
    parser.add_argument('--dry-run', action='store_true', help='Preview without generating')
    
    args = parser.parse_args()
    
    if not args.dry_run:
        setup_genai()
    
    if args.batch:
        results = process_batch(args.batch, args.dry_run)
        
        successes = [r for r in results if r.get('success')]
        failures = [r for r in results if not r.get('success')]
        
        print(f"\n=== BATCH COMPLETE ===")
        print(f"Success: {len(successes)}")
        print(f"Failed: {len(failures)}")
        
        if successes:
            save_log(successes, 'log')
        if failures:
            save_log(failures, 'errors')
            
    elif args.prompt and args.type and args.book:
        result = process_single(
            args.prompt, args.type, args.book, 
            args.stage, args.model, args.dry_run
        )
        
        if result.get('success'):
            print(f"\n✓ Generated: {result.get('output_path')}")
        else:
            print(f"\n✗ Failed: {result.get('error')}")
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python image_router.py --batch .tmp/image_prompts.csv")
        print("  python image_router.py --prompt 'PosiBot with money' --type POSIBOT --book dropshipping")


if __name__ == '__main__':
    main()

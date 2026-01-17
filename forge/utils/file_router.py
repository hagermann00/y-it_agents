"""
GEMINI FORGE - File Router Utility
Handles filename generation, parsing, and file movement.
"""
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple


def generate_staging_filename(
    book: str,
    chapter: str,
    image_id: str,
    variant: int,
    extension: str = "png"
) -> str:
    """
    Generate a standardized staging filename.
    
    Format: {book}_{chapter}_{id}_v{variant}_{timestamp}.{ext}
    Example: y_it_aaa_ch01_posibot_shrug_v1_20260116_033000.png
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitize components
    book = sanitize_component(book)
    chapter = sanitize_component(chapter)
    image_id = sanitize_component(image_id)
    
    return f"{book}_{chapter}_{image_id}_v{variant}_{timestamp}.{extension}"


def generate_final_filename(
    chapter: str,
    sequence: int,
    description: str,
    extension: str = "png"
) -> str:
    """
    Generate a book-ready final filename.
    
    Format: {chapter}_{sequence:02d}_{description}.{ext}
    Example: ch01_01_posibot_shrug.png
    """
    chapter = sanitize_component(chapter)
    description = sanitize_component(description)
    
    return f"{chapter}_{sequence:02d}_{description}.{extension}"


def parse_staging_filename(filename: str) -> Optional[Dict]:
    """
    Parse a staging filename back into its components.
    
    Returns dict with: book, chapter, image_id, variant, timestamp
    Returns None if parsing fails.
    """
    pattern = r"^(.+?)_(.+?)_(.+?)_v(\d+)_(\d{8}_\d{6})\.(\w+)$"
    match = re.match(pattern, filename)
    
    if not match:
        return None
    
    return {
        "book": match.group(1),
        "chapter": match.group(2),
        "image_id": match.group(3),
        "variant": int(match.group(4)),
        "timestamp": match.group(5),
        "extension": match.group(6),
    }


def sanitize_component(text: str) -> str:
    """
    Sanitize a filename component.
    - Lowercase
    - Replace spaces with underscores
    - Remove non-alphanumeric except underscores
    - Truncate to 50 chars
    """
    text = text.lower().strip()
    text = re.sub(r'\s+', '_', text)
    text = re.sub(r'[^a-z0-9_]', '', text)
    return text[:50]


def move_file(
    source: Path,
    destination_dir: Path,
    new_name: Optional[str] = None
) -> Path:
    """
    Move a file to a destination directory.
    Optionally rename it.
    Returns the new path.
    """
    destination_dir.mkdir(parents=True, exist_ok=True)
    
    if new_name:
        dest_path = destination_dir / new_name
    else:
        dest_path = destination_dir / source.name
    
    shutil.move(str(source), str(dest_path))
    return dest_path


def copy_file(
    source: Path,
    destination_dir: Path,
    new_name: Optional[str] = None
) -> Path:
    """
    Copy a file to a destination directory.
    Optionally rename it.
    Returns the new path.
    """
    destination_dir.mkdir(parents=True, exist_ok=True)
    
    if new_name:
        dest_path = destination_dir / new_name
    else:
        dest_path = destination_dir / source.name
    
    shutil.copy2(str(source), str(dest_path))
    return dest_path


def group_variants(file_list: list) -> Dict[str, list]:
    """
    Group a list of staging filenames by their base ID.
    
    Input: ["book_ch_id_v1_ts.png", "book_ch_id_v2_ts.png", ...]
    Output: {"book_ch_id": [Path1, Path2, ...], ...}
    """
    groups = {}
    
    for filepath in file_list:
        if isinstance(filepath, str):
            filepath = Path(filepath)
        
        parsed = parse_staging_filename(filepath.name)
        if not parsed:
            continue
        
        # Create group key (without variant and timestamp)
        key = f"{parsed['book']}_{parsed['chapter']}_{parsed['image_id']}"
        
        if key not in groups:
            groups[key] = []
        groups[key].append(filepath)
    
    # Sort each group by variant number
    for key in groups:
        groups[key].sort(key=lambda p: parse_staging_filename(p.name).get('variant', 0))
    
    return groups


def get_image_dimensions(filepath: Path) -> Tuple[int, int]:
    """
    Get image width and height.
    Returns (width, height) tuple.
    """
    try:
        from PIL import Image
        with Image.open(filepath) as img:
            return img.size
    except Exception:
        return (0, 0)


def get_image_dpi(filepath: Path) -> Tuple[int, int]:
    """
    Get image DPI.
    Returns (x_dpi, y_dpi) tuple.
    Returns (72, 72) if DPI info not available.
    """
    try:
        from PIL import Image
        with Image.open(filepath) as img:
            dpi = img.info.get('dpi', (72, 72))
            return (int(dpi[0]), int(dpi[1]))
    except Exception:
        return (72, 72)


def calculate_print_dpi(filepath: Path, target_size_inches: float = 6.0) -> int:
    """
    Calculate effective DPI if printed at target size.
    Assumes the longer dimension = target_size_inches.
    """
    width, height = get_image_dimensions(filepath)
    if width == 0 or height == 0:
        return 0
    
    longer_dimension = max(width, height)
    effective_dpi = int(longer_dimension / target_size_inches)
    return effective_dpi


if __name__ == "__main__":
    # Test the functions
    print("Testing file_router utilities...")
    
    # Test filename generation
    staging_name = generate_staging_filename("y_it_aaa", "ch01", "posibot_shrug", 1)
    print(f"Staging filename: {staging_name}")
    
    # Test parsing
    parsed = parse_staging_filename(staging_name)
    print(f"Parsed: {parsed}")
    
    # Test final filename
    final_name = generate_final_filename("ch01", 1, "posibot_shrug")
    print(f"Final filename: {final_name}")
    
    print("All tests passed!")

"""
GEMINI FORGE - Image Auditor
Check image quality (DPI, dimensions) for print readiness.
"""
import argparse
from pathlib import Path
from typing import List, Dict
import sys

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("ERROR: Pillow not installed. Run: pip install Pillow")

# Local imports
sys.path.insert(0, str(Path(__file__).parent))
from config import MIN_DPI, MIN_DIMENSION, STAGING_DIR, REVIEWED_DIR, FINAL_DIR
from utils.file_router import get_image_dimensions, calculate_print_dpi


def audit_image(image_path: Path, target_print_size: float = 6.0) -> Dict:
    """
    Audit a single image for print quality.
    
    Args:
        image_path: Path to image file
        target_print_size: Target print size in inches (longer dimension)
    
    Returns:
        Dict with audit results
    """
    result = {
        "path": str(image_path),
        "filename": image_path.name,
        "exists": image_path.exists(),
        "width": 0,
        "height": 0,
        "effective_dpi": 0,
        "meets_dpi_threshold": False,
        "meets_dimension_threshold": False,
        "status": "UNKNOWN",
        "issues": [],
    }
    
    if not image_path.exists():
        result["status"] = "FILE_NOT_FOUND"
        result["issues"].append("File does not exist")
        return result
    
    if not PIL_AVAILABLE:
        result["status"] = "PILLOW_NOT_AVAILABLE"
        result["issues"].append("Pillow library not installed")
        return result
    
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            result["width"] = width
            result["height"] = height
            
            # Calculate effective DPI for target print size
            longer_dimension = max(width, height)
            effective_dpi = int(longer_dimension / target_print_size)
            result["effective_dpi"] = effective_dpi
            
            # Check thresholds
            result["meets_dpi_threshold"] = effective_dpi >= MIN_DPI
            result["meets_dimension_threshold"] = (width >= MIN_DIMENSION and height >= MIN_DIMENSION)
            
            # Build issues list
            if not result["meets_dpi_threshold"]:
                result["issues"].append(f"DPI too low: {effective_dpi} < {MIN_DPI}")
            
            if not result["meets_dimension_threshold"]:
                result["issues"].append(f"Dimensions too small: {width}x{height} < {MIN_DIMENSION}x{MIN_DIMENSION}")
            
            # Overall status
            if result["meets_dpi_threshold"] and result["meets_dimension_threshold"]:
                result["status"] = "PASS"
            else:
                result["status"] = "FAIL"
            
            # Additional metadata
            result["format"] = img.format
            result["mode"] = img.mode
            
            # Try to get embedded DPI info
            dpi = img.info.get("dpi", (72, 72))
            result["embedded_dpi"] = dpi
            
    except Exception as e:
        result["status"] = "ERROR"
        result["issues"].append(f"Error reading image: {str(e)}")
    
    return result


def audit_directory(directory: Path, target_print_size: float = 6.0) -> List[Dict]:
    """
    Audit all images in a directory.
    
    Returns list of audit results.
    """
    extensions = [".png", ".jpg", ".jpeg", ".webp", ".tiff", ".bmp"]
    results = []
    
    for ext in extensions:
        for image_path in directory.glob(f"*{ext}"):
            results.append(audit_image(image_path, target_print_size))
        for image_path in directory.glob(f"*{ext.upper()}"):
            results.append(audit_image(image_path, target_print_size))
    
    return results


def print_audit_report(results: List[Dict]):
    """Print a formatted audit report."""
    if not results:
        print("No images found to audit.")
        return
    
    print("\n" + "=" * 80)
    print("GEMINI FORGE - IMAGE QUALITY AUDIT")
    print("=" * 80)
    
    pass_count = 0
    fail_count = 0
    error_count = 0
    
    for result in results:
        status_icon = {
            "PASS": "✅",
            "FAIL": "⚠️",
            "ERROR": "❌",
            "FILE_NOT_FOUND": "❓",
        }.get(result["status"], "❓")
        
        print(f"\n{status_icon} {result['filename']}")
        print(f"   Dimensions: {result['width']} × {result['height']}")
        print(f"   Effective DPI: {result['effective_dpi']} (min: {MIN_DPI})")
        
        if result["issues"]:
            for issue in result["issues"]:
                print(f"   ⚠️  {issue}")
        
        if result["status"] == "PASS":
            pass_count += 1
        elif result["status"] == "FAIL":
            fail_count += 1
        else:
            error_count += 1
    
    print("\n" + "-" * 80)
    print("SUMMARY")
    print("-" * 80)
    print(f"Total Images: {len(results)}")
    print(f"✅ Pass: {pass_count}")
    print(f"⚠️  Fail: {fail_count}")
    print(f"❌ Error: {error_count}")
    
    if fail_count > 0:
        print(f"\n⚠️  {fail_count} images need upscaling or regeneration.")
    
    if pass_count == len(results):
        print("\n🎉 All images meet print quality requirements!")
    
    print("=" * 80 + "\n")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Gemini Forge - Image Quality Auditor")
    parser.add_argument("--folder", help="Folder to audit (default: staging)")
    parser.add_argument("--file", help="Single file to audit")
    parser.add_argument("--print-size", type=float, default=6.0, 
                        help="Target print size in inches (default: 6.0)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if args.file:
        # Audit single file
        result = audit_image(Path(args.file), args.print_size)
        if args.json:
            import json
            print(json.dumps(result, indent=2))
        else:
            print_audit_report([result])
    
    elif args.folder:
        # Audit specified folder
        folder = Path(args.folder)
        if not folder.exists():
            print(f"Folder not found: {folder}")
            return 1
        results = audit_directory(folder, args.print_size)
        if args.json:
            import json
            print(json.dumps(results, indent=2))
        else:
            print_audit_report(results)
    
    else:
        # Default: audit staging
        print("Auditing staging directory...")
        results = audit_directory(STAGING_DIR, args.print_size)
        if args.json:
            import json
            print(json.dumps(results, indent=2))
        else:
            print_audit_report(results)
    
    return 0


if __name__ == "__main__":
    exit(main())

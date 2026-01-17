"""
GEMINI FORGE - Asset Finalizer
Move reviewed assets to book-ready locations with final naming.
"""
import argparse
import json
import shutil
from pathlib import Path
from typing import Dict, List
from datetime import datetime


# Local imports
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    REVIEWED_DIR, FINAL_DIR, PROJECTS_ROOT, LOGS_DIR,
    ensure_directories, get_project_assets_dir
)
from utils.file_router import (
    parse_staging_filename, generate_final_filename, 
    move_file, copy_file
)


def load_finalization_manifest(project: str) -> Dict:
    """Load or create a finalization manifest for a project."""
    manifest_path = LOGS_DIR / f"finalize_{project}.json"
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            return json.load(f)
    return {"project": project, "finalized": [], "sequence_counter": {}}


def save_finalization_manifest(project: str, manifest: Dict):
    """Save the finalization manifest."""
    manifest_path = LOGS_DIR / f"finalize_{project}.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)


def get_next_sequence(manifest: Dict, chapter: str) -> int:
    """Get the next sequence number for a chapter."""
    if chapter not in manifest["sequence_counter"]:
        manifest["sequence_counter"][chapter] = 0
    manifest["sequence_counter"][chapter] += 1
    return manifest["sequence_counter"][chapter]


def find_reviewed_images(project: str, chapter: str = None) -> List[Path]:
    """
    Find reviewed images matching project/chapter.
    
    If chapter is None, returns all images for the project.
    """
    images = []
    extensions = [".png", ".jpg", ".jpeg", ".webp"]
    
    for ext in extensions:
        for img in REVIEWED_DIR.glob(f"*{ext}"):
            parsed = parse_staging_filename(img.name)
            if not parsed:
                continue
            
            if parsed.get("book") == project:
                if chapter is None or parsed.get("chapter") == chapter:
                    images.append(img)
    
    return sorted(images)


def finalize_image(
    image_path: Path,
    project: str,
    manifest: Dict,
    dry_run: bool = False,
    copy_mode: bool = False
) -> Dict:
    """
    Finalize a single image.
    
    Returns dict with source, destination, and status.
    """
    parsed = parse_staging_filename(image_path.name)
    if not parsed:
        return {
            "source": str(image_path),
            "destination": None,
            "status": "PARSE_FAILED",
            "error": "Could not parse filename"
        }
    
    chapter = parsed.get("chapter", "unknown")
    image_id = parsed.get("image_id", "unknown")
    
    # Get destination directory
    dest_dir = get_project_assets_dir(project, chapter)
    
    # Get sequence number
    sequence = get_next_sequence(manifest, chapter)
    
    # Generate final filename
    final_name = generate_final_filename(chapter, sequence, image_id)
    final_path = dest_dir / final_name
    
    if dry_run:
        return {
            "source": str(image_path),
            "destination": str(final_path),
            "status": "DRY_RUN",
        }
    
    # Ensure destination exists
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Move or copy
    try:
        if copy_mode:
            copy_file(image_path, dest_dir, final_name)
        else:
            move_file(image_path, dest_dir, final_name)
        
        # Record in manifest
        manifest["finalized"].append({
            "source": str(image_path),
            "destination": str(final_path),
            "chapter": chapter,
            "sequence": sequence,
            "finalized_at": datetime.now().isoformat(),
        })
        
        return {
            "source": str(image_path),
            "destination": str(final_path),
            "status": "SUCCESS",
        }
        
    except Exception as e:
        return {
            "source": str(image_path),
            "destination": str(final_path),
            "status": "ERROR",
            "error": str(e),
        }


def finalize_project(
    project: str,
    chapter: str = None,
    dry_run: bool = False,
    copy_mode: bool = False
) -> List[Dict]:
    """
    Finalize all reviewed images for a project.
    
    Returns list of finalization results.
    """
    ensure_directories()
    
    images = find_reviewed_images(project, chapter)
    
    if not images:
        print(f"No reviewed images found for project: {project}" + 
              (f" chapter: {chapter}" if chapter else ""))
        return []
    
    manifest = load_finalization_manifest(project)
    results = []
    
    for img in images:
        result = finalize_image(img, project, manifest, dry_run, copy_mode)
        results.append(result)
        
        status_icon = {
            "SUCCESS": "✅",
            "DRY_RUN": "🔍",
            "ERROR": "❌",
            "PARSE_FAILED": "⚠️",
        }.get(result["status"], "❓")
        
        print(f"{status_icon} {result['source']} → {result.get('destination', 'N/A')}")
    
    if not dry_run:
        save_finalization_manifest(project, manifest)
    
    return results


def generate_manifest_md(project: str) -> str:
    """
    Generate a Markdown manifest of finalized assets.
    
    This can be used to insert image references into manuscripts.
    """
    manifest = load_finalization_manifest(project)
    
    lines = [
        f"# Asset Manifest: {project}",
        f"",
        f"Generated: {datetime.now().isoformat()}",
        f"",
        f"## Images",
        f"",
    ]
    
    # Group by chapter
    by_chapter = {}
    for item in manifest.get("finalized", []):
        chapter = item.get("chapter", "unknown")
        if chapter not in by_chapter:
            by_chapter[chapter] = []
        by_chapter[chapter].append(item)
    
    for chapter in sorted(by_chapter.keys()):
        lines.append(f"### {chapter}")
        lines.append("")
        
        for item in by_chapter[chapter]:
            dest = Path(item.get("destination", ""))
            lines.append(f"- `{dest.name}` - Finalized: {item.get('finalized_at', '')[:10]}")
            lines.append(f"  - Source: `{Path(item.get('source', '')).name}`")
        
        lines.append("")
    
    return "\n".join(lines)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Gemini Forge - Asset Finalizer")
    parser.add_argument("--project", required=True, help="Project name (e.g., y_it_aaa)")
    parser.add_argument("--chapter", help="Chapter to finalize (e.g., ch01), or all if not specified")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without doing it")
    parser.add_argument("--copy", action="store_true", help="Copy instead of move")
    parser.add_argument("--manifest", action="store_true", help="Generate Markdown manifest only")
    
    args = parser.parse_args()
    
    ensure_directories()
    
    if args.manifest:
        # Just generate manifest
        md = generate_manifest_md(args.project)
        print(md)
        return 0
    
    print(f"{'DRY RUN: ' if args.dry_run else ''}Finalizing {args.project}" +
          (f" chapter {args.chapter}" if args.chapter else " (all chapters)"))
    print("-" * 60)
    
    results = finalize_project(
        args.project,
        args.chapter,
        dry_run=args.dry_run,
        copy_mode=args.copy
    )
    
    print("-" * 60)
    success = sum(1 for r in results if r["status"] in ["SUCCESS", "DRY_RUN"])
    failed = sum(1 for r in results if r["status"] not in ["SUCCESS", "DRY_RUN"])
    print(f"Total: {len(results)} | Success: {success} | Failed: {failed}")
    
    return 0


if __name__ == "__main__":
    exit(main())

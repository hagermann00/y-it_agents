"""
GEMINI FORGE - Review Dashboard
Streamlit-based UI for visual selection of generated images.
"""
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

try:
    import streamlit as st
    from PIL import Image
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    print("ERROR: Streamlit not installed. Run: pip install streamlit Pillow")
    exit(1)

# Local imports
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    STAGING_DIR, REVIEWED_DIR, REJECTED_DIR, LOGS_DIR, FINAL_DIR,
    MIN_DPI, MIN_DIMENSION, ensure_directories
)
from utils.file_router import (
    parse_staging_filename, group_variants, 
    get_image_dimensions, calculate_print_dpi, move_file
)


# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Gemini Forge - Review",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# STATE MANAGEMENT
# ============================================================================

def load_manifest() -> Dict:
    """Load the manifest file."""
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


def get_staging_images() -> List[Path]:
    """Get all images in staging directory."""
    ensure_directories()
    extensions = [".png", ".jpg", ".jpeg", ".webp"]
    images = []
    for ext in extensions:
        images.extend(STAGING_DIR.glob(f"*{ext}"))
    return sorted(images)


def get_reviewed_images() -> List[Path]:
    """Get all images in reviewed directory."""
    extensions = [".png", ".jpg", ".jpeg", ".webp"]
    images = []
    for ext in extensions:
        images.extend(REVIEWED_DIR.glob(f"*{ext}"))
    return sorted(images)


def move_to_reviewed(image_path: Path) -> Path:
    """Move an image to the reviewed directory."""
    return move_file(image_path, REVIEWED_DIR)


def move_to_rejected(image_path: Path) -> Path:
    """Move an image to the rejected directory."""
    return move_file(image_path, REJECTED_DIR)


def get_image_info(image_path: Path) -> Dict:
    """Get metadata about an image."""
    width, height = get_image_dimensions(image_path)
    effective_dpi = calculate_print_dpi(image_path)
    parsed = parse_staging_filename(image_path.name)
    
    return {
        "path": image_path,
        "filename": image_path.name,
        "width": width,
        "height": height,
        "effective_dpi": effective_dpi,
        "meets_threshold": effective_dpi >= MIN_DPI,
        "parsed": parsed,
    }


# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_sidebar():
    """Render the sidebar with stats and controls."""
    st.sidebar.title("🔥 Gemini Forge")
    st.sidebar.markdown("---")
    
    # Stats
    staging = get_staging_images()
    reviewed = get_reviewed_images()
    
    st.sidebar.metric("📥 Staging", len(staging))
    st.sidebar.metric("✅ Reviewed", len(reviewed))
    
    # Progress
    total = len(staging) + len(reviewed)
    if total > 0:
        progress = len(reviewed) / total
        st.sidebar.progress(progress, text=f"{int(progress * 100)}% Complete")
    
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "View",
        ["Review Staging", "View Reviewed", "Batch Stats"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Bulk actions
    st.sidebar.subheader("Bulk Actions")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Approve All", use_container_width=True):
            for img in staging:
                move_to_reviewed(img)
            st.rerun()
    
    with col2:
        if st.button("Reject All", use_container_width=True, type="secondary"):
            for img in staging:
                move_to_rejected(img)
            st.rerun()
    
    return page


def render_image_card(image_info: Dict, show_actions: bool = True):
    """Render a single image card with metadata and actions."""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display image
        try:
            img = Image.open(image_info["path"])
            st.image(img, use_container_width=True)
        except Exception as e:
            st.error(f"Could not load image: {e}")
    
    with col2:
        # Metadata
        st.markdown(f"**Filename:** `{image_info['filename']}`")
        st.markdown(f"**Dimensions:** {image_info['width']} × {image_info['height']}")
        
        # DPI status
        if image_info["meets_threshold"]:
            st.success(f"✅ DPI: {image_info['effective_dpi']}")
        else:
            st.warning(f"⚠️ DPI: {image_info['effective_dpi']} (Below {MIN_DPI})")
        
        # Parsed info
        if image_info["parsed"]:
            st.markdown(f"**Book:** {image_info['parsed'].get('book', 'N/A')}")
            st.markdown(f"**Chapter:** {image_info['parsed'].get('chapter', 'N/A')}")
            st.markdown(f"**ID:** {image_info['parsed'].get('image_id', 'N/A')}")
            st.markdown(f"**Variant:** {image_info['parsed'].get('variant', 'N/A')}")
        
        # Actions
        if show_actions:
            st.markdown("---")
            action_col1, action_col2 = st.columns(2)
            
            with action_col1:
                if st.button("✅ Approve", key=f"approve_{image_info['filename']}", use_container_width=True):
                    move_to_reviewed(image_info["path"])
                    st.rerun()
            
            with action_col2:
                if st.button("❌ Reject", key=f"reject_{image_info['filename']}", use_container_width=True, type="secondary"):
                    move_to_rejected(image_info["path"])
                    st.rerun()


def render_variant_group(group_key: str, images: List[Path]):
    """Render a group of variant images side-by-side."""
    st.subheader(f"📦 {group_key}")
    
    # Get prompt from manifest if available
    manifest = load_manifest()
    for img in images:
        parsed = parse_staging_filename(img.name)
        if parsed:
            key = f"{parsed['book']}_{parsed['chapter']}_{parsed['image_id']}_v{parsed['variant']}"
            if key in manifest.get("images", {}):
                prompt = manifest["images"][key].get("prompt", "")
                if prompt:
                    st.caption(f"Prompt: {prompt[:200]}...")
                    break
    
    # Create columns for variants
    cols = st.columns(len(images))
    
    for col, img_path in zip(cols, images):
        with col:
            info = get_image_info(img_path)
            
            # Image
            try:
                img = Image.open(img_path)
                st.image(img, use_container_width=True)
            except:
                st.error("Failed to load")
            
            # Quick stats
            dpi_color = "green" if info["meets_threshold"] else "orange"
            st.markdown(f":{dpi_color}[DPI: {info['effective_dpi']}]")
            st.caption(f"Variant {info['parsed'].get('variant', '?') if info['parsed'] else '?'}")
            
            # Actions
            if st.button("✅ Approve", key=f"g_approve_{img_path.name}", use_container_width=True):
                move_to_reviewed(img_path)
                st.rerun()
            
            if st.button("❌ Reject", key=f"g_reject_{img_path.name}", use_container_width=True, type="secondary"):
                move_to_rejected(img_path)
                st.rerun()
    
    st.markdown("---")


def render_staging_review():
    """Render the staging review page."""
    st.title("📥 Review Staging")
    
    images = get_staging_images()
    
    if not images:
        st.info("No images in staging. Run the miner to generate some!")
        return
    
    # Group by base ID for variant comparison
    groups = group_variants(images)
    
    # View toggle
    view_mode = st.radio(
        "View Mode",
        ["Grouped (Variants Side-by-Side)", "Individual"],
        horizontal=True
    )
    
    if view_mode == "Grouped (Variants Side-by-Side)":
        for group_key, group_images in groups.items():
            render_variant_group(group_key, group_images)
    else:
        # Individual view
        for img in images:
            info = get_image_info(img)
            with st.expander(f"📷 {img.name}", expanded=False):
                render_image_card(info)


def render_reviewed_gallery():
    """Render the reviewed images gallery."""
    st.title("✅ Reviewed Images")
    
    images = get_reviewed_images()
    
    if not images:
        st.info("No reviewed images yet. Approve some from staging!")
        return
    
    # Grid display
    cols_per_row = 4
    for i in range(0, len(images), cols_per_row):
        row_images = images[i:i + cols_per_row]
        cols = st.columns(cols_per_row)
        
        for col, img_path in zip(cols, row_images):
            with col:
                try:
                    img = Image.open(img_path)
                    st.image(img, use_container_width=True)
                    st.caption(img_path.name[:30] + "...")
                except:
                    st.error("Failed")


def render_batch_stats():
    """Render batch statistics."""
    st.title("📊 Batch Statistics")
    
    manifest = load_manifest()
    
    if not manifest.get("runs"):
        st.info("No batch runs recorded yet.")
        return
    
    # Runs table
    st.subheader("Batch Runs")
    runs_data = []
    for run in manifest.get("runs", []):
        runs_data.append({
            "ID": run.get("id", ""),
            "Batch": Path(run.get("batch", "")).name,
            "Started": run.get("started_at", "")[:19],
            "Completed": run.get("completed_at", "")[:19] if run.get("completed_at") else "In Progress",
            "Success": run.get("success_count", 0),
            "Failed": run.get("fail_count", 0),
        })
    
    st.dataframe(runs_data, use_container_width=True)
    
    # Image stats
    st.subheader("Image Statistics")
    images = manifest.get("images", {})
    success_count = sum(1 for v in images.values() if v.get("status") == "success")
    fail_count = sum(1 for v in images.values() if v.get("status") == "failed")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Generated", len(images))
    col2.metric("Successful", success_count)
    col3.metric("Failed", fail_count)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point."""
    ensure_directories()
    
    page = render_sidebar()
    
    if page == "Review Staging":
        render_staging_review()
    elif page == "View Reviewed":
        render_reviewed_gallery()
    elif page == "Batch Stats":
        render_batch_stats()


if __name__ == "__main__":
    main()

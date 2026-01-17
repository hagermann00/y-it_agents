# GEMINI FORGE - Image Generation Pipeline
"""
A local-first image generation pipeline that wraps browser-based Gemini Ultra
for industrial-scale book asset production.

## Quick Start

1. Generate batch file (YAML)
2. Run miner: python forge_miner.py --batch your_batch.yaml
3. Review: streamlit run forge_review.py
4. Finalize: python forge_finalize.py --project your_project

## Components

- forge_miner.py   - Browser automation for Gemini
- forge_review.py  - Streamlit UI for selection
- forge_audit.py   - DPI/quality checker
- forge_finalize.py - Book-ready asset preparation

See FORGE_SPEC.md for full documentation.
"""
from config import ensure_directories

# Ensure directories exist on import
ensure_directories()

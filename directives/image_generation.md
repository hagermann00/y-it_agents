# Image Generation & Routing

## Purpose
Generate Y-IT visual assets from prompts via Gemini Ultra and route to correct folders by type.

## Prerequisites
- Gemini Ultra subscription (active)
- `.env` file with `GEMINI_API_KEY`
- Prompt source file in `.tmp/`

## Input Formats

### Option 1: CSV (batch)
```
.tmp/image_prompts.csv
```
Columns: `prompt,type,book_slug,stage,model`

| Column | Required | Values |
|--------|----------|--------|
| prompt | Yes | Full image prompt text |
| type | Yes | COVER, POSIBOT, CHAD, CHAPTER, COMIC, DIAGRAM |
| book_slug | Yes | e.g., `dropshipping`, `mlm`, `crypto` |
| stage | No | 1-8 (for CHAD type only) |
| model | No | `imagen3` (default), `nano_banana` |

### Option 2: Single prompt (interactive)
Pass directly to script via CLI argument.

## Routing Rules

| Type | Destination | Naming |
|------|-------------|--------|
| COVER | `outputs/covers/{book_slug}/` | `{book_slug}_cover_{n}.png` |
| POSIBOT | `outputs/assets/posibot/` | `posibot_{book_slug}_{n}.png` |
| CHAD | `outputs/assets/chad/stage-{stage}/` | `chad_s{stage}_{book_slug}_{n}.png` |
| CHAPTER | `outputs/assets/chapters/{book_slug}/` | `ch{n}_{book_slug}.png` |
| COMIC | `outputs/assets/comics/{book_slug}/` | `comic_{book_slug}_{n}.png` |
| DIAGRAM | `outputs/assets/diagrams/` | `diagram_{book_slug}_{n}.png` |

## Model Selection

| Model | Use Case | Style |
|-------|----------|-------|
| `imagen3` | Production covers, professional assets | Photorealistic, polished |
| `nano_banana` | PosiBot, Chad, stylized illustrations | Artistic, distinctive |

**Default routing:**
- COVER → imagen3
- POSIBOT, CHAD, COMIC → nano_banana
- CHAPTER, DIAGRAM → imagen3

## Execution

### Batch mode
```bash
python execution/image_router.py --batch .tmp/image_prompts.csv
```

### Single prompt
```bash
python execution/image_router.py --prompt "PosiBot holding money bag" --type POSIBOT --book dropshipping
```

### Dry run (no API calls)
```bash
python execution/image_router.py --batch .tmp/image_prompts.csv --dry-run
```

## Output
- Generated images in routed folders under `outputs/`
- Log file: `.tmp/image_generation_log.csv`
- Failed prompts: `.tmp/image_generation_errors.csv`

## Error Handling
- Rate limit hit → Wait and retry (3 attempts)
- Invalid prompt → Log to errors, continue batch
- API error → Log full response, continue batch

## Learnings
<!-- Updated by agent as issues are discovered -->
- [placeholder for API quirks]
- [placeholder for prompt patterns that work well]

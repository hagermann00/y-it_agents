# Directive: Image Batch Booking

> Generate 40-80 images per "booking" via browser automation on Gemini/NotebookLM.

## Overview

A **booking** = 40 images × 2 passes = 80 total images for one children's book project.

## Inputs

| Input | Description | Example |
|-------|-------------|---------|
| `projectName` | Short identifier | `nanoBananaPro` |
| `promptTemplate` | Base prompt for generation | See prompt library |
| `variationCount` | Images per pass | 40 |
| `passCount` | Number of passes | 2 |

## Workflow

```
1. Navigate to target site (gemini.google.com)
2. For each pass (1 to passCount):
   a. For each variation (1 to variationCount):
      - Submit prompt (with variation seed if applicable)
      - Wait for image generation complete
      - Export image with naming: {projectName}_{pass}_{variation:03d}.png
      - Wait for cooldown (rate limit buffer)
3. Consolidate all images into outputs/{projectName}/
4. Generate manifest.json with metadata
```

## Naming Convention

```
{projectName}_{pass}_{sequence:03d}.png

Examples:
nanoBananaPro_1_001.png
nanoBananaPro_1_002.png
...
nanoBananaPro_1_040.png
nanoBananaPro_2_001.png
...
nanoBananaPro_2_040.png
```

## Output Structure

```
outputs/
└── nanoBananaPro/
    ├── manifest.json
    ├── pass_1/
    │   ├── nanoBananaPro_1_001.png
    │   └── ...
    └── pass_2/
        ├── nanoBananaPro_2_001.png
        └── ...
```

## Execution Tools

| Tool | Purpose |
|------|---------|
| `yit-gemini.user.js` | Tampermonkey userscript for Gemini automation |
| Browser Agent | Orchestration and navigation |

## Edge Cases

- **Rate limit hit**: Pause 60s, retry 3x, then notify user
- **Generation stall**: Wait max 30s, refresh, retry
- **Download fail**: Log to `.tmp/errors.log`, continue sequence
- **Session timeout**: Re-authenticate via browser agent

## Learnings

_(Updated as we discover issues)_

---

## Related

- `CONSTRAINTS.md` — No API calls, browser-first
- `execution/` — Will contain userscript once built

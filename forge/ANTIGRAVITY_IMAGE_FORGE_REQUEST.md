# REQUEST: Antigravity Image Forge Extension

## What I Need

An extension to the **Antigravity agent system** that enables batch image generation. The backend is **Gemini Ultra (browser version)** — Antigravity orchestrates the prompts, drives the browser, and manages the output.

This is NOT a standalone Gemini tool. It's an **Antigravity capability** that happens to use Gemini Web as its image generation engine.

---

## The Problem I'm Solving

I need to generate **hundreds of images** for book illustrations. Doing this manually in the browser is painfully slow:

1. Type prompt
2. Wait for generation
3. Download image
4. Rename it properly
5. Repeat 300+ times

I want to automate steps 1-4 and add a smart review step before finalization.

---

## My Hard Constraints

### 1. ZERO API COSTS

- I have a **Gemini Ultra subscription** (browser-based, unlimited generations)
- I will NOT pay for API calls
- The solution MUST work through the browser interface at `gemini.google.com`

### 2. 100% LOCAL

- Nothing cloud-hosted
- All files stay on my Windows machine
- I don't want to set up servers or databases

### 3. BATCH INPUT

- I want to define prompts in a simple file format (YAML, JSON, CSV - you decide)
- Each prompt should generate **3 variations** automatically
- The system should handle 100+ prompts per batch

### 4. VISUAL REVIEW

- I need to SEE the generated images before approving them
- Side-by-side comparison of variants preferred
- One-click approve/reject
- Show me the image dimensions and effective DPI

### 5. ORGANIZED OUTPUT

- Approved images go to a "final" folder
- Proper naming: `{chapter}_{sequence}_{description}.png`
- Some kind of manifest/log so I know what was generated

### 6. PRINT QUALITY

- Target: **300 DPI** at 6 inches (longer dimension)
- Flag images that don't meet threshold
- Optional: ability to upscale or regenerate

---

## Critical: 3-Image Prompt Syntax

Gemini browser supports generating **multiple images in a single prompt**. This is essential for efficiency.

### The Syntax That Works

```
Generate three pictures:

1. [First variation description - 1-2 sentences]

2. [Second variation description - 1-2 sentences]

3. [Third variation description - 1-2 sentences]
```

### Real Example

```
Generate three pictures:

1. PosiBot (gold robot with cyan screen) doing a confused shrug, arms up, palms open. Precise cartoon style, white background.

2. Same character (PosiBot) doing a confident thumbs-up, slight spark from joints. Precise cartoon style, white background.

3. Same character (PosiBot) slumped over, defeated pose, oil tears leaking. Precise cartoon style, white background.
```

### Key Rules

- Start with **"Generate three pictures:"** explicitly
- **Number each image (1, 2, 3)** with its own description
- Keep each description to **1-2 sentences** for consistency
- Use **"Same character"** phrasing to maintain consistency across variants
- Gemini returns all 3 images in **one response**

### Why This Matters

- **3x fewer requests** = faster batch completion
- **Less rate-limit risk** = can grind more images per session
- **Built-in variants** = each prompt produces 3 options to choose from

The wrapper should convert each "image concept" in the batch file into this multi-image prompt format automatically.

---

## Nice to Have (Not Required)

- Resume capability if the batch is interrupted
- Local AI (Ollama/Llama) to analyze image quality
- Integration with my existing file structure at `c:\iiwii_db\y-it_agents\`

---

## What I Already Have

- Windows 11
- Chrome with Gemini Ultra login
- Python 3.x installed
- Ollama with `llama3.2-vision` model (optional use)
- Existing project structure at `c:\iiwii_db\y-it_agents\05_PROJECTS\`

---

## What Success Looks Like

1. I write a batch file with 100 prompts
2. I run a command and walk away
3. Chrome opens, generates all 300 images (100 prompts × 3 variants)
4. I come back and open a review interface
5. I click through, approving winners
6. Approved images land in my book project folder, properly named
7. I can audit DPI to ensure print readiness

---

## Deliverable

Build me a working system. You decide the architecture, tools, and implementation. Just make it work within my constraints.

---

*Author: brihag8*
*Date: 2026-01-16*

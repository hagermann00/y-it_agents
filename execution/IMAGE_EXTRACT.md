# IMAGE EXTRACTION PROMPT

> Paste Sonnet output here. Extracts [IMAGE] blocks into extension-ready YAML.

---

## PROMPT

Extract all `[IMAGE]...[/IMAGE]` blocks from the following chapter draft.

For each image, output in this YAML format:

```yaml
book: [BOOK_SLUG]
chapter: [CHAPTER_NUMBER]
images:
  - id: [from block]
    type: [from block]
    prompt: |
      [Convert description to Gemini image generation prompt. Be specific about:
      - Visual composition and layout
      - Art style (infographic, cartoon, diagram, etc.)
      - Color palette (match Y-IT brand: dark modes, sharp contrasts)
      - Text to include (if any)
      - Mood/tone]
    placement: [from block]
    caption: "[from block]"
```

### STYLE GUIDE FOR PROMPTS

| Image Type | Style Direction |
|------------|-----------------|
| DIAGRAM | Clean infographic, dark background, accent colors, minimal text |
| COMIC | Satirical cartoon, 2-4 panels, expressive characters, speech bubbles |
| CHAPTER_HEADER | Bold typography, thematic imagery, book cover aesthetic |
| SCREENSHOT | Realistic mockup, UI elements, fake but believable |

### OUTPUT

Output ONLY the YAML batch file. No commentary. This goes directly to the extension.

---

## CHAPTER DRAFT

```
[Paste full Sonnet output here]
```

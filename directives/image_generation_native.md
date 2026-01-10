# Y-IT Image Generation - Antigravity Native

## CONSTRAINTS (READ FIRST)

### DO NOT
- ❌ Write Python scripts that call external APIs
- ❌ Use `google-generativeai` or any SDK
- ❌ Create `.env` files or manage API keys
- ❌ Build automation that runs outside Antigravity
- ❌ Suggest "I'll write a script for this"

### DO USE
- ✅ Antigravity's built-in browser agent
- ✅ Gemini web UI (gemini.google.com) directly
- ✅ NotebookLM web UI (notebooklm.google.com) directly
- ✅ File system for organizing outputs
- ✅ Your built-in screenshot/artifact capabilities

---

## THE APPROACH

We're using Antigravity as a **browser automation layer** that:
1. Opens Gemini web interface
2. Pastes image prompts
3. Downloads generated images
4. Renames and routes them to correct folders
5. Logs what was generated

This uses YOUR browser control + Gemini Ultra subscription (already authenticated in browser).

---

## NOTEBOOK STRUCTURE (NotebookLM)

When pulling research context, query these notebooks via Gemini web "Add notebook" feature:

| Notebook Name | Content Type |
|---------------|--------------|
| `Y-IT_DROPSHIPPING_MASTER` | Production specs, chapter structure, character arcs, voice guide |
| `Y-IT_DROP_RESEARCH` | Guru claims, Reddit failures, platform policies, cost docs |
| `Y-IT_DROP_SEO_GEO` | Keywords, Amazon categories, comp titles, BISAC codes |
| `Y-IT_DROP_AFFILIATE` | Commission structures, platform terms, link strategies |
| `Y-IT_DROP_CASESTUDIES` | Real failures, lawsuits, FTC complaints, refund data |

---

## IMAGE GENERATION WORKFLOW

### Step 1: Read prompt list
Open and read: `.tmp/image_prompts.md` (or CSV if present)

### Step 2: For each prompt
1. Open browser to gemini.google.com
2. If image generation prompt:
   - Paste the prompt
   - Wait for image generation
   - Download the result
3. Rename file according to routing rules (below)
4. Move to correct output folder

### Step 3: Log results
Create/update `.tmp/generation_log.md` with:
- Timestamp
- Prompt used
- Output path
- Success/failure

---

## ROUTING RULES

Based on prompt PREFIX or explicit type marker:

| Marker | Destination Folder | Filename Pattern |
|--------|-------------------|------------------|
| `[COVER]` | `outputs/covers/{book}/` | `{book}_cover_{n}.png` |
| `[POSIBOT]` | `outputs/assets/posibot/` | `posibot_{book}_{n}.png` |
| `[CHAD-{stage}]` | `outputs/assets/chad/stage-{stage}/` | `chad_s{stage}_{book}_{n}.png` |
| `[CHAPTER]` | `outputs/assets/chapters/{book}/` | `ch_{book}_{n}.png` |
| `[COMIC]` | `outputs/assets/comics/{book}/` | `comic_{book}_{n}.png` |
| `[DIAGRAM]` | `outputs/assets/diagrams/` | `diagram_{book}_{n}.png` |

---

## PROMPT FORMAT

Prompts in `.tmp/image_prompts.md` should look like:

```markdown
## Dropshipping Book

[COVER] dropshipping
A smartphone screen showing a Shopify dashboard with red declining graphs, surrounded by cardboard boxes gathering dust, photorealistic style

[POSIBOT] dropshipping  
PosiBot mascot character, cute robot with glowing green eyes and a forced smile, holding a thumbs up sign that says 'YOU GOT THIS!', clean illustration style

[CHAD-1] dropshipping
Chad character stage 1: confident young man in designer clothes, standing in front of a Lamborghini, holding phone showing 'passive income'

[CHAD-3] dropshipping
Chad character stage 3: same man now slightly disheveled, surrounded by unsold inventory boxes, checking phone nervously

[CHAD-5] dropshipping
Chad character stage 5: defeated posture, sitting among boxes in garage, calculator showing losses, empty energy drink cans

[CHAD-8] dropshipping
Chad character stage 8: back in office cubicle but wiser, small genuine smile, photo of family on desk, modest but stable

[DIAGRAM] dropshipping
Flowchart: dropshipping money flow from customer through fees, supplier costs, shipping, returns - showing how $100 sale becomes $3 profit
```

---

## EXECUTION MODE

Set Antigravity to **Agent-assisted** or **Agent-driven** mode.

When ready, tell the agent:

> "Read the image prompts from `.tmp/image_prompts.md`. For each prompt, use the browser to open Gemini, generate the image, download it, rename it according to the routing rules in the directive, and save to the correct output folder. Log each result."

Then let it run.

---

## EXPECTED OUTPUT

```
outputs/
├── covers/
│   └── dropshipping/
│       └── dropshipping_cover_1.png
├── assets/
│   ├── posibot/
│   │   └── posibot_dropshipping_1.png
│   └── chad/
│       ├── stage-1/
│       │   └── chad_s1_dropshipping_1.png
│       ├── stage-3/
│       ├── stage-5/
│       └── stage-8/
├── chapters/
├── comics/
└── diagrams/
    └── diagram_dropshipping_1.png
```

---

## SELF-ANNEALING NOTES

When you discover issues, update this section:

### Learnings
- [ ] Gemini image gen URL/flow may change - update if UI shifts
- [ ] Download location varies by browser settings - may need to move from Downloads
- [ ] Rate limits on image gen - note cooldown patterns here

### Failures Encountered
<!-- Agent updates this as issues occur -->


# Y-IT Quick Flow Card

## The Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  1. SONNET_PROMPT.md                                        │
│     → Paste into Antigravity (Claude Sonnet)                │
│     → Get: Chapter prose + [IMAGE] markers                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  2. IMAGE_EXTRACT_PROMPT.md                                 │
│     → Paste Sonnet output                                   │
│     → Get: Generation-ready image prompts                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  3. EXTENSION HANDOFF                                       │
│     → Feed extracted prompts to image gen extension         │
│     → Extension uses Gemini browser UI                      │
│     → Get: Generated images in routed folders               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  4. PROOF_ASSEMBLE_PROMPT.md                                │
│     → Combine prose + image manifest                        │
│     → Human reviews assembled draft                         │
│     → Get: Final proofed chapter                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  5. Y-IT MACHINE (23 Formats)                               │
│     → See production_pipeline.md for format list            │
│     → Outputs all distribution formats                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  6. SUBMIT                                                  │
│     → KDP, IngramSpark, Gumroad, etc.                       │
└─────────────────────────────────────────────────────────────┘
```

## File Locations

| File | Purpose |
|------|---------|
| `.tmp/SONNET_PROMPT.md` | Paste to Sonnet for prose gen |
| `.tmp/IMAGE_EXTRACT_PROMPT.md` | Extract image prompts from prose |
| `.tmp/PROOF_ASSEMBLE_PROMPT.md` | Final assembly + QC |
| `directives/production_pipeline.md` | Full pipeline reference + 23 formats |
| `directives/image_generation_native.md` | Routing rules for images |

## Per-Chapter Workflow

1. Open Antigravity, select Claude Sonnet
2. Paste `SONNET_PROMPT.md`, fill in chapter brief + research
3. Copy output → paste into `IMAGE_EXTRACT_PROMPT.md`
4. Hand extracted prompts to image extension
5. Wait for images to generate
6. Paste prose + image manifest into `PROOF_ASSEMBLE_PROMPT.md`
7. Review assembled chapter
8. Approve → goes to 23-format output
9. Submit checklist → publish

## Time Estimate Per Chapter

| Step | Time |
|------|------|
| Sonnet prose | 2-3 min |
| Image extraction | 1 min |
| Image generation | 5-10 min (async) |
| Assembly | 2 min |
| Human proof | 10-15 min |
| **Total** | **~25 min/chapter** |

8 chapters = ~3-4 hours to first draft with images


# SONNET PROSE GENERATION PROMPT

> Paste this into Antigravity with Claude Sonnet selected. Fill in the bracketed sections.

---

## PROMPT

You are generating Chapter [CHAPTER_NUMBER] of a Y-IT satirical exposé book on **[TOPIC]**.

### VOICE

Forensic satire at 80% intensity. Think "financial autopsy meets dark comedy." You're the friend who lost money on this and is now warning others with gallows humor.

### STRUCTURE

Follow the Universal Chapter Outline for this chapter's phase:
- **CH1-2 (Phase 1)**: Mockumentary, deadpan, NO DATA
- **CH3-5 (Phase 2)**: Full Y-IT voice, DATA SLEDGEHAMMER
- **CH6-8 (Phase 3)**: Measured, constructive, EXIT RAMPS

### CHARACTER INTEGRATION

- **PosiBot**: Appears in sidebars with toxic positivity `[POSIBOT SIDEBAR: "..."]`
- **Chad**: Reference his journey per arc stage for this chapter

### IMAGE MARKERS

When you need a visual, insert:

```
[IMAGE]
id: ch{X}_img{N}
type: DIAGRAM | COMIC | CHAPTER_HEADER | SCREENSHOT
description: Detailed description of what the image should show
style: Clean infographic style, satirical cartoon, etc.
placement: inline | sidebar | full-page
caption: "Caption text"
[/IMAGE]
```

### OUTPUT

Full chapter prose with [IMAGE] markers embedded. Include:
- Minimum 1 sidebar per 3 pages (Reality Check / Guru Quote / Meanwhile...)
- 2-3 punchlines per page
- PosiBot appearances per chapter spec
- Source citations where applicable

---

## CHAPTER CONTEXT

**Chapter Number**: [X]
**Chapter Title**: [TITLE]
**Phase**: [1/2/3]
**Theme**: [FROM OUTLINE]
**Page Target**: [X-Y]
**Data Required**: [YES/NO + specifics]

### Chapter Brief
```
[Paste chapter requirements from Y-IT_UNIVERSAL_CHAPTER_OUTLINE_v2.1.md]
```

### Research Context
```
[Paste NotebookLM synthesis or research notes here]
```

---

## BEGIN CHAPTER:

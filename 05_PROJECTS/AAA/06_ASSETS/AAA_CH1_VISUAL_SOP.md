# Standard Operating Procedure: Generating Visual Assets for "The AI Body Count" - Chapter 1

## Document Objective

This document provides a comprehensive, step-by-step workflow for generating and managing all required visual assets for Chapter 1 of the book, "The AI Body Count." It synthesizes the project's visual identity, character bibles, and technical generation protocols into a single source of truth for production.

---

## 1.0 The Strategic Foundation: Core Assets & Visual Identity

### Chapter 1 Narrative Core

The manuscript for "Chapter 1: The AI Gold Rush" introduces the central promise of the "AI Automation Agency" (AAA) model—a seemingly effortless path to wealth. The narrative tone is satirical and hooks the reader by juxtaposing the extreme hype of online gurus with the underlying, unspoken reality of the venture.

### Key Characters & Styles

#### PosiBot

* **Appearance**: A compact, friendly humanoid robot with a tan-colored industrial chassis. Its "face" is a circular, bright cyan digital screen that displays simple, pixel-art expressions.
* **Purpose**: PosiBot functions as the project's mascot, a slightly eerie cheerleader for the AI gold rush.
* **Core Style**: High-quality 3D Pixar-style render with soft depth of field and detailed textures.

#### Chad

* **Appearance**: A relatable, 30-year-old office worker with short dark hair and business-casual attire. Generic "everyman".
* **Purpose**: Emotional anchor and reader surrogate.
* **Core Style**: Cinematic 4K shot with dramatic key lighting.

### Master Color Palettes

| Phase/Mood | Color Palette & Hex Codes |
| :--- | :--- |
| **PHASE 1 — MOCKUMENTARY (CH1-2)** | Primary: Teal (#319795), Secondary: Coral Accent (#F56565), Background: Warm Cream (#FFFAF0) |
| **PHASE 2 — REALITY (CH3-5)** | Primary: Navy Blue (#1A365D), Secondary: Warning Red (#E53E3E), Background: Cool Gray (#EDF2F7) |
| **PHASE 3 — REDEMPTION (CH6-8)** | Primary: Slate (#4A5568), Secondary: Amber/Hope (#D69E2E), Background: Neutral (#F7FAFC) |

---

## 2.0 Chapter 1 Image Requirements Analysis

### Image Manifest

* `[IMAGE: chad-ch1-opener-excited]`
* `[IMAGE: posibot-ch1-01-right]`
* `[IMAGE: posibot-ch1-02-left]`

### High-Fidelity Prompt Formulation

(Prompts omitted here for brevity but saved in IMAGE_PROMPT_LIST.md)

---

## 3.0 The Unified Generation & Routing Workflow

* **DO NOT** use Python scripts/APIs.
* **DO USE** Antigravity's built-in browser agent on gemini.google.com.
* **Routing**:
  * `[POSIBOT]` → `outputs/assets/posibot/`
  * `[CHAD-{stage}]` → `outputs/assets/chad/stage-{stage}/`

---

## 4.0 Quality Control and Process Improvement

(Standard protocols for rate limits, stalls, and download failures)

---
*End of Visual SOP v1.0*

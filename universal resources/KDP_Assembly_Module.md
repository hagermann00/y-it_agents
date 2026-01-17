# KDP ASSEMBLY MODULE v1.0

## Final Production & Packaging Standards

This module defines the process for taking polished manuscripts and images and transforming them into a professional KDP-ready (Kindle Direct Publishing) package.

---

## 1. FILE STANDARDS

### MANUSCRIPT (PDF/DOCX)

- **Trim Size:** 6" x 9" (Standard Trade Paperback).
- **Margins:**
  - Top/Bottom: 0.75"
  - Outside: 0.5"
  - Gutter (Inside): 0.75" (Mirror margins enabled).
- **Typography:**
  - Body Text: Garamond or Sabon (11pt / 1.3 line spacing).
  - Headers: Helvetica or Montserrat (Bold).
  - Data Sidebars: Courier New or JetBrains Mono (Coded aesthetic).

### IMAGES (PNG/JPG)

- **Resolution:** 300 DPI minimum.
- **Color Profile:** CMYK (for print) / RGB (for ebook).
- **Naming:** Must match script tags: `[type]-[chapter]-[descriptor]-[position].png`.

---

## 2. ASSEMBLY WORKFLOW

### STEP 1: IMAGE INJECTION

- Scan the `Claude Polish` manuscript for `[IMAGE: tag]` locations.
- Replace tags with the corresponding high-res image from the Reservoir.
- **Rules:**
  - Technical charts must be preceded by a "Reality Check" header.
  - PosiBot images should be floated right/left of guru quotes.
  - Chad images correspond to the chapter emotional opener.

### STEP 2: DATA VERIFICATION

- Perform a final cross-reference between the formatted manuscript and the **MASTER_DATA_TABLE**.
- Ensure all bolded numbers ($) match the table exactly.

### STEP 3: FRONT/BACK MATTER INJECTION

- Inject the **Locked Title Page** (from `TITLE_CHAPTER_OPENERS` module).
- Inject **Page 2 Signature** ("PROBABLY WON'T WORK").
- Inject **Chapter Openers** with epigraphs.
- Inject **Final Body Count** signature.

### STEP 4: PDF EXPORT

- Export using "High Quality Print" settings.
- Subset all fonts.
- Include 0.125" bleed if images extend to the edge.

---

## 3. PACKAGING CHECKLIST (The "Launch" Trigger)

Before uploading to KDP, verify:

- [ ] Trim size matches 6" x 9".
- [ ] All `[IMAGE]` tags are replaced with 300DPI assets.
- [ ] ISBN is present on the copyright page.
- [ ] Table of Contents links are verified (Ebook version).
- [ ] Page numbers match the TOC.
- [ ] Total Body Count (at the end) sums all case study losses.

---

## 4. AUTOMATION SCRIPT (Concept)

*Note: In future updates, this can be handled by a Python script using `reportlab` or `pandoc` to automate the assembly of the MD files into a final PDF.*

---
*End of KDP Assembly Module v1.0*

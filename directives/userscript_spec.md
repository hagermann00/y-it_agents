# Directive: YIT Userscript Specification

> Tampermonkey userscript for browser automation on AI image generation sites.

## Target Sites

```javascript
// @match https://gemini.google.com/*
// @match https://notebooklm.google.com/*
// @match https://aistudio.google.com/*
```

## Exposed API

The userscript exposes `window.__yit` for browser agent calls:

```javascript
window.__yit = {
  // Core
  status: () => { ... },           // Returns current state
  
  // Prompting
  submitPrompt: (text) => { ... }, // Inject and submit prompt
  waitForComplete: () => { ... },  // Wait for generation done
  
  // Export
  getImages: () => { ... },        // Get all generated image URLs
  downloadImage: (url, filename) => { ... }, // Download single
  downloadAll: (prefix, startNum) => { ... }, // Batch download
  
  // Batch mode
  startBatch: (config) => { ... }, // Begin automated sequence
  pauseBatch: () => { ... },       // Pause current batch
  getBatchStatus: () => { ... },   // Progress info
}
```

## State Machine

```
IDLE → SUBMITTING → GENERATING → READY → EXPORTING → IDLE
         ↓              ↓           ↓
       ERROR ←──────────┴───────────┘
```

## Key Selectors (Gemini)

```javascript
const SELECTORS = {
  promptInput: 'div[contenteditable="true"]',
  submitButton: 'button[aria-label="Send"]',
  imageContainer: '.generated-image-container',
  downloadButton: '[aria-label="Download"]',
  loadingSpinner: '.loading-indicator',
};
```

> ⚠️ These selectors WILL break. Update in Learnings when they do.

## Download Handler

```javascript
// Files go to browser's default download location
// Browser agent then moves to proper output folder
downloadImage: async (url, filename) => {
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
}
```

## Rate Limit Buffer

```javascript
const RATE_LIMITS = {
  betweenPrompts: 3000,   // 3s between submissions
  betweenDownloads: 500,  // 0.5s between downloads
  onError: 60000,         // 60s on rate limit error
};
```

## Learnings

_(Selector changes, timing adjustments, discovered edge cases)_

---

## Installation

1. Install Tampermonkey browser extension
2. Create new userscript
3. Paste contents of `execution/yit-gemini.user.js`
4. Save and enable

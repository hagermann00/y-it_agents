# YIT Image Generator - Chrome Extension

## Installation

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select this `extension/` directory
5. Pin the extension to your toolbar

## Usage

### 1. Prepare YAML Batch

Generate a batch file using the `IMAGE_EXTRACT.md` prompt template:

```yaml
book: dropshipping
chapter: 3
images:
  - id: ch3_img1
    type: DIAGRAM
    prompt: "Flowchart showing customer pays $49.99..."
    placement: inline
    caption: "Where your money goes"
```

### 2. Open Gemini

Navigate to `https://gemini.google.com/` in Chrome.

### 3. Start Batch

1. Click the YIT extension icon
2. Paste your YAML into the text area
3. Click "Start Batch"
4. Watch progress in the popup

### 4. Collect Output

Images download to your Chrome download folder with naming:
```
outputs/{book}/ch{chapter}/{image_id}.png
```

## Files

| File | Purpose |
|------|---------|
| `manifest.json` | Extension configuration |
| `background.js` | Service worker, batch queue management |
| `content.js` | DOM automation on Gemini pages |
| `popup.html/js` | Extension popup UI |

## Troubleshooting

### Selectors broke (Google updated UI)

Edit `content.js` → `SELECTORS` object. Add new selectors to the arrays.

### Rate limiting

Increase delays in `content.js` → `CONFIG.delays`.

### Downloads not going to right folder

Chrome downloads to default location. Move manually or update Chrome download settings.

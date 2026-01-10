// YIT Image Generator - Popup Script

// ============================================================
// ELEMENTS
// ============================================================

const statusEl = document.getElementById('status');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const batchInput = document.getElementById('batchInput');
const batchYaml = document.getElementById('batchYaml');
const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');
const errorsEl = document.getElementById('errors');

// ============================================================
// STATE
// ============================================================

let isProcessing = false;

// ============================================================
// YAML PARSER (simple)
// ============================================================

function parseYaml(yamlStr) {
    // Simple YAML parser for our specific format
    // For production, use js-yaml library
    try {
        const lines = yamlStr.split('\n');
        const result = { images: [] };
        let currentImage = null;
        let inPrompt = false;
        let promptLines = [];

        for (const line of lines) {
            const trimmed = line.trim();

            if (line.startsWith('book:')) {
                result.book = trimmed.replace('book:', '').trim();
            } else if (line.startsWith('chapter:')) {
                result.chapter = parseInt(trimmed.replace('chapter:', '').trim());
            } else if (trimmed.startsWith('- id:')) {
                if (currentImage) result.images.push(currentImage);
                currentImage = { id: trimmed.replace('- id:', '').trim() };
            } else if (currentImage) {
                if (trimmed.startsWith('type:')) {
                    currentImage.type = trimmed.replace('type:', '').trim();
                } else if (trimmed.startsWith('prompt:')) {
                    const promptValue = trimmed.replace('prompt:', '').trim();
                    if (promptValue === '|') {
                        inPrompt = true;
                        promptLines = [];
                    } else {
                        currentImage.prompt = promptValue.replace(/^"/, '').replace(/"$/, '');
                    }
                } else if (inPrompt) {
                    if (trimmed.startsWith('placement:') || trimmed.startsWith('caption:')) {
                        currentImage.prompt = promptLines.join('\n').trim();
                        inPrompt = false;
                        // Parse the line that ended the prompt
                        if (trimmed.startsWith('placement:')) {
                            currentImage.placement = trimmed.replace('placement:', '').trim();
                        } else if (trimmed.startsWith('caption:')) {
                            currentImage.caption = trimmed.replace('caption:', '').trim().replace(/^"/, '').replace(/"$/, '');
                        }
                    } else {
                        promptLines.push(trimmed);
                    }
                } else if (trimmed.startsWith('placement:')) {
                    currentImage.placement = trimmed.replace('placement:', '').trim();
                } else if (trimmed.startsWith('caption:')) {
                    currentImage.caption = trimmed.replace('caption:', '').trim().replace(/^"/, '').replace(/"$/, '');
                }
            }
        }

        if (currentImage) result.images.push(currentImage);

        return result;
    } catch (e) {
        throw new Error('Invalid YAML format');
    }
}

// ============================================================
// UI UPDATES
// ============================================================

function updateUI(state) {
    isProcessing = state.isProcessing;

    // Status
    statusEl.textContent = state.isProcessing ? 'Processing' : 'Idle';
    statusEl.className = `status-value ${state.isProcessing ? 'processing' : 'idle'}`;

    // Progress
    if (state.isProcessing && state.progress) {
        progressSection.style.display = 'block';
        batchInput.style.display = 'none';
        startBtn.style.display = 'none';
        pauseBtn.style.display = 'block';

        const pct = state.progress.total > 0
            ? (state.progress.current / state.progress.total * 100)
            : 0;
        progressFill.style.width = `${pct}%`;
        progressText.textContent = `${state.progress.current} / ${state.progress.total}`;

        // Errors
        if (state.progress.errors && state.progress.errors.length > 0) {
            errorsEl.style.display = 'block';
            errorsEl.textContent = state.progress.errors
                .map(e => `#${e.index + 1}: ${e.error}`)
                .join('\n');
        }
    } else {
        progressSection.style.display = 'none';
        batchInput.style.display = 'block';
        startBtn.style.display = 'block';
        pauseBtn.style.display = 'none';
        errorsEl.style.display = 'none';
    }
}

// ============================================================
// EVENT HANDLERS
// ============================================================

startBtn.addEventListener('click', async () => {
    const yaml = batchYaml.value.trim();
    if (!yaml) {
        alert('Please paste a YAML batch file');
        return;
    }

    try {
        const batch = parseYaml(yaml);
        if (!batch.book || !batch.chapter || !batch.images.length) {
            throw new Error('Missing required fields: book, chapter, images');
        }

        chrome.runtime.sendMessage({ type: 'START_BATCH', batch });
        updateUI({ isProcessing: true, progress: { current: 0, total: batch.images.length } });
    } catch (e) {
        alert(`Parse error: ${e.message}`);
    }
});

pauseBtn.addEventListener('click', () => {
    chrome.runtime.sendMessage({ type: 'PAUSE_BATCH' });
});

// ============================================================
// INITIALIZATION
// ============================================================

// Get initial status
chrome.runtime.sendMessage({ type: 'GET_STATUS' }, updateUI);

// Poll for status updates every 2 seconds (popup doesn't receive push updates reliably)
setInterval(() => {
    chrome.runtime.sendMessage({ type: 'GET_STATUS' }, (response) => {
        if (response) updateUI(response);
    });
}, 2000);

// Listen for updates
chrome.runtime.onMessage.addListener((message) => {
    if (message.type === 'BATCH_COMPLETE') {
        updateUI({ isProcessing: false });
        alert(`Batch complete!\n\nGenerated: ${message.manifest.images.length}\nErrors: ${message.manifest.errors.length}`);
    }
});

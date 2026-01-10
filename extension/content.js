// YIT Image Generator - Content Script
// Runs on Gemini pages, handles DOM automation

// ============================================================
// CONFIGURATION
// ============================================================

const CONFIG = {
    delays: {
        afterSubmit: 500,
        pollInterval: 1000,
        maxWait: 60000,
        afterDownload: 500
    },
    retries: 3
};

// Selectors - UPDATE WHEN GOOGLE CHANGES UI
const SELECTORS = {
    promptInput: [
        'div[contenteditable="true"]',
        'rich-textarea div[contenteditable="true"]',
        'textarea',
        '[aria-label*="prompt" i]',
        '[aria-label*="message" i]',
        '[placeholder*="prompt" i]',
        '.ql-editor',
        'div[role="textbox"]',
    ],
    submitButton: [
        'button[aria-label*="Send" i]',
        'button[aria-label*="Submit" i]',
        'button[data-test-id="send-button"]',
        'button.send-button',
        'button[type="submit"]',
        'mat-icon-button',
    ],
    loadingIndicator: [
        '.loading',
        '[data-loading]',
        '.thinking',
        '.generating',
        '.response-loading',
        '[aria-busy="true"]',
        '.spinner',
    ],
    generatedImage: [
        'img[src*="blob:"]',
        'img[src*="googleusercontent"]',
        '.generated-image img',
        '.response-container img',
        'img[alt*="Generated" i]',
    ],
    errorMessage: [
        '.error-message',
        '[data-error]',
        '.generation-error',
        '[role="alert"]',
    ]
};

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const log = (msg) => console.log(`[YIT Content] ${msg}`);

function findElement(selectorList) {
    for (const selector of selectorList) {
        const el = document.querySelector(selector);
        if (el) return el;
    }
    return null;
}

async function waitForElement(selectorList, timeout = 10000) {
    const start = Date.now();
    while (Date.now() - start < timeout) {
        const el = findElement(selectorList);
        if (el) return el;
        await sleep(100);
    }
    return null;
}

// ============================================================
// CORE AUTOMATION
// ============================================================

async function submitPrompt(text) {
    log(`Submitting prompt: ${text.substring(0, 50)}...`);

    // Find input
    const input = await waitForElement(SELECTORS.promptInput);
    if (!input) throw new Error('Prompt input not found');

    // Focus and clear
    input.focus();
    input.innerHTML = '';

    // Insert text
    document.execCommand('insertText', false, text);
    input.dispatchEvent(new Event('input', { bubbles: true }));

    await sleep(CONFIG.delays.afterSubmit);

    // Find and click submit
    const submitBtn = await waitForElement(SELECTORS.submitButton);
    if (!submitBtn) throw new Error('Submit button not found');

    submitBtn.click();
    log('Prompt submitted');
}

async function waitForGeneration() {
    log('Waiting for generation...');
    const start = Date.now();

    // Wait for loading to start
    await sleep(1000);

    while (Date.now() - start < CONFIG.delays.maxWait) {
        // Check for error
        const errorEl = findElement(SELECTORS.errorMessage);
        if (errorEl && errorEl.textContent.trim()) {
            throw new Error(`Generation error: ${errorEl.textContent.trim()}`);
        }

        // Check if still loading
        const loading = findElement(SELECTORS.loadingIndicator);
        if (!loading || loading.offsetParent === null) {
            // Loading done, look for image
            await sleep(500);
            const img = findElement(SELECTORS.generatedImage);
            if (img && img.src) {
                log('Generation complete');
                return img.src;
            }
        }

        await sleep(CONFIG.delays.pollInterval);
    }

    throw new Error('Generation timeout');
}

async function downloadImage(url, filename) {
    log(`Downloading: ${filename}`);

    // Request download via background script
    return new Promise((resolve, reject) => {
        chrome.runtime.sendMessage({
            type: 'DOWNLOAD_IMAGE',
            url,
            filename
        }, (response) => {
            if (response.success) {
                resolve(response.downloadId);
            } else {
                reject(new Error('Download failed'));
            }
        });
    });
}

// ============================================================
// MESSAGE HANDLER
// ============================================================

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'GENERATE_IMAGE') {
        handleGenerateImage(message.image, message.naming);
        sendResponse({ received: true });
    }
    return true;
});

async function handleGenerateImage(image, naming) {
    const filename = `outputs/${naming.book}/ch${naming.chapter}/${naming.id}.png`;

    try {
        // Submit prompt
        await submitPrompt(image.prompt);

        // Wait for generation
        const imageUrl = await waitForGeneration();

        // Download
        await downloadImage(imageUrl, filename);
        await sleep(CONFIG.delays.afterDownload);

        // Report success
        chrome.runtime.sendMessage({
            type: 'IMAGE_GENERATED',
            result: { id: naming.id, filename, success: true }
        });

    } catch (error) {
        log(`Error: ${error.message}`);
        chrome.runtime.sendMessage({
            type: 'IMAGE_ERROR',
            error: { id: naming.id, message: error.message }
        });
    }
}

// ============================================================
// INITIALIZATION
// ============================================================

log('Content script loaded on ' + window.location.hostname);

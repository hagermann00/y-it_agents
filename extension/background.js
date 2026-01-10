// YIT Image Generator - Background Service Worker
// Manages batch queue and coordinates with content script

// ============================================================
// STATE
// ============================================================

let batchQueue = [];
let currentBatch = null;
let isProcessing = false;
let progress = { current: 0, total: 0, errors: [] };
let targetTabId = null; // Track the specific tab we're automating

// ============================================================
// MESSAGE HANDLERS
// ============================================================

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    switch (message.type) {
        case 'START_BATCH':
            handleStartBatch(message.batch);
            sendResponse({ success: true });
            break;

        case 'PAUSE_BATCH':
            isProcessing = false;
            sendResponse({ success: true, progress });
            break;

        case 'RESUME_BATCH':
            if (currentBatch && !isProcessing) {
                isProcessing = true;
                processNextImage();
            }
            sendResponse({ success: true });
            break;

        case 'GET_STATUS':
            sendResponse({
                isProcessing,
                progress,
                currentBatch: currentBatch ? {
                    book: currentBatch.book,
                    chapter: currentBatch.chapter,
                    totalImages: currentBatch.images.length
                } : null
            });
            break;

        case 'IMAGE_GENERATED':
            handleImageGenerated(message.result);
            sendResponse({ success: true });
            break;

        case 'IMAGE_ERROR':
            handleImageError(message.error);
            sendResponse({ success: true });
            break;

        default:
            sendResponse({ error: 'Unknown message type' });
    }
    return true; // Async response
});

// ============================================================
// BATCH PROCESSING
// ============================================================

async function handleStartBatch(batch) {
    currentBatch = batch;
    progress = {
        current: 0,
        total: batch.images.length,
        errors: [],
        book: batch.book,
        chapter: batch.chapter
    };
    isProcessing = true;

    // Capture the current Gemini tab
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tabs[0]) {
        targetTabId = tabs[0].id;
        console.log(`[YIT] Targeting tab ${targetTabId}`);
    }

    console.log(`[YIT] Starting batch: ${batch.book} ch${batch.chapter}, ${batch.images.length} images`);
    processNextImage();
}

async function processNextImage() {
    if (!isProcessing || !currentBatch) return;

    if (progress.current >= currentBatch.images.length) {
        // Batch complete
        await completeBatch();
        return;
    }

    const image = currentBatch.images[progress.current];
    console.log(`[YIT] Processing image ${progress.current + 1}/${progress.total}: ${image.id}`);

    // Send to the captured Gemini tab (not active tab)
    if (targetTabId) {
        chrome.tabs.sendMessage(targetTabId, {
            type: 'GENERATE_IMAGE',
            image,
            naming: {
                book: currentBatch.book,
                chapter: currentBatch.chapter,
                id: image.id
            }
        });
    } else {
        console.error('[YIT] No target tab captured!');
    }
}

function handleImageGenerated(result) {
    console.log(`[YIT] Image generated: ${result.filename}`);
    progress.current++;

    // Continue to next
    setTimeout(() => processNextImage(), 3000); // Rate limit delay
}

function handleImageError(error) {
    console.error(`[YIT] Image error:`, error);
    progress.errors.push({
        index: progress.current,
        error: error.message
    });
    progress.current++;

    // Continue despite error
    setTimeout(() => processNextImage(), 5000);
}

async function completeBatch() {
    isProcessing = false;

    // Generate manifest
    const manifest = {
        book: currentBatch.book,
        chapter: currentBatch.chapter,
        generated: new Date().toISOString(),
        images: currentBatch.images.map((img, i) => ({
            id: img.id,
            path: `outputs/${currentBatch.book}/ch${currentBatch.chapter}/${img.id}.png`,
            success: !progress.errors.find(e => e.index === i)
        })),
        errors: progress.errors
    };

    // Store manifest
    await chrome.storage.local.set({
        [`manifest_${currentBatch.book}_ch${currentBatch.chapter}`]: manifest
    });

    console.log(`[YIT] Batch complete. ${progress.errors.length} errors.`);

    // Notify popup
    chrome.runtime.sendMessage({
        type: 'BATCH_COMPLETE',
        manifest
    });

    currentBatch = null;
}

// ============================================================
// DOWNLOAD HANDLING
// ============================================================

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'DOWNLOAD_IMAGE') {
        chrome.downloads.download({
            url: message.url,
            filename: message.filename,
            saveAs: false
        }, (downloadId) => {
            sendResponse({ success: true, downloadId });
        });
        return true;
    }
});

// ==UserScript==
// @name         YIT Gemini Automation
// @namespace    http://y-it.agents/
// @version      1.0.0
// @description  Browser automation for batch image generation on Gemini/NotebookLM
// @author       Y-IT Agents
// @match        https://gemini.google.com/*
// @match        https://notebooklm.google.com/*
// @match        https://aistudio.google.com/*
// @grant        GM_download
// @grant        GM_log
// ==/UserScript==

(function () {
    'use strict';

    // ============================================================
    // CONFIGURATION
    // ============================================================

    const CONFIG = {
        // Rate limits (ms)
        delays: {
            betweenPrompts: 3000,      // 3s between submissions
            betweenDownloads: 500,     // 0.5s between downloads
            onError: 60000,            // 60s on rate limit error
            pollInterval: 1000,        // 1s polling for completion
            maxWait: 30000,            // 30s max wait for generation
        },
        // Retry settings
        maxRetries: 3,
    };

    // ============================================================
    // SELECTORS - UPDATE THESE WHEN GOOGLE CHANGES UI
    // ============================================================

    const SELECTORS = {
        // Gemini selectors (as of 2026-01)
        gemini: {
            promptInput: 'div[contenteditable="true"].ql-editor, rich-textarea div[contenteditable="true"]',
            submitButton: 'button[aria-label="Send message"], button[data-test-id="send-button"]',
            imageContainer: '.response-container img, .generated-image img',
            // Added for Text Extraction
            textContainer: '.model-response-text, .response-content',
            responseContainer: 'user-scroller .response-container:last-of-type', // Focus on last response
            loadingIndicator: '.loading-indicator, [data-loading="true"], .thinking-indicator',
            errorMessage: '.error-message, [data-error="true"]',
        },
        // NotebookLM selectors
        notebooklm: {
            promptInput: 'textarea, div[contenteditable="true"]',
            submitButton: 'button[type="submit"], button[aria-label="Send"]',
            responseContainer: '.response-content, .answer-bubble',
            textContainer: '.message-content, .answer-text',
        },
    };

    // ============================================================
    // STATE MACHINE
    // ============================================================

    const STATE = {
        IDLE: 'IDLE',
        SUBMITTING: 'SUBMITTING',
        GENERATING: 'GENERATING',
        READY: 'READY',
        EXPORTING: 'EXPORTING',
        ERROR: 'ERROR',
    };

    let currentState = STATE.IDLE;
    let batchConfig = null;
    let batchProgress = { pass: 0, variation: 0, total: 0, errors: [] };

    // ============================================================
    // UTILITY FUNCTIONS
    // ============================================================

    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    const log = (msg, level = 'info') => {
        const prefix = `[YIT ${new Date().toISOString()}]`;
        console[level](`${prefix} ${msg}`);
    };

    const getSiteType = () => {
        const host = window.location.hostname;
        if (host.includes('gemini')) return 'gemini';
        if (host.includes('notebooklm')) return 'notebooklm';
        if (host.includes('aistudio')) return 'gemini'; // Similar UI
        return 'unknown';
    };

    const getSelectors = () => {
        const site = getSiteType();
        return SELECTORS[site] || SELECTORS.gemini;
    };

    const waitForElement = async (selector, timeout = 10000) => {
        const start = Date.now();
        while (Date.now() - start < timeout) {
            const el = document.querySelector(selector);
            if (el) return el;
            await sleep(100);
        }
        throw new Error(`Element not found: ${selector}`);
    };

    // ============================================================
    // CORE API
    // ============================================================

    const YIT = {
        /**
         * Get current status
         */
        status: () => ({
            state: currentState,
            site: getSiteType(),
            batch: batchConfig ? { ...batchProgress } : null,
            timestamp: new Date().toISOString(),
        }),

        /**
         * Submit a prompt to the input field
         */
        submitPrompt: async (text) => {
            try {
                currentState = STATE.SUBMITTING;
                const selectors = getSelectors();

                // Find and focus input
                const input = await waitForElement(selectors.promptInput);
                input.focus();

                // Clear existing content
                input.innerHTML = '';

                // Insert text
                document.execCommand('insertText', false, text);

                // Trigger input events
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));

                await sleep(300); // Let UI update

                // Find and click submit
                const submitBtn = await waitForElement(selectors.submitButton);
                submitBtn.click();

                currentState = STATE.GENERATING;
                log(`Submitted prompt: ${text.substring(0, 50)}...`);
                return true;
            } catch (err) {
                currentState = STATE.ERROR;
                log(`Submit failed: ${err.message}`, 'error');
                throw err;
            }
        },

        /**
         * Wait for generation to complete
         */
        waitForComplete: async () => {
            const selectors = getSelectors();
            const start = Date.now();

            while (Date.now() - start < CONFIG.delays.maxWait) {
                // Check for error
                const errorEl = document.querySelector(selectors.errorMessage);
                if (errorEl && errorEl.textContent.trim()) {
                    currentState = STATE.ERROR;
                    throw new Error(`Generation error: ${errorEl.textContent}`);
                }

                // Check for loading indicator
                const loading = document.querySelector(selectors.loadingIndicator);
                if (!loading || loading.offsetParent === null) {
                    // No loading indicator visible = done
                    currentState = STATE.READY;
                    log('Generation complete');
                    return true;
                }

                await sleep(CONFIG.delays.pollInterval);
            }

            currentState = STATE.ERROR;
            throw new Error('Generation timeout');
        },

        /**
         * Get all generated images on the page
         */
        getImages: () => {
            const selectors = getSelectors();
            const images = document.querySelectorAll(selectors.imageContainer);
            return Array.from(images).map((img, idx) => ({
                index: idx,
                src: img.src,
                alt: img.alt || '',
            }));
        },

        /**
         * Download a single image
         */
        downloadImage: async (url, filename) => {
            try {
                currentState = STATE.EXPORTING;

                // Use GM_download if available (better for cross-origin)
                if (typeof GM_download !== 'undefined') {
                    GM_download({
                        url: url,
                        name: filename,
                        saveAs: false,
                    });
                } else {
                    // Fallback to link click
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = filename;
                    a.style.display = 'none';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                }

                log(`Downloaded: ${filename}`);
                await sleep(CONFIG.delays.betweenDownloads);
                currentState = STATE.READY;
                return true;
            } catch (err) {
                log(`Download failed: ${err.message}`, 'error');
                throw err;
            }
        },

        /**
         * Download all images with naming convention
         * @param {string} prefix - Project name prefix
         * @param {number} pass - Pass number (1 or 2)
         * @param {number} startNum - Starting sequence number
         */
        downloadAll: async (prefix, pass, startNum = 1) => {
            const images = YIT.getImages();
            const results = [];

            for (let i = 0; i < images.length; i++) {
                const seq = String(startNum + i).padStart(3, '0');
                const filename = `${prefix}_${pass}_${seq}.png`;

                try {
                    await YIT.downloadImage(images[i].src, filename);
                    results.push({ success: true, filename });
                } catch (err) {
                    results.push({ success: false, filename, error: err.message });
                }
            }

            currentState = STATE.IDLE;
            return results;
        },

        /**
         * Start a batch booking run
         * @param {Object} config - { projectName, prompts[], passCount }
         */
        startBatch: async (config) => {
            batchConfig = config;
            batchProgress = {
                pass: 0,
                variation: 0,
                total: config.prompts.length * config.passCount,
                errors: [],
            };

            log(`Starting batch: ${config.projectName}, ${batchProgress.total} total`);

            for (let pass = 1; pass <= config.passCount; pass++) {
                batchProgress.pass = pass;

                for (let i = 0; i < config.prompts.length; i++) {
                    batchProgress.variation = i + 1;

                    try {
                        // Submit prompt
                        await YIT.submitPrompt(config.prompts[i]);
                        await sleep(CONFIG.delays.betweenPrompts);

                        // Wait for generation
                        await YIT.waitForComplete();

                        // Download with naming
                        const seq = String(i + 1).padStart(3, '0');
                        const filename = `${config.projectName}_${pass}_${seq}.png`;
                        const images = YIT.getImages();

                        if (images.length > 0) {
                            await YIT.downloadImage(images[images.length - 1].src, filename);
                        }

                        await sleep(CONFIG.delays.betweenPrompts);

                    } catch (err) {
                        batchProgress.errors.push({
                            pass,
                            variation: i + 1,
                            error: err.message,
                        });
                        log(`Batch error at ${pass}-${i + 1}: ${err.message}`, 'error');

                        // Retry logic
                        await sleep(CONFIG.delays.onError);
                    }
                }
            }

            currentState = STATE.IDLE;
            log(`Batch complete. Errors: ${batchProgress.errors.length}`);
            return batchProgress;
        },

        /**
         * Pause the current batch (sets flag, batch checks this)
         */
        pauseBatch: () => {
            batchConfig = null;
            currentState = STATE.IDLE;
            log('Batch paused');
        },

        /**
         * Get batch progress
         */
        getBatchStatus: () => ({ ...batchProgress }),

        /**
         * Get the text content of the last response
         */
        getLastResponseText: () => {
            const selectors = getSelectors();
            // Try specific text container first, fall back to general response container
            const textEl = document.querySelector(selectors.textContainer) ||
                document.querySelector(selectors.responseContainer);

            if (!textEl) {
                log('No response text found', 'warn');
                return null;
            }

            // Geminis often use specific classes for the markdown content
            const markdownEl = textEl.querySelector('.markdown-content') || textEl;
            return markdownEl.textContent.trim();
        },

        // Expose config for debugging
        _config: CONFIG,
        _selectors: SELECTORS,
    };

    // ============================================================
    // INITIALIZATION
    // ============================================================

    // Expose to window for browser agent access
    window.__yit = YIT;

    // Log ready state
    log(`YIT Automation loaded on ${getSiteType()}`);
    log('Access via window.__yit');

})();

# Y-IT Antigravity Constraints

> These rules apply to ALL directives in this project. Read before executing any task.

## HARD CONSTRAINTS

### No External APIs
- ❌ No Python SDK calls (google-generativeai, openai, anthropic, etc.)
- ❌ No API keys in .env files
- ❌ No REST/HTTP calls to AI services
- ❌ No "let me write a script" for AI tasks

### No Custom Automation Scripts for AI
- ❌ No building scrapers that call external services
- ❌ No webhook/callback systems
- ❌ No background job runners

### Why?
- Gemini Ultra subscription = unlimited UI access, metered API access
- Browser automation = free usage via subscription
- Scripts = burns API quota unnecessarily
- We're leveraging the subscription, not building around it

---

## USE INSTEAD

### Browser Agent (Primary)
- ✅ Navigate to gemini.google.com
- ✅ Navigate to notebooklm.google.com
- ✅ Interact with UI elements directly
- ✅ Download outputs via browser
- ✅ Screenshot artifacts for logging

### Built-in Antigravity Models
- ✅ Gemini 3 Pro (hi/lo) - for planning, analysis
- ✅ Gemini Flash - for quick tasks
- ✅ Claude Sonnet 4.5 - for voice/style work
- ✅ Claude Opus - for complex reasoning (use sparingly)

### File Operations
- ✅ Create/edit local files
- ✅ Organize outputs into folders
- ✅ Generate markdown logs
- ✅ Process CSV/text locally

### Terminal (for non-AI tasks)
- ✅ File operations (move, copy, rename)
- ✅ Directory creation
- ✅ Git operations
- ✅ Local tooling (pandoc, etc.)

---

## MODEL SELECTION GUIDE

| Task | Model | Why |
|------|-------|-----|
| Planning/analysis | Gemini 3 Pro | Best reasoning, free quota |
| Quick classification | Gemini Flash | Fast, saves Pro quota |
| Technical content | Gemini 3 Pro Hi | Deep thinking mode |
| Satirical voice | Claude Sonnet/Opus | Better at style/tone |
| Image generation | Gemini (browser) 3 Pro | Use web UI, not API | 

---

## WORKFLOW PATTERN

```
1. Read directive from directives/
2. Check constraints (this file)
3. Use browser agent for AI services
4. Use built-in models for local reasoning
5. Save outputs to outputs/
6. Log results to .tmp/
7. Update directive with learnings
```

---

## EXCEPTION PROCESS

If a task genuinely requires API access:
1. STOP execution
2. Ask user: "This requires API calls. Proceed?"
3. Only continue with explicit approval
4. Document why in directive learnings


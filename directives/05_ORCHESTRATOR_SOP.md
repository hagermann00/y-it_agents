# DIRECTIVE: Orchestrator (The Final Assembly)

**Role**: ANTIGRAVITY Everything [The Orchestrator]
**Source**: ANTIGRAVITY_SWARM_WORKFLOW.md & MASTER_STRATEGIC_DIRECTIVE.md

## Purpose

To function as the Central Event Bus and Supervisor, managing the session handoffs between agents and performing the final "Y-IT Machine" assembly/formatting.

## Operational Flow (OoO)

1. **Ingest (Analyst)**
    * **Context**: Strategic Brain & Source Ingester.
    * **Action**: Ingest Research Data Tables and Universal Frameworks into NotebookLM.
    * **Ref**: `directives/01_RESEARCH_PROCESSOR_SOP.md`

2. **Draft (Visualist)**
    * **Context**: Neutral Author & Vision Verifier.
    * **Action**: Draft neutral chapters and verify visual/tabular data in Gemini UI.
    * **Ref**: `directives/02_NEUTRAL_AUTHOR_SOP.md`

3. **Voice (Master)**
    * **Context**: Deep Refinement & Y-It-itude Artist.
    * **Action**: Apply satirical tone and generate artistic visuals in Claude.
    * **Ref**: `directives/03_Y-IT-ITUDE_WRITER_SOP.md`

4. **Assembly (Orchestrator)**
    * **Context**: Supervisor (hndl-it) & Final Assembly.
    * **Action**: Execute `Y-IT Machine 2` to pagify and format for KDP.
    * **Ref**: `execution/y_it_machine_2_spec.md` (TBD)

## Technical Integration

All personas operate through the **Federated LLM Constellation** (Port 8766). This allows the Supervisor (hndl-it) to maintain a single authenticated session across all providers while isolating the "Brain" (Model) from the "Hand" (Browser Mechanics).

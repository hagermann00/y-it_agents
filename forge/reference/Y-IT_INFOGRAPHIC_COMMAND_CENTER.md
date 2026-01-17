# Y-IT Infographic Command Center

This document is your complete "Y-it" Infographic Command Center. It is designed to be fed directly into your AI agents within NotebookLM Studio to generate high-fidelity, on-brand infographics that are grounded in your research data.

Below you will find the Master Style Block, a technical addendum for the agent, and six universal infographic templates. Each template includes a specific prompt that references data from your notebook, alongside an example image demonstrating the correct output.

---

## Part 1: The "Y-it" Master Style Block & Palette

This block must be appended to every infographic prompt to ensure brand consistency. It defines the visual DNA of your data visualizations.

```
[Y-IT MASTER STYLE BLOCK]

Aesthetic: "Editorial Cartoon Data Viz." Clean, newspaper-style infographics with white/cream backgrounds and flat vector art. Professional but approachable.

Color Palette:
- PRIMARY: Gold/Tan (#D4A84B) for positive data and main elements
- SECONDARY: Cyan (#00D4D4) for accents and support metrics
- WARNING: Muted Red (#C94C4C) for negative data, risks, and warnings
- TEXT: Dark gray (#333333) or black for maximum readability
- BACKGROUND: White or light cream (#F9F9F9)

Visual Polish: 
- Flat vector art with clean lines
- NO glow effects, NO neon, NO 3D renders
- NO circuit board textures or futuristic overlays
- Simple drop shadows only where needed for depth
- Typography: Clean sans-serif (Inter, Roboto, or similar)

CHARACTER INTEGRATION: When PosiBot appears, use the established Gold/Tan body with Cyan screen face. Match the "Precise Cartoon" mascot aesthetic.

PRINT READINESS: All infographics must be legible when printed in black and white. Avoid relying solely on color to convey meaning.
```

---

## Part 2: Infographic Tool Capability Addendum

Include this addendum in your agent's instructions to ensure it uses the model's capabilities correctly and avoids common errors.

```
[EDITORIAL INFOGRAPHIC AGENT INSTRUCTIONS]

Reasoning-First Logic: Plan the layout structure before rendering to ensure elements are not crowded and flow logically.

Data Grounding: All statistics and labels must be directly sourced from the provided NotebookLM data tables or chapter text. Do not hallucinate data.

High Resolution Rendering: Execute final render at high resolution for maximum clarity of text and small elements.

Strict Style Adherence: Follow the [Y-IT MASTER STYLE BLOCK] precisely. 
- DO NOT use dark backgrounds
- DO NOT add glow or neon effects
- DO NOT use 3D rendered elements
- DO NOT use circuit board or tech textures

White Space: Embrace generous white space. Data should breathe.
```

---

## Part 3: Universal Layout Templates & Examples

Choose the template that best fits your data, fill in the bracketed data references, and provide it to your agent.

---

### 1. The "Disparity" Template (Expectation vs. Reality)

**Best for:** Comparing a "guru's promise" with actual results.

**Agent Prompt:**

```
Create a split-screen comparison infographic on a white background. 

LEFT SIDE (The Promise): Visualize the 'Projected Earnings' data from [Table 2.1: Guru Claims] as a rising gold bar chart with a rocket icon. Label it "THE GURU PROMISE" with "$10K MONTHLY PROFIT".

RIGHT SIDE (The Reality): Visualize the 'Actual Average Earnings' data from [Chapter 3: The First Month] as a declining muted red bar chart with a broken chain icon. Label it "THE REALITY" with "$142 MONTHLY PROFIT".

CENTER: Place a "GAP" callout box showing "STATISTICAL VARIANCE: 98.5%".

[Y-IT MASTER STYLE BLOCK]
```

**Example Image:**

![Guru vs Reality Infographic](c:/iiwii_db/y-it_agents/forge/staging/infographic_02_guru_vs_reality_correct.png)

---

### 2. The "Burden" Template (Structural Breakdown)

**Best for:** Visualizing hidden costs or hidden work.

**Agent Prompt:**

```
Design an iceberg infographic on a light blue/white background.

ABOVE WATERLINE: The small visible tip represents "PASSIVE INCOME (THE VISIBLE 10%)" from [Chapter 1: The Hook].

BELOW WATERLINE: The massive submerged base is divided into four labeled layers representing hidden tasks from [Table 4.3: Daily Operations Checklist]:
- "DAILY AD TWEAKS"
- "CUSTOMER DISPUTES" 
- "SUPPLIER DELAYS"
- "PLATFORM FEES"

FOOTER: "THE HIDDEN BURDEN OF 'EASY' MONEY"

Include Y-it logo in corner. Use flat vector art, no 3D render.

[Y-IT MASTER STYLE BLOCK]
```

**Example Image:**

![Iceberg Hidden Costs](c:/iiwii_db/y-it_agents/forge/staging/infographic_03_iceberg_correct.png)

---

### 3. The "Pulse" Template (Tactical Dashboard)

**Best for:** A summary of key performance indicators (KPIs).

**Agent Prompt:**

```
Generate a clean dashboard infographic on white background.

CENTRAL ELEMENT: Large radial gauge displaying "SURVIVAL RATE: 4%" from [Table 5.1: Industry Success Metrics]. Use cyan for the gauge arc, red for the danger zone.

SURROUNDING CARDS: Three connected metric boxes with gold borders:
- "AVG LOSS: -$2,500"
- "WORK HOURS: 60+/wk"  
- "SATURATION: CRITICAL"

Connect cards to gauge with simple lines. Flat vector style, no glow effects.

[Y-IT MASTER STYLE BLOCK]
```

**Example Image:**

![Survival Rate Dashboard](c:/iiwii_db/y-it_agents/forge/staging/infographic_04_survival_gauge_correct.png)

---

### 4. The "Friction" Template (Process Flow)

**Best for:** Showing where a process breaks down or where potential is lost.

**Agent Prompt:**

```
Create a horizontal pipeline flow visualization on white background.

INPUT (LEFT): Pipe labeled "INPUT: 10,000 CLICKS" from [Chapter 6: The Funnel].

LEAK POINTS: Three cracks in the pipe with dripping liquid and labels:
- "BAD LANDING PAGE (-40%)"
- "HIGH SHIPPING COST (-30%)"
- "OUT OF STOCK (-20%)"

OUTPUT (RIGHT): Small bucket catching remaining flow, labeled "FINAL OUTPUT: 12 SALES"

Use blue for water/flow, muted red for leak labels. Y-it logo in corner.

[Y-IT MASTER STYLE BLOCK]
```

**Example Image:**

![Leaky Pipe Funnel](c:/iiwii_db/y-it_agents/forge/staging/infographic_05_leaky_pipe_correct.png)

---

### 5. The "Metrics" Template (Data Dashboard)

**Best for:** Displaying multiple metrics in organized layout.

**Agent Prompt:**

```
Create a data metrics dashboard on white background.

CENTRAL GAUGE: Large speedometer showing "600 BRAND GAUGE" with "326 MPH" indicator.

LEFT PANEL - "DATA TARGET":
- Arrow metrics showing 800+ (Q4 Target), 750 (Current), 700 (Minimum)
- "+15% GROWTH" highlight

RIGHT PANEL - "SECONDARY METRICS":
- "50% MARKET SHARE" in circular badge
- "+385 ONLINE ENGAGEMENT" in circular badge

Use gold and cyan flat colors. Clean sans-serif typography.

[Y-IT MASTER STYLE BLOCK]
```

**Example Image:**

![Data Visualization Dashboard](c:/iiwii_db/y-it_agents/forge/staging/infographic_01_data_viz_correct.png)

---

### 6. The "Decay" Template (Resource Burn Rate)

**Best for:** Showing how quickly capital, time, or hype is depleted.

**Agent Prompt:**

```
Generate a line chart infographic titled "CAPITAL BURN RATE" on white background.

X-AXIS: "WEEK 1" through "WEEK 12"
Y-AXIS: "HYPE/CAPITAL REMAINING"

LINE: Starts high at Week 1, gradually declines. Use blue color that fades to gray as it drops.

THRESHOLD: Horizontal red line near bottom labeled "BANKRUPTCY HAZARD" at critical threshold from [Table 8.2: Financial Runway].

Clean vector style, no glow or neon effects.

[Y-IT MASTER STYLE BLOCK]
```

**Example Image:**

![Capital Burn Rate Chart](c:/iiwii_db/y-it_agents/forge/staging/infographic_06_burn_rate_correct.png)

---

*This complete package provides your NotebookLM agents with the precise instructions, data references, and visual examples needed to autonomously generate high-quality, "Y-it" branded infographics.*

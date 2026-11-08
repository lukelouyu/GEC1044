# Prompt for Claude — Two-Subsystem Causal Loop Diagram (TCM × Psychological)

> Copy everything inside the fenced block below and paste it into Claude.

```text
You are a senior System Dynamics (SD) modeler and teaching assistant for the course IE2141 Systems Thinking and Dynamics. Build me a rigorous, academically defensible Causal Loop Diagram (CLD) that would score full marks under the IE2141 mini-project rubric, especially the criteria "CLD and Dynamic Mechanism" and "Systems Thinking Interpretation (Laws / System Archetypes)."

# 1. PROJECT CONTEXT
The intervention is a "Chinese Yam, Lotus Seed and Red Date Congee (山药莲子红枣粥)" designed to improve the physical and mental wellbeing of time-constrained National University of Singapore (NUS) students. I need the model explicitly split into TWO INTERACTING subsystems, with the cross-subsystem coupling links shown clearly.

Subsystem A — TCM Physiological Subsystem
- "Overthinking injures the Spleen" (思虑伤脾): sustained academic worry and rumination constrain qi and impair the Spleen's transforming function, producing Spleen Qi deficiency symptoms such as poor appetite and fatigue.
- Ingredient properties (these are active causal agents, not just nutrition): Chinese yam/Shan Yao 山药 strengthens the Spleen and replenishes qi (健脾益气); lotus seed/Lian Zi 莲子 nourishes the Heart and calms shen (养心安神); red date/Da Zao 红枣 nourishes blood and supports the middle jiao. Together they directly improve physical energy and sleep quality (calm shen).

Subsystem B — Psychological / Behavioural Subsystem
- Rumination: repetitive, unresolved thinking about academic work that consumes psychological energy.
- Behavioural activation: because the recipe is "low-friction" (one pot, minimal washing-up, familiar ingredients, two portions at once), the barrier to starting is low, so students actually complete the task and gain a sense of control.
- Mindfulness: the 45–60 minute simmer requires waiting and attending to the present moment, which directly interrupts rumination.

# 2. VARIABLES — KEEP THE TWO TYPES STRICTLY SEPARATED
Use exactly these core variables (you may add at most a few, but keep the whole CLD at 20 variables or fewer, per the IE2141 CLD limit). Variables must be nouns or quantities that can rise or fall — never action phrases.

TCM physiological variables: Spleen Qi, Calm Shen (Heart Shen), Physical Energy, Sleep Quality, Fatigue, Therapeutic Food Effect (you may split into Spleen-strengthening effect and Shen-calming effect if needed).
Psychological variables: Rumination, Mindfulness, Behavioural Activation, Sense of Control, Low-Friction Cooking (recipe accessibility/adherence), Self-Care Engagement.
Shared/exogenous driver: Academic Stress.

First deliver a variable dictionary table: variable name | subsystem (TCM / Psychological / Shared) | plain-English definition | direction of "good" state.

# 3. SD NOTATION RULES (IE2141 conventions — non-negotiable)
- Label every causal link with its polarity: "+" (a change in A causes B to change in the SAME direction) or "–" (OPPOSITE direction).
- Name every feedback loop as R (reinforcing) or B (balancing). Verify each designation by counting the negative links: an EVEN number of negative links = reinforcing; an ODD number = balancing. If your count contradicts my label, flag it and explain rather than silently changing it.
- Mark every material time delay with the delay symbol "||" on the slow link (e.g., herbal buildup of qi, sleep recovery, habit formation), and justify each delay in one sentence.
- Show the cross-subsystem coupling explicitly, at minimum: Rumination → (–) Spleen Qi (the 思虑伤脾 link); Physical Energy → (+) Behavioural Activation / Self-Care Engagement; Calm Shen / Sleep Quality → (–) Rumination; Sense of Control → (–) perceived Academic Stress.
- This is a qualitative conceptual CLD. Do not write simulation equations, but do state your key assumptions and keep the framing causal-hypothetical (no claim of proven clinical effect).

# 4. FOUR CORE LOOPS — draw and explain each one with its full polarity path
- R1 — Physiological vicious cycle: Academic Stress → Rumination → Spleen damage (Spleen Qi down) → Physical Energy down / Fatigue up → reduced capacity to cope, which feeds back toward stress.
- R2 — Behavioural activation virtuous loop: Low-Friction Cooking → Behavioural Activation → Sense of Control → perceived stress reduced → further engagement with the routine.
- B1 — Mindfulness regulating loop: the congee-cooking/simmering process → Mindfulness / present-moment focus → Rumination down (a balancing mechanism that counteracts the rumination driving R1).
- R3 — Ingredient reinforcement loop: yam/lotus seed/red date therapeutic actions → Spleen Qi up and Calm Shen up → Physical Energy and Sleep Quality improve → greater vitality and motivation → sustained Self-Care Engagement and congee adherence, which loops back to continued therapeutic intake.

For each loop, (a) write the complete chain with per-link polarity and any "||" delay, (b) state the loop type and negative-link count, and (c) give one or two sentences interpreting the real-world dynamic.

# 5. MERMAID CODE — complete, renderable, colour-coded by mechanism
Produce a single complete Mermaid `flowchart LR` diagram (no placeholders, no truncated code) that:
- uses two `subgraph` blocks, one for each subsystem, with the shared driver placed so the coupling is visible;
- colours the mechanisms differently using `classDef`: TCM physiological nodes in a warm earth/amber palette, psychological nodes in a cool blue/teal palette, and shared/coupling nodes in a distinct neutral colour; colour intra-subsystem edges to match their subsystem and use the neutral colour for cross-subsystem coupling edges;
- puts polarity on every edge (e.g. `A -- "+" --> B`; `A -- "–" --> B`) and marks delays on the edge label using "||";
- identifies the four loops (R1, R2, B1, R3) and includes a legend explaining the colour scheme and notation.
Choose accessible, high-contrast hex values and ensure the code renders on a standard Mermaid viewer.

# 6. SYSTEM ARCHETYPE ANALYSIS — Shifting the Burden
Analyse the model using the "Shifting the Burden" archetype. Identify and justify:
- the persistent problem symptom (student fatigue / stress / poor sleep and appetite);
- the symptomatic, quick-relief solution (e.g., caffeine or energy drinks, takeout/skipping meals, distraction or avoidance, over-the-counter sleep aids) — revise these examples if the context suggests better ones;
- the fundamental solution (sustained self-care capacity: the low-friction congee routine plus behavioural activation and mindfulness, which rebuild Spleen Qi, calm shen and the sense of control);
- the two balancing loops — symptomatic relief versus slow fundamental improvement (with its delay) — and the reinforcing dependency/addiction side effect in which reliance on quick relief gradually erodes the motivation, time and capability to maintain fundamental self-care.
To avoid notation collision with my four project loops, label these archetype loops distinctly, e.g. STB-B_sym, STB-B_fund and STB-R_dep.
Then state: the underlying mental model (the "put a bandage on it" mindset), the key strategy, and three prescriptive actions following IE2141 teaching. Briefly distinguish Shifting the Burden from "Fixes that Fail" (the difference is dependency that weakens the fundamental solution, versus a side effect that directly worsens the symptom), and explain how the congee intervention deliberately strengthens the fundamental loop while avoiding dependency. Treat the archetype as a hypothesis to confirm, not a definitive diagnosis.

# 7. LEVERAGE POINTS (aligned to the IE2141 / Meadows framework)
Map your recommended interventions onto the five intervention levels from lowest to highest leverage: (1) parameter settings → (2) feedback/delays → (3) information flows → (4) decision rules → (5) goals/mental models. Identify the highest-leverage intervention in this system and explain why high numerical sensitivity is not the same as high leverage.

# 8. DELIVERABLE ORDER
Present the answer in this order, in clear academic English:
(1) variable dictionary table; (2) the four loop walk-throughs with polarity, negative-link counts and delays; (3) cross-subsystem coupling explanation; (4) the complete colour-coded Mermaid code with legend; (5) Shifting the Burden archetype analysis with mental model, strategy and three actions; (6) leverage-point mapping; (7) assumptions and limitations.
Keep claims hedged and evidence-based: this is a conceptual model of plausible mechanisms, not a demonstrated clinical treatment effect.
```

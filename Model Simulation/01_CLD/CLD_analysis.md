# Causal Loop Diagram: Chinese Yam, Lotus Seed and Red Date Congee (山药莲子红枣粥) for NUS Students

IE2141 Systems Thinking and Dynamics. Qualitative, causal-hypothetical model; no claim of proven clinical effect.

Diagram files: `congee_cld.mmd` / `congee_cld.png` (main CLD) and `congee_stb.mmd` / `congee_stb.png` (Shifting the Burden overlay).

## Design notes (departures from the original brief)

1. **B1 as first specified was not a closed loop.** "Cooking → Mindfulness → less Rumination" is an open chain. Closed through the existing links (stress lowers self-care, so less cooking and less mindfulness) it has 2 negative links and is *reinforcing*. A genuine balancing loop needs a designed decision rule — "when I catch myself ruminating, I put the pot on" (the dotted *simmer-as-pause* link).
2. **No natural goal-seeking loop exists.** Of the 31 simple feedback cycles, 22 are reinforcing and 9 balancing. The four balancing cycles that arise without any designed rule all pass through the Congee Routine → Available Study Time link; they are variants of a single time-cost brake (B2), which limits how often a student can cook rather than restoring wellbeing. The remaining five balancing cycles, including B1, only appear once the dotted rule Rumination → Congee Routine is introduced. Because balancing loops are the goal-seeking structures that move a system toward a desired state (Meadows, 2008; Sterman, 2000), without a designed rule the system can only tip between a vicious and a virtuous spiral. This makes the decision rule a structural, high-leverage intervention (Meadows, 1999).
3. **Low-Friction Cooking is exogenous.** As a fixed recipe property it cannot sit inside R2; it feeds Congee Routine (adherence), which is the loop variable.
4. **Added variables:** Academic Demands (exogenous, separate from Perceived Academic Stress), Coping Capacity, Congee Routine, Available Study Time. Main CLD = 18 variables; the archetype overlay adds Quick-Relief Use and Reliance on Quick Relief = 20 (the IE2141 limit).

## 1. Variable dictionary

| Variable | Subsystem | Definition | "Good" direction |
|---|---|---|---|
| Academic Demands | Shared (exogenous) | Objective workload: deadlines, exams, assessment density | n/a |
| Perceived Academic Stress | Shared | Felt pressure relative to perceived ability to cope | ↓ |
| Coping Capacity | Shared | Physical and mental resources available to meet demands | ↑ |
| Available Study Time | Shared | Discretionary hours left after self-care activities | ↑ (within reason) |
| Spleen Qi | TCM | Traditional functional capacity to transform food into qi (proxy: appetite, post-meal energy) | ↑ |
| Spleen-Strengthening Effect | TCM | Cumulative 健脾益气 action of yam (chief), red date and rice | ↑ |
| Shen-Calming Effect | TCM | Cumulative 养心安神 action of lotus seed (and red date) | ↑ |
| Calm Shen | TCM | Settledness of the Heart-housed shen | ↑ |
| Sleep Quality | TCM | Ease of falling asleep, continuity, restorativeness | ↑ |
| Physical Energy | TCM | Available daytime vitality | ↑ |
| Fatigue | TCM | Felt tiredness / exhaustion (the symptom) | ↓ |
| Rumination | Psychological | Repetitive, unresolved thinking about academic work | ↓ |
| Mindfulness | Psychological | Present-moment, non-judgemental attention | ↑ |
| Behavioural Activation | Psychological | Engagement in achievable, completed, valued activities | ↑ |
| Sense of Control | Psychological | Perceived mastery over one's routine and outcomes | ↑ |
| Self-Care Engagement | Psychological | Motivation and willingness to invest in self-care | ↑ |
| Congee Routine (adherence) | Psychological / behavioural | Batches cooked and eaten per week | ↑ (sustainable level) |
| Low-Friction Cooking | Psychological (exogenous) | Recipe accessibility: one pot, familiar ingredients, two portions | ↑ |
| *Quick-Relief Use* (overlay) | Shared | Kopi / energy drinks, delivery or skipped meals, scrolling | ↓ |
| *Reliance on Quick Relief* (overlay) | Shared | Habitual dependence built from repeated quick relief | ↓ |

## 2. Loop walk-throughs

Notation: →(+) same direction, →(–) opposite direction, || delay.

**R1 — stress–Spleen vicious cycle.** Perceived Academic Stress →(+) Rumination →(– ||) Spleen Qi →(+) Physical Energy →(–) Fatigue →(–) Coping Capacity →(–) Perceived Academic Stress. **4 negatives → reinforcing.** Sustained worry slowly impairs the Spleen's transforming function (思虑伤脾); the resulting fatigue weakens coping, so the same workload feels more threatening.

**R2 — activation–control virtuous loop.** Congee Routine →(+) Behavioural Activation →(+) Sense of Control →(–) Perceived Academic Stress →(–) Self-Care Engagement →(+ ||) Congee Routine. **2 negatives → reinforcing.** Each finished batch is a concrete success; control lowers stress, freeing motivation for the next batch. It can run backwards: high stress crowds out cooking.

**B1 — simmer-as-pause mindfulness brake.** Rumination →(+, designed) Congee Routine →(+) Mindfulness →(–) Rumination. **1 negative → balancing** (only with the designed link). The 45–60 min simmer interrupts rumination; cooking capacity limits how much B1 can offset R1.

**R3a — ingredient reinforcement, Spleen branch.** Congee Routine →(+) Spleen-Strengthening Effect →(+ ||) Spleen Qi →(+) Physical Energy →(+) Self-Care Engagement →(+ ||) Congee Routine. **0 negatives → reinforcing.**

**R3b — ingredient reinforcement, shen branch.** Congee Routine →(+) Shen-Calming Effect →(+ ||) Calm Shen →(+ ||) Sleep Quality →(–) Fatigue →(–) Self-Care Engagement →(+ ||) Congee Routine. **2 negatives → reinforcing.** Benefits arrive weeks after the effort, so this loop is the most vulnerable to early abandonment.

**Secondary loops.** R4 rumination–sleep spiral: Rumination →(–) Calm Shen →(+ ||) Sleep Quality →(–) Rumination (2 negatives, reinforcing). B2 time-cost brake: Congee Routine →(–) Available Study Time →(–) Perceived Academic Stress →(–) Self-Care Engagement →(+ ||) Congee Routine (3 negatives, balancing).

**Delays**

| Link | Justification |
|---|---|
| Rumination → Spleen Qi | Emotional injury arises from prolonged brooding; accumulates over weeks |
| Spleen-Strengthening Effect → Spleen Qi | Food-therapy tonification is cumulative; one meal cannot establish improvement |
| Shen-Calming Effect → Calm Shen | Builds with repeated intake |
| Calm Shen → Sleep Quality | Sleep needs several nights to recover (Lo et al., 2016: 2 recovery nights insufficient) |
| Self-Care Engagement → Congee Routine | Habit formation: median 59–66 days (Singh et al., 2024) |

## 3. Cross-subsystem coupling

Psychological → TCM: Rumination →(– ||) Spleen Qi (思虑伤脾); Rumination →(–) Calm Shen; Congee Routine →(+) both therapeutic effects. TCM → psychological: Sleep Quality →(–) Rumination; Physical Energy →(+) Self-Care Engagement; Fatigue →(–) Self-Care Engagement. Shared: Sense of Control →(–) Perceived Academic Stress; Perceived Academic Stress →(+) Rumination and →(–) Self-Care Engagement; Fatigue →(–) Coping Capacity; Congee Routine →(–) Available Study Time.

No core loop stays inside one subsystem, so a single-sided intervention (a yam supplement alone, or a mindfulness app alone) attacks only part of each loop. The congee works on both because cooking is a behaviour and eating is the route for the food effects.

## 4. Diagram

See `congee_cld.mmd` (renders on mermaid.live) and `congee_cld.png`. Amber = TCM, teal = psychological, grey = shared and coupling; dotted edge = designed decision rule; dashed box = exogenous input; red circles = reinforcing, green = balancing.

## 5. Shifting the Burden (hypothesis)

- **Problem symptom:** Fatigue (with poor appetite, poor sleep, felt stress).
- **Symptomatic solution:** Quick-Relief Use — kopi / energy drinks, delivery food or skipped meals, scrolling, all-nighters.
- **Fundamental solution:** sustained self-care capacity — Congee Routine with behavioural activation and mindfulness.
- **STB-B_sym:** Fatigue →(+) Quick-Relief Use →(–) Fatigue (1 negative, balancing; fast, masks symptom).
- **STB-B_fund:** Fatigue →(+, designed trigger) Self-Care Engagement →(+ ||) Congee Routine →(+) Spleen-Strengthening Effect →(+ ||) Spleen Qi →(+) Physical Energy →(–) Fatigue (1 negative, balancing; slow).
- **STB-R_dep:** Quick-Relief Use →(+ ||) Reliance →(–) Self-Care Engagement → … →(–) Fatigue →(+) Quick-Relief Use (2 negatives, reinforcing).
- **Rigour note:** in the baseline CLD Fatigue →(–) Self-Care Engagement, so the "fundamental" loop is reinforcing, not balancing — the textbook B_fund exists only if the symptom triggers self-care. This explains why the burden shifts so easily.
- **Mental model:** "Put a bandage on it" — push through with caffeine now, look after myself after exams.
- **Strategy:** strengthen the fundamental solution, make its delay tolerable, use the symptomatic fix only as a bounded bridge.
- **Three actions:** (1) pre-commit fixed weekly batch slots; (2) cap quick relief (e.g. one kopi before 2 pm); (3) log appetite, energy and sleep 1–5 after each batch so the slow improvement is visible.
- **vs Fixes that Fail:** STB's side effect weakens the fundamental solution; FtF's side effect directly worsens the symptom. The overlay contains both: late caffeine →(–) Sleep →(–) Fatigue →(+) caffeine (2 negatives, reinforcing) is an embedded FtF structure.

## 6. Leverage points

| Level (low → high) | Intervention |
|---|---|
| 1. Parameters | Ingredient weights, simmer time, portions, cost |
| 2. Feedback and delays | Fixed weekly slot to shorten habit delay; less active cooking time to weaken B2 |
| 3. Information flows | Batch log and quick-relief tally |
| 4. Decision rules | Simmer-as-pause (creates B1); "when run-down, cook before kopi" (creates STB-B_fund); quick-relief cap |
| 5. Goals / mental models | Self-care as infrastructure for studying, not a post-exam reward |

Highest leverage: level 5, operationalised through level 4 — the only interventions that change structure. High numerical sensitivity (e.g. ingredient dose) is not high leverage: in the simulation, doubling the dose looked powerful only under a linear dose-response assumption; with a saturating response it rarely beats the decision rules.

## 7. Assumptions and limitations

Qualitative model; link strengths and loop dominance estimated, not measured. TCM constructs are traditional functional concepts needing proxies. Ingredient links assume a matching pattern (Spleen qi / Heart–Spleen deficiency). Designed links are proposed rules, not observed behaviour. Physical ceilings (sleep, satiety, time) are implicit. Omitted: Spleen Qi → Calm Shen via blood; social factors.

## 8. Simulation summary (see `02_Simulation`)

Calibrated to NUS data (OSA Student Wellbeing Pulse 2024; Health@NUS; NUS Registrar workload), Singapore surveys and TCM sources. Finals-week effects vs no congee: congee alone SMD 0.30 (mental), congee + decision rules 0.51 (+6.7 index points). See `parameter_sources.csv` for provenance and `references.md` for citations.

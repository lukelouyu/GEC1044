# CLD v3 (TCM holistic): Chinese yam, lotus seed and red date congee for time-constrained NUS students

Diagrams:
- `congee_cld_v3_20var.png`: **20-variable version for IE2141 submission** (section 6).
- `congee_cld_v3_holistic.png`: full 27-variable version.
- `congee_cld_v2.png`: the earlier version without the holistic revision, kept for comparison.
Edge list and loop audit: `../code/cld_v3.py`. Running `python cld_v3.py` checks that every R/B label matches its count of negative links.
Stock-and-flow version: `../2_SFD_Stella/congee_model_v3.stmx` (Stella Architect) and `congee_sfd_v3.png`.

This is a qualitative, causal-hypothetical model. It does not claim a proven clinical effect.

---

## 0. What changed and why (summary)

| Change | Request | Status |
|---|---|---|
| Cooking Workload, Recovery Break, cooking → Mindfulness | Workload of preparation; mindfulness of cooking | Added in v2, kept |
| Spleen Function → physical and mental wellbeing | Spleen → wellbeing | v2 direct links; physical now runs through Qi & Blood Generation |
| Liver Qi Stagnation (Five Elements) | Holistic revision, item 1 | Added as specified |
| Qi & Blood Generation, Heart Blood / Shen Malnourishment | Item 2 | Added as specified |
| Circadian Rhythm Disruption | Item 3 | Added as specified (see note 3) |
| TCM Non-Pharmacological Interventions | Item 4 | Added as specified |
| Body Awareness + B4 | Item 5 | Added, **with one extra link so that B4 is really balancing** (see note 1) |
| Individual Constitution | Item 6 | Added as an exogenous moderator (parameter switch) |

**Notes flagged rather than silently changed** (as the original IE2141 brief asked):

1. **B4 needs Fatigue → Body Awareness (+).** With only `Mindfulness → Body Awareness (+)` and `Body Awareness → Fatigue (–)`, there is no direct return path. The only way back from Fatigue to Mindfulness is Fatigue →(–) Physical Wellbeing → Self-Care → Congee Routine → Cooking Workload → Mindfulness. That route has **two** negative links, so the loop is *reinforcing* (listed below as R13). The loop audit confirms this: without the extra link, none of the 71 cycles through Body Awareness is balancing. Adding `Fatigue →(+) Body Awareness` ("early tiredness is a signal you can notice") gives `Fatigue → Body Awareness →(–) Fatigue`, one negative link, so B4 becomes a genuine goal-seeking loop. Mindfulness then sets *how sensitive* that alarm is. In the SFD: Body Awareness = 2 × Mindfulness × Felt Fatigue.
2. **The full holistic CLD has 27 variables**, above the IE2141 limit of 20. A 20-variable version with seven merges is in section 6 and `congee_cld_v3_20var.png`.
3. **Circadian Rhythm Disruption is drawn as an exogenous (dashed) node, as requested.** It is driven only by Academic Demands, so it sits on an exogenous chain and is not inside any loop. Adding `Perceived Academic Stress → Circadian Disruption` (stress-driven all-nighters) would bring it into the feedback structure.
4. **`Spleen Function → Calm Shen` (v2) is replaced by `Spleen Function →(–) Heart Blood / Shen Malnourishment`.** This keeps the same Heart–Spleen rationale, now made explicit, and avoids counting the same mechanism twice.
5. **v1 "Physical Energy" became `Qi & Blood Generation`.** v2 had folded Physical Energy into Spleen Function; it is now restored as the qi-blood node, and Spleen Function acts on Fatigue and Physical Wellbeing through it.

---

## 1. New and modified nodes

**New nodes**
- **Liver Qi Stagnation (肝气郁结)**: teal box with an amber border, a psychological–physiological bridge. Constrained, stagnant Liver qi from emotional strain; the Five-Element route by which stress injures the Spleen (Wood overacting Earth, 肝木乘脾). Stock in the SFD (builds over about a week, soothed by TCM practice).
- **Qi & Blood Generation (气血生化)**: TCM, replaces v1 "Physical Energy". The Spleen as "the source of qi and blood" (气血生化之源). SFD converter: 0.1 + 0.8 × Spleen Function + gentle-movement bonus.
- **Heart Blood / Shen Malnourishment (心血/心神失养)**: TCM. The Heart is short of blood to house the shen when the Spleen and qi-blood are weak (the Heart–Spleen deficiency pattern, 心脾两虚). SFD converter.
- **Circadian Rhythm Disruption / All-nighters (昼夜节律紊乱/熬夜)**: exogenous, dashed. Tian Ren He Yi (天人合一): living against the day–night rhythm. In the SFD it is the share of late or all-night study nights, rising with study load (about 0.15 in the holidays, about 0.74 in finals; NUS freshmen's mean bedtime was 01:53, Soon et al., 2025).
- **TCM Non-Pharmacological Interventions (中医非药物干预)**: psychological/behavioural. Acupoint massage, Baduanjin and gentle exercise, done more when Self-Care Engagement is high.
- **Body Awareness (身体觉察)**: psychological. Noticing early bodily signals and resting or self-caring early (Zhi Wei Bing, 治未病: treat before illness appears).
- **Individual Constitution (个体体质)**: exogenous, dashed, TCM. Balanced, Yin deficiency or Yang deficiency. It is a moderator, not a causal variable (see section 5).

**Modified nodes**
- Physical Energy (v1) → **Qi & Blood Generation**.
- Coping Capacity, Available Study Time and Low-Friction Cooking (v1) were folded into links and parameters in v2. Quick-Relief Use and Reliance were merged into **Unhealthy Habits** (caffeine, cigarettes, alcohol, junk food).
- **Cooking Workload** and **Recovery Break** (added in v2) model the preparation workload: about 20 min active preparation, a 45 min simmer with occasional stirring, and about 10 min clean-up, i.e. 1.25 h per two-portion batch.

**Full variable list (27):**
- Shared: Academic Demands*, Circadian Rhythm Disruption*, Perceived Academic Stress, Unhealthy Habits.
- TCM: Spleen-Strengthening Effect, Shen-Calming Effect, Spleen Function, Qi & Blood Generation, Heart Blood / Shen Malnourishment, Calm Shen, Sleep Quality, Fatigue, Individual Constitution*.
- Bridge: Liver Qi Stagnation.
- Psychological / behavioural: Planned Frequency*, Congee Routine, Cooking Workload, Recovery Break, Mindfulness, Body Awareness, Rumination, Behavioural Activation, Sense of Control, Self-Care Engagement, TCM Non-Pharmacological Interventions.
- Outcomes: Physical Wellbeing, Mental Wellbeing.

(* = exogenous)

---

## 2. New links (polarity, delays)

`||` = material time delay.

**Five Elements: Liver overacts Spleen**
- Perceived Academic Stress **+** Liver Qi Stagnation
- Rumination **+** Liver Qi Stagnation
- Liver Qi Stagnation **– ||** Spleen Function (Wood overacting Earth; slow functional injury, like 思虑伤脾)

**Qi and blood, Heart–Spleen**
- Spleen Function **+** Qi & Blood Generation
- Spleen Function **–** Heart Blood / Shen Malnourishment (replaces v2 Spleen Function + Calm Shen)
- Qi & Blood Generation **–** Heart Blood / Shen Malnourishment
- Heart Blood / Shen Malnourishment **+** Rumination
- Heart Blood / Shen Malnourishment **–** Sleep Quality
- Qi & Blood Generation **–** Fatigue (replaces v2 Spleen Function – Fatigue)
- Qi & Blood Generation **+** Physical Wellbeing (replaces v2 Spleen Function + Physical Wellbeing)

**Heaven and Human Unity (circadian rhythm)**
- Academic Demands **+** Circadian Rhythm Disruption
- Circadian Rhythm Disruption **– ||** Spleen Function (staying up late consumes Yang qi)
- Circadian Rhythm Disruption **–** Calm Shen
- Circadian Rhythm Disruption **–** Sleep Quality

**TCM interventions beyond eating**
- Self-Care Engagement **+** TCM Non-Pharmacological Interventions
- TCM Non-Pharmacological Interventions **–** Liver Qi Stagnation (soothing the Liver, 疏肝)
- TCM Non-Pharmacological Interventions **+** Qi & Blood Generation (movement generates Yang and qi-blood)

**Zhi Wei Bing early warning**
- Mindfulness **+** Body Awareness
- Fatigue **+** Body Awareness (**added** so that B4 closes; see note 1)
- Body Awareness **–** Fatigue (early rest before fatigue becomes severe)

**Constitution (moderators, dotted, no fixed polarity)**
- Individual Constitution → Sleep Quality: Yin deficiency makes the circadian and Heart-blood links to sleep 1.5× stronger.
- Individual Constitution → Fatigue: Yang deficiency makes study load build fatigue 1.5× faster.

**Kept from v2 (workload and mindfulness of cooking)**
- Congee Routine **+** Cooking Workload
- Cooking Workload **+** Recovery Break
- Recovery Break **–** Fatigue
- Cooking Workload **+** Fatigue (small physical effort)
- Cooking Workload **+** Perceived Stress (time squeeze)
- Cooking Workload **–** Congee Routine (preparation burden under stress)
- Cooking Workload **+** Mindfulness
- Mindfulness **–** Rumination
- Mindfulness **+** Mental Wellbeing
- Spleen Function **+** Mental Wellbeing

---

## 3. Feedback loops created or changed by the holistic update

Negative links are counted for every loop: an even count is reinforcing (R), an odd count is balancing (B). `cld_v3.py` checks all of them.

**New loops**
- **R9 – Liver Wood overacts Spleen Earth (肝木乘脾).** Stress →(+) Liver Qi Stagnation →(– ||) Spleen Function →(+) Qi & Blood →(–) Fatigue →(+) Stress. 2 negatives, reinforcing. Exam stress stagnates Liver qi, which weakens the Spleen; less qi-blood means more fatigue and less coping, so stress rises further. A second, emotional route into the v1 stress–Spleen vicious cycle (R1).
- **R10 – Liver–Spleen–Heart rumination loop.** Rumination →(+) Liver Qi Stagnation →(– ||) Spleen →(–) Heart Blood/Shen Malnourishment →(+) Rumination. 2 negatives, reinforcing. Brooding stagnates qi and weakens the Spleen; the unnourished Heart cannot settle the mind, so brooding continues.
- **R5 (revised) – Heart–Spleen deficiency (心脾两虚).** Rumination →(– ||) Spleen →(–) Heart Blood/Shen Malnourishment →(+) Rumination. 2 negatives, reinforcing. The classic pattern of overthinking, poor appetite, fatigue and insomnia.
- **R11 – TCM practice builds qi and blood.** Self-Care →(+) TCM Interventions →(+) Qi & Blood →(+) Physical Wellbeing →(+) Self-Care. 0 negatives, reinforcing (virtuous).
- **R12 – TCM practice soothes the Liver.** Self-Care →(+) TCM Interventions →(–) Liver Qi Stagnation →(– ||) Spleen →(+) Qi & Blood →(+) Physical Wellbeing →(+) Self-Care. 2 negatives, reinforcing (virtuous).
- **B4 – Zhi Wei Bing early-warning brake (治未病).** Fatigue →(+) Body Awareness →(–) Fatigue. 1 negative, balancing. The only balancing loop that works *before* the problem becomes a symptom. Mindfulness (fed by cooking) raises its gain.
- **R13 – mindful-awareness loop** (the loop the original B4 links actually form). Cooking Workload →(+) Mindfulness →(+) Body Awareness →(–) Fatigue →(–) Physical Wellbeing →(+) Self-Care →(+ ||) Congee Routine →(+) Cooking Workload. 2 negatives, reinforcing.

**Loops re-routed through Qi & Blood** (type unchanged)
- **R1 – stress–Spleen.** Stress → Rumination →(– ||) Spleen → Qi & Blood →(–) Fatigue → Stress. 2 negatives, R.
- **R3a – ingredients → Spleen → qi & blood.** Congee → Spleen-Strengthening Effect →|| Spleen → Qi & Blood → Physical Wellbeing → Self-Care →|| Congee. 0 negatives, R.
- **R8 – habits injure the Spleen (Fixes that Fail).** Unhealthy Habits →(– ||) Spleen → Qi & Blood →(–) Fatigue →(+) Unhealthy Habits. 2 negatives, R.
- **STB-R – dependency erodes self-care.** Unhealthy Habits →(–) Self-Care →|| Congee → Spleen-Strengthening →|| Spleen → Qi & Blood →(–) Fatigue →(+) Unhealthy Habits. 2 negatives, R.

**Loops unchanged from v2**
- R2 activation–control
- R3b ingredients → Shen
- R4 rumination–sleep
- R6 cooking–mindfulness
- R7 recovery break
- B1 masking quick fix
- B2 time-cost brake
- B3 workload brake

**Structure count:** 63 causal links plus 2 moderators, and 766 simple feedback cycles (576 reinforcing, 190 balancing).

---

## 4. Rationale: why this is a TCM holistic system dynamics model

- **Holism (整体观) in the structure, not just the labels.** Every core loop now passes through more than one Zang-Fu organ (Liver, Spleen, Heart) and through both body and mind. Stress does not act on "the student" in general: it travels Liver → Spleen → Heart, the way TCM traces emotional injury.
- **Five-Element dynamics become feedback.** Wood overacting Earth (R9, R10) is a reinforcing loop with a delay, which explains why exam-period stress keeps hurting digestion and energy after the exam pressure eases.
- **Qi and blood is the shared currency.** One node (Qi & Blood Generation) links digestion, energy, fatigue recovery and Heart nourishment, so a single intervention on the Spleen spreads to sleep and mood.
- **Heaven and Human Unity (天人合一).** The academic calendar affects the body directly through broken day–night rhythm, not only through felt stress. Exam weeks harm the Spleen, Shen and sleep even when a student feels calm.
- **Treating the undiseased (治未病).** B4 is the model's only early-acting balancing loop: rest is triggered by awareness of mild fatigue, before the vicious cycles take hold. The congee works upstream: cooking → mindfulness → body awareness.
- **Pattern differentiation through constitution (辨证/体质).** The same stressors hit different students in different places (see section 5). This is how TCM individualises treatment.
- **More than food therapy.** TCM practice (acupoint massage, Baduanjin) is a second self-care path, so the model compares the congee within a wider TCM self-care system rather than as a single remedy.

---

## 5. Individual Constitution as a parameter switch

Constitution is not caused by anything in the model and does not form loops. It changes **how strongly** existing links act; in system dynamics terms it is a structural parameter or moderator. In the SFD it is the converter `Constitution` (0 balanced, 1 Yin deficiency, 2 Yang deficiency), which feeds two graphical functions:

| Constitution | Yin Deficiency Factor | Yang Deficiency Factor | Effect in the equations |
|---|---|---|---|
| 0 Balanced | 1.0 | 1.0 | baseline |
| 1 Yin deficiency (阴虚) | **1.5** | 1.0 | Sleep loses 1.5× more from late nights and Heart-blood malnourishment (deficient Yin cannot anchor Yang at night, so empty heat disturbs the shen and causes insomnia) |
| 2 Yang deficiency (阳虚) | 1.0 | **1.5** | Study load builds fatigue 1.5× faster (too little Yang to power activity, so tiredness and cold set in) |

Simulated finals-week medians (1,000 students). Sleep quality and fatigue are on a 0–100 scale; lower fatigue is better.

| Scenario | Sleep quality: balanced / Yin-def. | Fatigue: balanced / Yang-def. |
|---|---|---|
| S2 healthy lifestyle | 57 / 42 | 49 / 59 |
| S4 congee every day | 65 / 50 | 44 / 54 |

Congee lifts every constitution, but the gap between constitutions stays about the same. This recipe strengthens the Spleen and calms the shen; it does not specifically nourish Yin or warm Yang. In TCM terms, a pattern-matched diet (辨证施膳) would be needed for those students. Evidence: in small student surveys, Yang deficiency was the most common constitution among students with mental fatigue (Beijing University of Chinese Medicine, 2016), and Yin deficiency was among the constitutions linked to poor sleep (Huachiew Chalermprakiet University students). Both studies are small and cross-sectional, so the 1.5× factors are illustrative.

---

## 6. 20-variable version for IE2141 (submission CLD)

Diagram: `congee_cld_v3_20var.png` (and `.svg`). Edge list and loop audit: `../code/cld_v3_20.py`.

The full 27-variable CLD above is kept as the detailed reference. The 20-variable version makes **seven merges**. Every concept from the holistic revision is still in the diagram, either as its own node or written into a merged node's label, and every loop keeps its type. The Stella SFD and the simulation are unchanged.

| # | Merge | How it appears in the 20-variable CLD |
|---|---|---|
| 1 | Planned Frequency → parameter | ⚙ grey note on Congee Routine: "scenario lever: none / once a week / every day". Not a variable. |
| 2 | Individual Constitution → parameter | ⚙ grey note near Fatigue / Sleep: "Yin deficiency ×1.5 on sleep links; Yang deficiency ×1.5 on fatigue build-up". Not a variable. |
| 3 | Spleen-Strengthening Effect + Shen-Calming Effect | **Food-Therapy Effect (yam, lotus seed, red date)**: + || Spleen Function; – || Heart Blood / Shen Malnourishment |
| 4 | Calm Shen → folded into **Heart Blood / Shen Malnourishment** (its inverse) | Polarities flipped: Rumination +, Circadian Disruption +, Food-Therapy Effect – || into it; out of it: – || Sleep, – Mental Wellbeing |
| 5 | Behavioural Activation → **Sense of Control (behavioural activation)** | Congee Routine + Sense of Control |
| 6 | Recovery Break → net link | Cooking Workload **–** Fatigue: the recovery break outweighs the small preparation effort (in the SFD both are kept separately) |
| 7 | TCM Non-Pharmacological Interventions → under **Self-Care Engagement (congee + TCM practice: acupoint massage, Baduanjin)** | Self-Care – Liver Qi Stagnation; Self-Care + Qi & Blood Generation. Matches the brief's "Modify Node: under Self-Care Engagement". |

**The 20 variables:**
- Exogenous: Academic Demands, Circadian Rhythm Disruption.
- Shared: Perceived Academic Stress, Unhealthy Habits.
- Bridge: Liver Qi Stagnation.
- TCM: Food-Therapy Effect, Spleen Function, Qi & Blood Generation, Heart Blood / Shen Malnourishment, Sleep Quality, Fatigue.
- Psychological / behavioural: Congee Routine, Cooking Workload, Mindfulness, Body Awareness, Rumination, Sense of Control, Self-Care Engagement.
- Outcomes: Physical Wellbeing, Mental Wellbeing.

**Totals:** 56 links and 653 simple feedback cycles (540 reinforcing, 113 balancing).

**Named loops in the 20-variable CLD** (all checked by counting negative links):

| Loop | Path | Negatives | Type |
|---|---|---|---|
| R1 stress–Spleen | Stress → Rumination →(– ‖) Spleen → Qi & Blood →(–) Fatigue → Stress | 2 | R |
| R2 activation–control | Congee → Sense of Control → Mental Wellbeing → Self-Care →‖ Congee | 0 | R |
| R3a ingredients → Spleen | Congee → Food-Therapy →‖ Spleen → Qi & Blood → Physical → Self-Care →‖ Congee | 0 | R |
| R3b ingredients → Shen | Congee → Food-Therapy →(– ‖) Heart Blood Maln. →(– ‖) Sleep →(–) Fatigue →(–) Physical → Self-Care →‖ Congee | 4 | R |
| R4 rumination–sleep | Rumination → Heart Blood Maln. →(–) Sleep →(–) Rumination | 2 | R |
| R5 Heart–Spleen deficiency | Rumination →(– ‖) Spleen →(–) Heart Blood Maln. → Rumination | 2 | R |
| R5b worry–shen spiral | Rumination → Heart Blood Maln. → Rumination | 0 | R |
| R6 cooking–mindfulness | Cooking → Mindfulness →(–) Rumination →(–) Mental → Self-Care → Congee → Cooking | 2 | R |
| R7 recovery break | Cooking →(–) Fatigue →(–) Physical → Self-Care → Congee → Cooking | 2 | R |
| R8 habits injure Spleen | Habits →(– ‖) Spleen → Qi & Blood →(–) Fatigue → Habits | 2 | R |
| R9 Liver overacts Spleen | Stress → Liver →(– ‖) Spleen → Qi & Blood →(–) Fatigue → Stress | 2 | R |
| R10 Liver–Spleen–Heart | Rumination → Liver →(– ‖) Spleen →(–) Heart Blood Maln. → Rumination | 2 | R |
| R11 TCM practice builds qi & blood | Self-Care → Qi & Blood → Physical → Self-Care | 0 | R |
| R12 TCM practice soothes the Liver | Self-Care →(–) Liver →(– ‖) Spleen → Qi & Blood → Physical → Self-Care | 2 | R |
| R13 mindful awareness | Cooking → Mindfulness → Body Awareness →(–) Fatigue →(–) Physical → Self-Care → Congee → Cooking | 2 | R |
| B1 masking quick fix | Fatigue → Habits →(–, felt) Fatigue | 1 | B |
| B2 time-cost brake | Congee → Cooking → Stress →(–) Mental → Self-Care → Congee | 1 | B |
| B3 workload brake | Congee → Cooking →(–) Congee | 1 | B |
| B4 Zhi Wei Bing early-warning brake | Fatigue → Body Awareness →(–) Fatigue | 1 | B |
| STB-R dependency | Habits →(–) Self-Care → Congee → Food-Therapy → Spleen → Qi & Blood →(–) Fatigue → Habits | 2 | R |

R5b is a short loop that the merge makes visible: worry disturbs the shen, and a disturbed, unnourished shen breeds more worry.

**Where each CLD variable lives in the Stella SFD**

| CLD variable (20-variable version) | SFD elements (`congee_model_v3.stmx`) |
|---|---|
| Academic Demands | Academic Demands (graphical function of TIME), Course Load, Study Load, Free Hours |
| Circadian Rhythm Disruption | Circadian Disruption |
| Perceived Academic Stress | stock Perceived Stress |
| Unhealthy Habits | stock Unhealthy Habits; Lifestyle Propensity; Felt Fatigue |
| Liver Qi Stagnation | stock Liver Qi Stagnation |
| Food-Therapy Effect | Spleen Strengthening Effect + Shen Calming Effect |
| Spleen Function | stock Spleen Function |
| Qi & Blood Generation | Qi Blood Generation |
| Heart Blood / Shen Malnourishment | Heart Blood Malnourishment + stock Calm Shen (inverse) |
| Sleep Quality | stock Sleep Quality |
| Fatigue | stock Fatigue; Felt Fatigue |
| Physical / Mental Wellbeing | Physical Wellbeing, Mental Wellbeing |
| Congee Routine | Congee Plan, Planned Servings, Adherence, Servings Eaten, stock Congee Habit |
| Cooking Workload | Batches Cooked, Cooking Workload, Recovery Break, Time Squeeze |
| Mindfulness | stock Mindfulness; Mindful Cooking |
| Body Awareness | Body Awareness |
| Rumination | stock Rumination |
| Sense of Control | stock Sense of Control + Behavioural Activation |
| Self-Care Engagement | stock Self Care Engagement + TCM Practice |
| (parameters) | Scenario (planned frequency, lifestyle); Constitution, Yin / Yang Deficiency Factor |

---

## 7. Evidence used for the new mechanisms

**Mindfulness of cooking.** There is no randomised trial of "mindful cooking" itself, so the model borrows from close evidence:
- Informal mindfulness while washing dishes raised state mindfulness, cut nervousness by about 27% and raised inspiration by about 25% (Hanley et al., 2015).
- In a daily-diary study of 658 young adults, everyday creative activity predicted more positive affect and flourishing the next day, not the reverse (Conner et al., 2018).
- A 7-week cooking programme improved mental health and subjective vitality for 6 months against controls, although diet did not change; the authors credit cooking confidence and satisfaction (Rees et al., 2022).
- Cooking interventions benefited affect, self-esteem and quality of life, but evidence quality is low (Farmer et al., 2018).
- Bound used: the effect of daily congee on mental wellbeing is capped at the effect of formal mindfulness programmes on stress (g = 0.52; Querstret et al., 2020).

**Preparation workload as a recovery break.** Micro-breaks reduce fatigue (d = 0.35) and raise vigour (d = 0.36), and longer breaks help more after depleting tasks (Albulescu et al., 2022). Psychological detachment from work is a core recovery experience (Sonnentag & Fritz, 2007). The time cost is modelled as cooking hours ÷ free waking hours, so it bites hardest in exam weeks.

**Spleen → mind.** The brain–gut pathway is bidirectional: gut disorders predicted later anxiety and depression over 12 years, and vice versa (Koloski et al., 2012). Formulas for Heart–Spleen deficiency (Guipi decoction) and for Liver stagnation with Spleen deficiency (Xiaoyao San) show benefits on depression in mostly small Chinese trials.

**Baduanjin.** A meta-analysis found reduced anxiety (g = −0.99) and depression (g = −1.07), but with high risk of bias (Zou et al., 2018). The model link strength is therefore modest (±30% uncertainty).

**Bad habits.** Ultra-processed food is linked to later depression (HR 1.22; Lane et al., 2022). Alcohol fragments the second half of the night (Ebrahim et al., 2013). Caffeine taken 6 h before bed cut sleep by more than 1 h (Drake et al., 2013). The gap between the bad-habit and healthy scenarios is calibrated to the Health@NUS associations of limited unhealthy food (+3.80 WHO-5 points) plus adequate sleep (+4.86); the model gives 8.5 points.

Full references: `../4_Sources/references_v3.md`. Parameter provenance: `../4_Sources/parameter_sources_v3.csv`.

---

## 8. Simulation results

1,000 simulated NUS students, 18-week semester, median. Index 0–100, higher is better.

| Scenario | Physical, semester | Physical, finals | Mental, semester | Mental, finals | Cooking h/week |
|---|---|---|---|---|---|
| S1 No congee + bad habits (caffeine, cigarettes, alcohol, junk food) | 45 | 35 | 48 | 42 | 0 |
| S2 No congee + healthy lifestyle | 67 | 56 | 56 | 49 | 0 |
| S3 Congee once a week (1 batch = 2 servings) | 69 | 60 | 59 | 53 | 0.9 |
| S4 Congee every day (7 servings = 3.5 batches) | 71 | 62 | 61 | 55 | 2.7 |

- **The healthy lifestyle is the biggest single step** (S1 → S2): +20 physical and +7 mental at finals. Bad habits damage sleep (finals sleep quality 21 vs 57) and the Spleen (44 vs 61) through R8 and STB-R.
- **Congee adds to a healthy lifestyle; it does not replace one.** Weekly congee adds +3.9 physical and +3.7 mental at finals (SMD 0.59 and 0.35 vs S2). Daily congee adds +6.4 and +5.4 (SMD 0.96 and 0.51).
- **Diminishing returns.** Daily use means 3.5× the servings and 3× the cooking time, but only about 1.5–1.6× the benefit of weekly use. The ingredient dose-response saturates, the recovery-break and mindfulness effects saturate, and daily cookers skip more under exam stress: adherence about 63% vs 73% of planned servings, through the workload brake B3.
- **Cooking and eating both matter.** For daily congee, the cooking paths alone (mindfulness, recovery break, completed task, with the ingredient effect set to zero) add +2.9 mental and +2.6 physical at finals. The ingredient paths alone (yam, lotus seed, red date, with the cooking paths switched off) add +2.7 mental and +4.4 physical. So about half of the mental benefit comes from the act of cooking, while the physical benefit leans on the ingredients.
- **Typical student check (no congee, typical habits):** 52% elevated stress in weeks 11–14 (NUS OSA 2024: 53%); mean wellbeing 54.1 (Health@NUS WHO-5: 54.9); 37% poor wellbeing (37.7%).

These results come from the model's assumptions. Every simulated student does better with congee because, apart from time cost, the model has no harmful path from congee. Potency is sampled from zero (no ingredient effect) to the full assumed effect.

---

## 9. Assumptions and limitations

- TCM constructs (Liver qi, Spleen function, Heart blood, shen, constitution) are functional concepts measured through proxies. Link strengths come from judgement plus published effect-size bounds; they are not measured on NUS students.
- The Liver, Heart-blood, circadian, Baduanjin and constitution links rest on small or mostly Chinese-language trials and cross-sectional surveys.
- The physical wellbeing index is not calibrated to data; only the mental index (WHO-5-like) and stress are calibrated.
- S3 and S4 keep the healthy lifestyle of S2, so each step changes one thing. Congee on top of bad habits was not simulated; it can be added by setting the lifestyle switch in Stella.
- The recipe is assumed to suit a Spleen-qi / Heart–Spleen deficiency pattern. People with damp-heat, or with diabetes (red dates and rice are high in sugar), need advice first. The model is not medical advice.

# Model v3 (TCM holistic): congee, cooking workload, mindfulness, Liver–Spleen–Heart, circadian rhythm, constitution

## Folders

- **1_CLD**
  - `congee_cld_v3_20var.png` / `.svg`: **20-variable CLD for IE2141 submission** (56 links, 20 named loops; planned frequency and constitution shown as parameter notes)
  - `congee_cld_v3_holistic.png` / `.svg`: full causal loop diagram, 27 variables, 63 links + 2 moderators, 19 named loops
  - `CLD_v3_holistic.md`: new/modified nodes, new links, new loops (R/B), rationale, constitution switch, evidence, results
  - `congee_cld_v2.png`: the earlier version (cooking workload and mindfulness only, before the holistic revision), for comparison
- **2_SFD_Stella**
  - `congee_model_v3.stmx`: the stock-and-flow model for **Stella Architect / Stella Professional** (XMILE). 12 stocks, 17 flows, 29 converters, 47 ghosts, 103 connectors, 7 sectors
  - `congee_sfd_v3.png`: picture of the same diagram in Stella's visual style
- **3_Simulation_Charts**
  - `fig1_line_wellbeing_v3.png`: line graph of physical and mental wellbeing by week, four scenarios
  - `fig2_bar_wellbeing_v3.png`: bar graph of semester-average and finals-week wellbeing, four scenarios
  - `fig3_BOTG_v3.png`: behaviour-over-time graphs (BOTG) of 16 model variables, four scenarios
  - `fig4_constitution_v3.png`: balanced vs Yin- vs Yang-deficient students
  - `summary_v3.json`, `weekly_results_v3.csv`: numbers behind the charts (median, 10th and 90th percentile)
- **4_Sources**: `references_v3.md` (new references), `parameter_sources_v3.csv` (where each new parameter comes from)
- **code**: Python. One equation list (`model_v3.py`) drives both the simulation and the Stella file.

## Scenarios

| Code | Scenario | Congee | Lifestyle |
|---|---|---|---|
| 1 | No congee + bad habits | none | caffeine, cigarettes, alcohol, junk food (high propensity) |
| 2 | No congee + healthy lifestyle | none | healthy |
| 3 | Congee once a week | 1 batch = 2 servings/week | healthy |
| 4 | Congee every day | 7 servings = 3.5 batches/week | healthy |
| 0 | Typical NUS student (calibration only) | none | typical |

Scenarios 3 and 4 keep the healthy lifestyle of scenario 2, so each step changes one thing.

## Running the Stella model

1. Open `2_SFD_Stella/congee_model_v3.stmx` in Stella Architect.
2. The run goes from week −8 to 18 with DT = 1/7 week (one day), Euler. Weeks −8 to 0 are a pre-semester holiday with no congee, so each scenario starts the semester from its own steady state.
3. Set the converter **Scenario** to 1, 2, 3 or 4, and **Constitution** to 0, 1 or 2. To compare all four scenarios in one graph, use *Sensitivity Analysis* (ad hoc values 1, 2, 3, 4 for Scenario) and add a graph of Physical Wellbeing, Mental Wellbeing or any stock.
4. Stella's own graph pads replace the Python charts; the Python charts add the 1,000-student spread.

The `.stmx` was generated from the Python equations. Read with PySD, it reproduces the Python model exactly: zero difference for all 4 scenarios, the reference run and all 3 constitutions (`code/validate_stella.py`). It has not been opened in Stella itself here; if Stella shows a "?" on any element, open its equation once and press OK.

## Re-running the Python version

From `code`:

```bash
python calibrate_v3.py
```

```bash
python run_mc_v3.py
```

```bash
python plot_v3.py
```

```bash
python sfd_v3.py
```

```bash
python draw_cld_v3.py
```

`python cld_v3.py` and `python cld_v3_20.py` print the loop audits; `python draw_cld_v3_20.py` redraws the 20-variable CLD. `validate_stella.py` needs `pip install pysd`.

Illustrative output of a conceptual model, not a clinical prediction.

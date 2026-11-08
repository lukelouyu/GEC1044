# Model Simulation — GEC1044 / IE2141 congee CLD and semester simulation

> **Latest version: `05_Model_v3_holistic/`** — TCM holistic CLD (Liver–Spleen–Heart, qi & blood, circadian rhythm, TCM practice, body awareness, constitution), cooking workload and mindfulness of cooking, a Stella Architect model (`.stmx`), and line / bar / BOTG charts for four scenarios (bad habits, healthy lifestyle, congee weekly, congee daily). See its README. Folders 01–04 below are v1 and are kept unchanged.

## Folders (v1)

- **01_CLD** — causal loop diagram and write-up
  - `CLD_analysis.md` — variable dictionary, loop walk-throughs, coupling, Shifting the Burden, leverage points, limitations
  - `congee_cld.mmd` / `.png` — main CLD (18 variables, 28 links), Mermaid source + rendered image
  - `congee_stb.mmd` / `.png` — Shifting the Burden overlay
- **02_Simulation** — results of the NUS-calibrated stock-and-flow simulation (1,000 simulated students, 18 weeks)
  - `fig1_wellbeing_semester.png` — study hours and physical/mental wellbeing by week, four scenarios
  - `fig2_mechanisms.png` — cooking frequency, quick-relief use, rumination, sleep
  - `fig3_effect_size_benchmarks.png` — simulated effect sizes vs published programmes
  - `fig4_model_vs_nus_data.png` — no-congee scenario vs NUS survey data (calibration and validation)
  - `weekly_wellbeing.csv` — weekly median and 10th–90th percentile per scenario
  - `summary.json`, `calibration.json` — summary metrics and fitted parameters
- **03_Sources**
  - `parameter_sources.csv` — every parameter, its source, and how the source was used
  - `references.md` — APA 7th reference list († = check primary source before submission)
- **04_Code** — Python (numpy, networkx, matplotlib)
  - `cld_model.py` — CLD edge list and loop audit; `make_mermaid.py` — generates the .mmd files
  - `sim.py` — simulation model; `calibrate.py` — fits to NUS data; `run_mc.py` — Monte Carlo; `plot.py` — figures

## Re-running

From `04_Code`: `python calibrate.py` → `python run_mc.py` → `python plot.py` (writes outputs to the current folder). `python cld_model.py` prints the loop audit.

## Scenarios

S0 no congee (quick relief only) · S1 congee routine · S2 congee + decision rules (fixed batch slots, simmer-as-pause, fatigue trigger, quick-relief cap) · S3 double ingredient dose (saturating dose-response).

Illustrative output of a conceptual model, not a clinical prediction.

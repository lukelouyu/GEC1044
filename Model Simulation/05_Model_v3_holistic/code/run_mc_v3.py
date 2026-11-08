"""Monte Carlo: 1,000 simulated NUS students x 4 scenarios (+ the calibration reference and the 3 constitutions).
Run: python run_mc_v3.py  -> mc_v3.npz, ../3_Simulation_Charts/weekly_results_v3.csv, ../3_Simulation_Charts/summary_v3.json
"""
import csv
import json
import numpy as np
import model_v3 as m

N = 1000
OUT = "../3_Simulation_Charts/"
REC = ["Physical_Wellbeing", "Mental_Wellbeing", "Perceived_Stress", "Rumination", "Liver_Qi_Stagnation",
       "Spleen_Function", "Qi_Blood_Generation", "Heart_Blood_Malnourishment", "Calm_Shen", "Sleep_Quality",
       "Fatigue", "Body_Awareness", "Mindfulness", "Unhealthy_Habits", "Self_Care_Engagement", "TCM_Practice",
       "Servings_Eaten", "Cooking_Workload", "Recovery_Break", "Circadian_Disruption", "Adherence"]
cal = json.load(open("calibration_v3.json"))
names = list(m.SCENARIOS)
rng = np.random.default_rng(2141)
p = m.sample_params(N, rng, cal)          # the same 1,000 students in every scenario

res = {}
for key, sc, const in ([(n, m.SCENARIOS[n], 0) for n in names] + [("REF", m.REFERENCE, 0)]
                       + [(f"{n}|C{c}", m.SCENARIOS[n], c) for n in names for c in (1, 2)]):
    o = m.run(dict(p, constitution=np.full(N, float(const))), sc, record=REC)
    res[key] = {k: m.weekly(o[k]) for k in REC}
np.savez_compressed("mc_v3.npz", **{f"{k}::{v}": arr for k, d in res.items() for v, arr in d.items()})

S1, S2, S3, S4 = names
FIN, SEM = [15, 16], list(range(17))          # zero-based weeks 16-17 (finals), weeks 1-17
win = lambda k, v, w: res[k][v][w].mean(axis=0)
med = lambda x: float(np.median(x))
summary = {"n_students": N, "calibration": {k: cal[k] for k in ("b0", "sd_resil", "s_AD_PAS", "k_int", "L_bad")},
           "scenarios": {}}
for n in names:
    d = {}
    for v in REC:
        d[v] = dict(week1=med(res[n][v][0]), semester_mean=med(win(n, v, SEM)), finals=med(win(n, v, FIN)),
                    week18=med(res[n][v][17]))
    summary["scenarios"][n] = d
for n in names[1:]:
    for v in ("Physical_Wellbeing", "Mental_Wellbeing"):
        a, b = win(n, v, FIN), win(S1, v, FIN)
        summary["scenarios"][n][v][f"finals_gain_vs_S1_points"] = float(a.mean() - b.mean())
for n in (S3, S4):
    for v in ("Physical_Wellbeing", "Mental_Wellbeing"):
        a, b = win(n, v, FIN), win(S2, v, FIN)
        summary["scenarios"][n][v]["finals_gain_vs_S2_points"] = float(a.mean() - b.mean())
        summary["scenarios"][n][v]["finals_SMD_vs_S2"] = float((a.mean() - b.mean()) / b.std())
        summary["scenarios"][n][v]["P(better than S2) finals"] = float((a > b).mean())
summary["P(S4 > S3) finals mental"] = float((win(S4, "Mental_Wellbeing", FIN) > win(S3, "Mental_Wellbeing", FIN)).mean())
summary["P(S4 > S3) finals physical"] = float((win(S4, "Physical_Wellbeing", FIN) > win(S3, "Physical_Wellbeing", FIN)).mean())
summary["cooking hours per week (median, semester)"] = {n: med(win(n, "Cooking_Workload", SEM)) for n in (S3, S4)}
summary["servings eaten per week (median, semester)"] = {n: med(win(n, "Servings_Eaten", SEM)) for n in (S3, S4)}
summary["constitution_finals"] = {
    n: {lab: {v: med(win(n if c == 0 else f"{n}|C{c}", v, FIN)) for v in ("Physical_Wellbeing", "Mental_Wellbeing",
                                                                           "Sleep_Quality", "Fatigue")}
        for c, (lab, _, _) in m.CONSTITUTION.items()} for n in names}
ref = res["REF"]
summary["NUS_checks_typical_student"] = dict(
    elevated_stress_wk11_14=dict(target=0.53, model=float((ref["Perceived_Stress"][10:14] >= 0.5).mean())),
    mean_stress_wk11_14=dict(target=0.454, model=float(ref["Perceived_Stress"][10:14].mean())),
    WHO5_mean=dict(target=54.9, model=float(ref["Mental_Wellbeing"][:17].mean())),
    poor_wellbeing_share=dict(target=0.377, model=float((ref["Mental_Wellbeing"][:17] <= 50).mean())),
    lifestyle_gap_S2_minus_S1=dict(target=8.66, model=float(win(S2, "Mental_Wellbeing", SEM).mean()
                                                              - win(S1, "Mental_Wellbeing", SEM).mean())),
)
json.dump(summary, open(OUT + "summary_v3.json", "w"), indent=1)

with open(OUT + "weekly_results_v3.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["week", "phase", "scenario", "variable", "median", "p10", "p90"])
    for n in names:
        for v in REC:
            for wk in range(18):
                x = res[n][v][wk]
                w.writerow([wk + 1, m.PHASE[wk + 1], n, v, round(med(x), 4), round(float(np.percentile(x, 10)), 4),
                            round(float(np.percentile(x, 90)), 4)])
print(json.dumps({n: {v: round(summary["scenarios"][n][v]["finals"], 2) for v in ("Physical_Wellbeing", "Mental_Wellbeing")}
                  for n in names}, indent=1))
print(json.dumps(summary["NUS_checks_typical_student"], indent=1))
print({k: v for k, v in summary.items() if k.startswith("P(") or k.startswith("cooking") or k.startswith("servings")})
for n in (S3, S4):
    print(n, {v: {k: round(x, 3) for k, x in summary["scenarios"][n][v].items() if "S2" in k} for v in ("Physical_Wellbeing", "Mental_Wellbeing")})

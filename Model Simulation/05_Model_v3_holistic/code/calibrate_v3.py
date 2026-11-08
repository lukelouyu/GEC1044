"""Calibration of the v3 (holistic) model. Run from this folder: python calibrate_v3.py  -> calibration_v3.json

Step 1  Typical NUS student (Scenario 0: typical lifestyle, no congee) fitted to NUS survey data, as in v1:
        T_a  NUS OSA Student Wellbeing Pulse 2024: 53% elevated stress (PSS-4 >= 8) in weeks 11-14
        T_b  NUS OSA 2024: mean PSS-4 = 7.27/16 = 0.454 in weeks 11-14
        T_c  Health@NUS: WHO-5 mean ~54.9 over the semester
        T_d  Health@NUS: 37.7% poor well-being (WHO-5 <= 50)
        Free parameters: b0 (stress intercept), sd_resil (spread between students), s_AD_PAS (stress per unit of workload)
Step 2  Lifestyle gap. The habit stock acts through diet and sleep, so the S2 (healthy) minus S1 (bad habits) gap on
        the semester-mean mental index is set to the sum of the two matching Health@NUS associations with WHO-5:
        limited unhealthy food +3.80 and adequate sleep +4.86 = 8.66 points. (Health@NUS 4-6 healthy behaviours,
        +10.46, is an upper bound: it also counts movement behaviours the model leaves out.)
Step 3  Congee effect bound. k_int (strength of the cooking -> mindfulness and cooking -> activation links) is the
        largest value that keeps the daily-congee effect (S4 vs S2, finals weeks, mental index) at or below the
        effect of formal mindfulness programmes on stress in non-clinical samples (g = 0.52; Querstret et al. 2020).
"""
import json
import numpy as np
import model_v3 as m

N = 600
W_SUB = [10, 11, 12, 13]      # zero-based weeks 11-14
W_SEM = list(range(17))       # weeks 1-17
W_FIN = [15, 16]              # weeks 16-17
WHO5 = 52.85 * 0.568 + 57.64 * 0.432
GAP_TARGET = 3.80 + 4.86
S1, S2, S3, S4 = list(m.SCENARIOS)


def runset(cal, sc, seed=2141, n=N):
    rng = np.random.default_rng(seed)
    p = m.sample_params(n, rng, cal)
    o = m.run(p, sc, record=("Mental_Wellbeing", "Physical_Wellbeing", "Perceived_Stress"))
    return dict(me=m.weekly(o["Mental_Wellbeing"]), ph=m.weekly(o["Physical_Wellbeing"]),
                PAS=m.weekly(o["Perceived_Stress"]))


def targets(r):
    return dict(stress_sub=float((r["PAS"][W_SUB] >= 0.5).mean()),
                meanPAS_sub=float(r["PAS"][W_SUB].mean()),
                mean_mental=float(r["me"][W_SEM].mean()),
                poor_mental=float((r["me"][W_SEM] <= 50).mean()),
                mental_lt50_sub=float((r["me"][W_SUB] < 50).mean()))


cal = dict(b0=0.28, sd_resil=0.2, s_AD_PAS=0.42, k_int=0.6, L_bad=2.5)

# ---------------- step 1 ----------------
best = None
for s_ad in [0.28, 0.35, 0.42, 0.49, 0.56, 0.63, 0.70]:
    for b0 in np.arange(0.0, 0.41, 0.02):
        for sd in [0.12, 0.16, 0.20, 0.24, 0.28, 0.32]:
            c = dict(cal, b0=float(b0), sd_resil=sd, s_AD_PAS=s_ad)
            t = targets(runset(c, m.REFERENCE))
            err = (abs(t["stress_sub"] - 0.53) / 0.53 + abs(t["meanPAS_sub"] - 0.4544) / 0.4544
                   + abs(t["mean_mental"] - WHO5) / WHO5 + abs(t["poor_mental"] - 0.377) / 0.377)
            if best is None or err < best[0]:
                best = (err, c, t)
_, cal, fit = best
cal["b0"] = round(cal["b0"], 2)
print("step 1:", {k: cal[k] for k in ("b0", "sd_resil", "s_AD_PAS")})
for k, v in fit.items():
    print(f"   {k}: {v:.3f}")

# ---------------- step 2 ----------------
gaps = []
for L in np.arange(1.0, 10.01, 0.25):
    c = dict(cal, L_bad=float(L))
    g = runset(c, m.SCENARIOS[S2])["me"][W_SEM].mean() - runset(c, m.SCENARIOS[S1])["me"][W_SEM].mean()
    gaps.append((float(L), float(g)))
L_best, gap = min(gaps, key=lambda x: abs(x[1] - GAP_TARGET))
cal["L_bad"] = L_best
print(f"step 2: L_bad = {L_best}  (S2 - S1 mental gap = {gap:.2f}, target {GAP_TARGET})")

# ---------------- step 3 ----------------
smd_table = []
for k in np.arange(0.0, 1.01, 0.05):
    c = dict(cal, k_int=float(k))
    r2, r3, r4 = (runset(c, m.SCENARIOS[s]) for s in (S2, S3, S4))
    f = lambda r: r["me"][W_FIN].mean(0)
    sd2 = f(r2).std()
    smd_table.append((round(float(k), 2), float((f(r3).mean() - f(r2).mean()) / sd2),
                      float((f(r4).mean() - f(r2).mean()) / sd2), float(f(r4).mean() - f(r2).mean())))
    print("   k_int=%.2f  SMD weekly=%.2f  daily=%.2f  (daily - S2 = %.1f points)" % smd_table[-1])
ok = [row for row in smd_table if row[2] <= 0.52]
cal["k_int"] = max(ok, key=lambda row: row[0])[0] if ok else 0.0
print("step 3: k_int =", cal["k_int"])

json.dump(dict(cal, fit=fit, who5_target=WHO5, lifestyle_gap_target=GAP_TARGET, lifestyle_gap_model=gap, lifestyle_gap_table=gaps, smd_table=smd_table),
          open("calibration_v3.json", "w"), indent=1)

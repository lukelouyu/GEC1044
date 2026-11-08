import numpy as np, json, csv, sim

N = 1000
rng = np.random.default_rng(2141)
cal = json.load(open("calibration.json"))
p = sim.sample_params_v2(N, rng, b0=cal["b0"], sd_resil=cal["sd_resil"], k_int=cal["k_int"])
p["s_AD_PAS"] = p["s_AD_PAS"] * cal["m_AD"]
init = sim.burn_in(p)

res = {}
for name, sc in sim.SCENARIOS.items():
    o, _ = sim.run(p, init={k: v.copy() for k, v in init.items()}, **sc)
    ph, me = sim.indices(o)
    res[name] = dict(phys=sim.weekly(ph), ment=sim.weekly(me), CR=sim.weekly(o["CR"]),
                     QR=sim.weekly(o["QR"]), SL=sim.weekly(o["SL"]), PAS=sim.weekly(o["PAS"]),
                     RU=sim.weekly(o["RU"]), SQ=sim.weekly(o["SQ"]))
np.save("mc_results.npy", res, allow_pickle=True)

names = list(sim.SCENARIOS)
S0, S1, S2, S3 = names
q = lambda x, a: np.percentile(x, a, axis=-1)

# weekly table (median, P10, P90)
with open("weekly_wellbeing.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["week", "phase", "academic_demand"] + [f"{n.split()[0]}_{m}_{s}" for n in names
                for m in ("physical", "mental") for s in ("median", "p10", "p90")])
    dem = sim.demand_profile()
    for wk in range(18):
        row = [wk + 1, sim.PHASE[wk + 1], dem[wk + 1]]
        for n in names:
            for m in ("phys", "ment"):
                x = res[n][m][wk]
                row += [round(float(np.median(x)), 1), round(float(q(x, 10)), 1), round(float(q(x, 90)), 1)]
        w.writerow(row)

# summary metrics
def win(n, m, weeks):  # mean over a set of weeks (1-based), per run
    return res[n][m][[w - 1 for w in weeks]].mean(axis=0)

summary = {}
for n in names:
    d = {}
    for m in ("phys", "ment"):
        d[m] = dict(
            wk1=float(np.median(res[n][m][0])),
            midterms=float(np.median(win(n, m, [8, 9]))),
            submissions=float(np.median(win(n, m, [11, 12, 13, 14]))),
            finals=float(np.median(win(n, m, [16, 17]))),
            wk18=float(np.median(res[n][m][17])),
            trough=float(np.median(res[n][m].min(axis=0))),
        )
    d["cooking_batches_per_week_finals"] = float(np.median(win(n, "CR", [16, 17]))) * 4
    d["cooking_batches_per_week_wk1_6"] = float(np.median(win(n, "CR", range(1, 7)))) * 4
    d["quick_relief_finals"] = float(np.median(win(n, "QR", [16, 17])))
    summary[n] = d

fin = lambda n, m: win(n, m, [16, 17])
for n in names[1:]:
    for m in ("phys", "ment"):
        summary[n][f"SMD_vs_S0_finals_{m}"] = float((fin(n, m).mean() - fin(S0, m).mean()) / fin(S0, m).std())
summary["checks"] = dict(
    NUS_OSA_elevated_stress_wk11_14=dict(target=0.53, model=float((res[S0]["PAS"][10:14] >= 0.5).mean())),
    NUS_OSA_mean_PSS4_wk11_14=dict(target=7.27 / 16, model=float(res[S0]["PAS"][10:14].mean())),
    HealthNUS_WHO5_mean=dict(target=52.85 * 0.568 + 57.64 * 0.432, model=float(res[S0]["ment"][:17].mean())),
    HealthNUS_poor_wellbeing=dict(target=0.377, model=float((res[S0]["ment"][:17] <= 50).mean())),
    NUS_OSA_PHQ4_risk_vs_mental_lt50_wk11_14=dict(target=0.32, model=float((res[S0]["ment"][10:14] < 50).mean())),
)
summary["S2_minus_S0_finals_mental_points"] = float(fin(S2, "ment").mean() - fin(S0, "ment").mean())
cmp = {
    "P(S1>S0) finals phys": float((fin(S1, "phys") > fin(S0, "phys")).mean()),
    "P(S1>S0) finals ment": float((fin(S1, "ment") > fin(S0, "ment")).mean()),
    "P(S2>S1) finals phys": float((fin(S2, "phys") > fin(S1, "phys")).mean()),
    "P(S2>S1) finals ment": float((fin(S2, "ment") > fin(S1, "ment")).mean()),
    "P(S3>S2) finals phys": float((fin(S3, "phys") > fin(S2, "phys")).mean()),
    "P(S3>S2) finals ment": float((fin(S3, "ment") > fin(S2, "ment")).mean()),
}
# vulnerable students: stress strongly suppresses self-care (top quartile of s_PAS_SE)
vul = p["s_PAS_SE"] >= np.percentile(p["s_PAS_SE"], 75)
for n in names:
    cmp[f"vulnerable finals ment median {n.split()[0]}"] = float(np.median(fin(n, "ment")[vul]))
    cmp[f"vulnerable finals phys median {n.split()[0]}"] = float(np.median(fin(n, "phys")[vul]))
    cmp[f"vulnerable finals CR batches {n.split()[0]}"] = float(np.median(win(n, "CR", [16, 17])[vul])) * 4
# which parameters drive the S1 finals mental-gain over S0 (rank correlation)
gain = fin(S1, "ment") - fin(S0, "ment")
rank = lambda x: np.argsort(np.argsort(x))
corr = {k: float(np.corrcoef(rank(p[k]), rank(gain))[0, 1]) for k in p if np.ptp(p[k]) > 0}
cmp["top drivers of S1 gain (spearman)"] = sorted(corr.items(), key=lambda kv: -abs(kv[1]))[:6]

json.dump(dict(summary=summary, compare=cmp), open("summary.json", "w"), indent=1)
print(json.dumps(dict(summary=summary, compare=cmp), indent=1))

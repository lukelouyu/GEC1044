import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sim

res = np.load("mc_results.npy", allow_pickle=True).item()
names = list(sim.SCENARIOS)
COL = {names[0]: "#7d7c78", names[1]: "#2a78d6", names[2]: "#eb6834", names[3]: "#1baf7a"}
LS = {names[0]: "-", names[1]: "-", names[2]: "-", names[3]: (0, (5, 3))}
SHORT = {names[0]: "S0 No congee", names[1]: "S1 Congee", names[2]: "S2 Congee + rules",
         names[3]: "S3 Double dose\n(saturating response)"}
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
wk = np.arange(1, 19)
dem = sim.demand_profile()

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": "#b9b8b2",
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.spines.top": False, "axes.spines.right": False})

BANDS = [(8, 9, "Midterms"), (11, 14, "Submissions"), (16, 17, "Finals")]
RECESS = [(7, 7, "Recess"), (15, 15, "Recess")]


def shade(ax, label=False, short=False):
    for a, b, t in BANDS:
        ax.axvspan(a - 0.5, b + 0.5, color="#f3e3dc", zorder=0, lw=0)
        if label:
            ax.text((a + b) / 2, 1.02, {"Midterms": "Mid", "Submissions": "Subm.", "Finals": "Fin"}[t] if short else t, transform=ax.get_xaxis_transform(), ha="center",
                    va="bottom", fontsize=9, color=INK2)
    for a, b, t in RECESS:
        ax.axvspan(a - 0.5, b + 0.5, color="#e6eef5", zorder=0, lw=0)
        if label:
            ax.text(a, 1.02, "R" if short else t, transform=ax.get_xaxis_transform(), ha="center", va="bottom",
                    fontsize=9, color=INK2)


def lines(ax, key, which, scale=1.0, band=True, labels=True, nudge=None, band_for=None):
    ends = []
    for n in which:
        x = res[n][key] * scale
        med = np.median(x, axis=1)
        if band and (band_for is None or n in band_for):
            ax.fill_between(wk, np.percentile(x, 10, 1), np.percentile(x, 90, 1),
                            color=COL[n], alpha=0.10, lw=0)
        ax.plot(wk, med, color=COL[n], lw=2, ls=LS[n], marker="o", ms=3.5, solid_capstyle="round")
        ends.append([n, med[-1]])
    if labels:  # direct labels, de-collided
        ends.sort(key=lambda e: e[1])
        gap = nudge or (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.075
        for i in range(1, len(ends)):
            ends[i][1] = max(ends[i][1], ends[i - 1][1] + gap)
        for n, y in ends:
            ax.text(18.4, y, SHORT[n], color=INK, fontsize=8.5, va="center")
    ax.set_xlim(0.5, 18.5)
    ax.set_xticks(wk)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)


# ---------------- Figure 1: wellbeing over the semester ----------------
fig, axs = plt.subplots(3, 1, figsize=(10, 9.2), sharex=True,
                        gridspec_kw=dict(height_ratios=[0.8, 2, 2], hspace=0.28))
ax = axs[0]
shade(ax, label=True)
hrs = sim.study_hours(20)
ax.bar(wk, [hrs[w] for w in wk], width=0.7, color="#9b9a95", edgecolor="none")
ax.set_ylim(0, 90); ax.set_yticks([0, 25, 50, 75])
ax.axhline(50, color="#52514e", lw=0.8, ls=(0, (3, 3)))
ax.text(0.6, 52, "NUS norm: 20 units × 2.5 h = 50 h/wk", fontsize=8, color=INK2, va="bottom")
ax.set_ylabel("Expected study\nhours/week")
ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)

for ax, key, title in [(axs[1], "phys", "Physical wellbeing index"), (axs[2], "ment", "Mental wellbeing index")]:
    shade(ax)
    ax.set_ylim(20, 85)
    lines(ax, key, names, band_for=[names[0], names[2]])
    ax.set_ylabel(f"{title}\n(0–100, higher = better)")
axs[2].set_xlabel("Semester week")
fig.suptitle("Simulated wellbeing of a time-constrained NUS student over an 18-week semester",
             x=0.06, ha="left", fontsize=13, color=INK, y=0.985)
fig.text(0.06, 0.925, "Lines = median of 1,000 simulated students; calibrated to NUS survey, Singapore and TCM sources (parameter_sources.csv).\n"
         "Bands = 10th–90th percentile for S0 and S2. Illustrative output of a conceptual model, not a clinical prediction.",
         fontsize=9, color=INK2, ha="left")
fig.subplots_adjust(left=0.1, right=0.82, top=0.86, bottom=0.06)
fig.savefig("fig1_wellbeing_semester.png", dpi=200)

# ---------------- Figure 2: why it happens (mechanisms) ----------------
three = names[:3]
fig, axs = plt.subplots(2, 2, figsize=(11, 7), sharex=True, gridspec_kw=dict(hspace=0.35, wspace=0.42))
spec = [("CR", 4.0, "Congee batches cooked per week", (0, 2.2)),
        ("QR", 100, "Quick-relief use (index 0–100, lower = better)", (20, 75)),
        ("RU", 100, "Rumination (index 0–100, lower = better)", (0, 90)),
        ("SL", 100, "Sleep quality (index 0–100)", (25, 75))]
for ax, (k, sc, t, yl) in zip(axs.ravel(), spec):
    shade(ax, label=(ax in axs[0]), short=True)
    ax.set_ylim(*yl)
    lines(ax, k, three, scale=sc)
    ax.set_title(t, loc="left", fontsize=10.5, color=INK, pad=16)
for ax in axs[1]:
    ax.set_xlabel("Semester week")
fig.suptitle("Mechanisms behind the wellbeing curves (median of 1,000 runs, 10th–90th percentile bands)\nR = recess · Mid = midterms · Subm. = submissions · Fin = finals",
             x=0.06, ha="left", fontsize=12.5, color=INK, y=0.985)
fig.subplots_adjust(left=0.06, right=0.88, top=0.84, bottom=0.08)
fig.savefig("fig2_mechanisms.png", dpi=200)
print("saved")

# ---------------- Figure 3: simulated effect sizes vs published benchmarks ----------------
import json
summ = json.load(open("summary.json"))["summary"]
fig, ax = plt.subplots(figsize=(9, 4.2))
rows = [("S1 Congee (simulated)", summ[names[1]]["SMD_vs_S0_finals_ment"], COL[names[1]]),
        ("S2 Congee + rules (simulated)", summ[names[2]]["SMD_vs_S0_finals_ment"], COL[names[2]]),
        ("S3 Double dose (simulated)", summ[names[3]]["SMD_vs_S0_finals_ment"], COL[names[3]]),
        ("MBSR/MBCT on stress, nonclinical\n(Querstret et al. 2020)", 0.52, "#9b9a95"),
        ("Behavioural activation on depression\n(Ekers et al. 2014)", 0.74, "#9b9a95")]
y = np.arange(len(rows))[::-1]
for yi, (lab, v, c) in zip(y, rows):
    ax.barh(yi, v, color=c, height=0.55)
    ax.text(v + 0.01, yi, f"{v:.2f}", va="center", fontsize=9.5, color=INK)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=9.5)
ax.set_xlim(0, 0.9); ax.set_xlabel("Standardised effect on mental wellbeing (|SMD| vs no congee, finals weeks)")
ax.grid(axis="x", color=GRID, lw=0.8); ax.set_axisbelow(True)
fig.suptitle("Simulated effects are kept at or below published effects of structured programmes",
             x=0.02, ha="left", fontsize=11.5, color=INK)
fig.subplots_adjust(left=0.36, right=0.97, top=0.88, bottom=0.14)
fig.savefig("fig3_effect_size_benchmarks.png", dpi=200)
print("saved fig3")

# ---------------- Figure 4: model vs NUS survey data (calibration and validation) ----------------
chk = json.load(open("summary.json"))["summary"]["checks"]
rows = [("Elevated stress, late-semester weeks\nNUS OSA 2024: PSS-4 >= 8", "NUS_OSA_elevated_stress_wk11_14", 100, "Fitted"),
        ("Poor well-being, semester average\nHealth@NUS: WHO-5 <= 50", "HealthNUS_poor_wellbeing", 100, "Fitted"),
        ("Mean well-being, semester average\nHealth@NUS: WHO-5 mean", "HealthNUS_WHO5_mean", 1, "Fitted"),
        ("Mean stress, late-semester weeks\nNUS OSA 2024: PSS-4 mean / 16", "NUS_OSA_mean_PSS4_wk11_14", 100, "Fitted (partial)"),
        ("Anxiety/depression risk, late semester\nNUS OSA 2024: PHQ-4 >= 6 (validation only)", "NUS_OSA_PHQ4_risk_vs_mental_lt50_wk11_14", 100, "Not fitted")]
fig, ax = plt.subplots(figsize=(9.5, 5))
y = np.arange(len(rows))[::-1]
for yi, (lab, key, sc, status) in zip(y, rows):
    t, m = chk[key]["target"] * sc, chk[key]["model"] * sc
    ax.barh(yi + 0.18, t, height=0.34, color="#9b9a95")
    ax.barh(yi - 0.18, m, height=0.34, color=COL[names[0]] if False else "#2a78d6")
    ax.text(t + 0.8, yi + 0.18, f"NUS data {t:.1f}", va="center", fontsize=8.5, color=INK)
    ax.text(m + 0.8, yi - 0.18, f"model {m:.1f}  ({status})", va="center", fontsize=8.5, color=INK)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=9)
ax.set_xlim(0, 85); ax.set_xlabel("Percent of students, or mean score on a 0–100 scale")
ax.grid(axis="x", color=GRID, lw=0.8); ax.set_axisbelow(True)
fig.suptitle("No-congee scenario (S0) compared with NUS student survey data", x=0.02, ha="left", fontsize=11.5, color=INK)
fig.subplots_adjust(left=0.36, right=0.97, top=0.9, bottom=0.12)
fig.savefig("fig4_model_vs_nus_data.png", dpi=200)
print("saved fig4")

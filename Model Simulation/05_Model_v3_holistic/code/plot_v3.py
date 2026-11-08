"""Charts for the four scenarios. Run after run_mc_v3.py: python plot_v3.py -> ../3_Simulation_Charts/*.png
  fig1_line_wellbeing_v3.png   line graph: physical and mental wellbeing week by week (median, 10th-90th percentile)
  fig2_bar_wellbeing_v3.png    bar graph: semester average and finals-week wellbeing per scenario
  fig3_BOTG_v3.png             behaviour-over-time graphs (BOTG) of 16 model variables, all four scenarios
  fig4_constitution_v3.png     constitution switch: balanced vs Yin- vs Yang-deficient students at finals
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import model_v3 as m

OUT = "../3_Simulation_Charts/"
plt.rcParams.update({"font.family": ["DejaVu Sans", "Microsoft YaHei"], "font.size": 10,
                     "axes.edgecolor": "#b9b8b2", "axes.labelcolor": "#52514e", "xtick.color": "#52514e",
                     "ytick.color": "#52514e", "axes.spines.top": False, "axes.spines.right": False})
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
names = list(m.SCENARIOS)
COL = dict(zip(names, ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]))      # validated categorical slots 1-4
SHORT = dict(zip(names, ["S1 No congee + bad habits", "S2 No congee + healthy lifestyle",
                         "S3 Congee once a week", "S4 Congee every day"]))
TINY = dict(zip(names, ["S1 bad habits", "S2 healthy", "S3 weekly", "S4 daily"]))
z = np.load("mc_v3.npz")
res = lambda key, v: z[f"{key}::{v}"]
summ = json.load(open(OUT + "summary_v3.json"))
wk = np.arange(1, 19)
BANDS = [(8, 9, "Midterms"), (11, 14, "Submissions"), (16, 17, "Finals")]
RECESS = [(7, 7, "Recess"), (15, 15, "Reading")]
NOTE = ("Median of 1,000 simulated NUS students (same students in every scenario), calibrated to NUS OSA 2024 and "
        "Health@NUS survey data.\nIllustrative output of a conceptual model, not a clinical prediction.")


def shade(ax, label=False, short=False):
    for a, b, t in BANDS:
        ax.axvspan(a - 0.5, b + 0.5, color="#f3e3dc", zorder=0, lw=0)
        if label:
            ax.text((a + b) / 2, 1.02, {"Midterms": "Mid", "Submissions": "Subm.", "Finals": "Fin"}[t] if short else t,
                    transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=8.5, color=INK2)
    for a, b, t in RECESS:
        ax.axvspan(a - 0.5, b + 0.5, color="#e6eef5", zorder=0, lw=0)
        if label:
            ax.text(a, 1.02, "R" if short else t, transform=ax.get_xaxis_transform(), ha="center", va="bottom",
                    fontsize=8.5, color=INK2)


def lines(ax, v, scale=1.0, band_for=(), labels=True, fmt="{:.0f}", lw=2):
    ends = []
    for n in names:
        x = res(n, v) * scale
        md = np.median(x, axis=1)
        if n in band_for:
            ax.fill_between(wk, np.percentile(x, 10, 1), np.percentile(x, 90, 1), color=COL[n], alpha=0.12, lw=0)
        ax.plot(wk, md, color=COL[n], lw=lw, marker="o", ms=3.2, solid_capstyle="round", zorder=3)
        ends.append([n, md[-1]])
    if labels:
        lo, hi = ax.get_ylim()
        gap = (hi - lo) * 0.075
        ends.sort(key=lambda e: e[1])
        for i in range(1, len(ends)):
            ends[i][1] = max(ends[i][1], ends[i - 1][1] + gap)
        for n, y in ends:
            ax.text(18.45, y, SHORT[n], color=INK, fontsize=8.5, va="center")
    ax.set_xlim(0.5, 18.5)
    ax.set_xticks(wk)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)


# ------------------------------------------------------------- Figure 1: line graph
fig, axs = plt.subplots(3, 1, figsize=(11, 10), sharex=True, gridspec_kw=dict(height_ratios=[0.75, 2, 2], hspace=0.25))
ax = axs[0]
shade(ax, label=True)
hrs = [v * m.WAKING_H for v in m.semester_demand()]
ax.bar(wk, hrs, width=0.68, color="#9b9a95", edgecolor="none")
ax.axhline(50, color=INK2, lw=0.8, ls=(0, (3, 3)))
ax.text(0.6, 52, "NUS norm: 20 units x 2.5 h = 50 h/week", fontsize=8, color=INK2, va="bottom")
ax.set_ylim(0, 92)
ax.set_yticks([0, 25, 50, 75])
ax.set_ylabel("Study hours\nper week")
ax.grid(axis="y", color=GRID, lw=0.8)
ax.set_axisbelow(True)
for ax, v, t in [(axs[1], "Physical_Wellbeing", "Physical wellbeing"), (axs[2], "Mental_Wellbeing", "Mental wellbeing")]:
    shade(ax)
    ax.set_ylim(20, 92)
    lines(ax, v, band_for=(names[0], names[3]))
    ax.set_ylabel(f"{t}\n(0-100, higher = better)")
axs[2].set_xlabel("Semester week")
fig.suptitle("Effect of the congee on wellbeing over an 18-week NUS semester: four scenarios",
             x=0.07, ha="left", fontsize=13.5, color=INK, y=0.985)
fig.text(0.07, 0.915, NOTE + "\nShaded bands = 10th-90th percentile for S1 and S4. S3 and S4 keep the healthy lifestyle of S2, "
         "so each step changes one thing.", fontsize=8.8, color=INK2, ha="left", va="center")
fig.subplots_adjust(left=0.1, right=0.78, top=0.845, bottom=0.06)
fig.savefig(OUT + "fig1_line_wellbeing_v3.png", dpi=200)
plt.close(fig)

# ------------------------------------------------------------- Figure 2: bar graph
FIN, SEM = [15, 16], list(range(17))
fig, axs = plt.subplots(1, 2, figsize=(12, 5.6), sharey=True, gridspec_kw=dict(wspace=0.08))
groups = [("Semester average\n(weeks 1-17)", SEM), ("Finals\n(weeks 16-17)", FIN)]
bw = 0.19
for ax, v, t in [(axs[0], "Physical_Wellbeing", "Physical wellbeing"), (axs[1], "Mental_Wellbeing", "Mental wellbeing")]:
    for gi, (glab, wks) in enumerate(groups):
        for si, n in enumerate(names):
            x = res(n, v)[wks].mean(axis=0)
            md, lo, hi = np.median(x), np.percentile(x, 25), np.percentile(x, 75)
            xpos = gi + (si - 1.5) * (bw + 0.02)
            ax.bar(xpos, md, width=bw, color=COL[n], edgecolor="none", zorder=2)
            ax.plot([xpos, xpos], [lo, hi], color=INK2, lw=1.1, zorder=3)
            ax.text(xpos, hi + 1.2, f"{md:.0f}", ha="center", va="bottom", fontsize=9, color=INK)
    ax.set_xticks([0, 1])
    ax.set_xticklabels([g[0] for g in groups], fontsize=10)
    ax.set_title(t + " (0-100)", loc="left", fontsize=11.5, color=INK)
    ax.set_ylim(0, 95)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
axs[0].set_ylabel("Median index (whiskers = 25th-75th percentile)")
handles = [plt.Rectangle((0, 0), 1, 1, color=COL[n]) for n in names]
fig.legend(handles, [SHORT[n] for n in names], loc="lower center", ncol=4, frameon=False, fontsize=9.5,
           bbox_to_anchor=(0.5, 0.0))
s = summ["scenarios"]
gain = (f"Finals gain from congee on top of a healthy lifestyle (S2): once a week +{s[names[2]]['Physical_Wellbeing']['finals_gain_vs_S2_points']:.1f} physical, "
        f"+{s[names[2]]['Mental_Wellbeing']['finals_gain_vs_S2_points']:.1f} mental; every day +{s[names[3]]['Physical_Wellbeing']['finals_gain_vs_S2_points']:.1f} physical, "
        f"+{s[names[3]]['Mental_Wellbeing']['finals_gain_vs_S2_points']:.1f} mental (3.5x the servings, diminishing returns).")
fig.suptitle("Bad habits vs healthy lifestyle vs congee once a week vs every day", x=0.07, ha="left", fontsize=13.5,
             color=INK, y=0.98)
fig.text(0.07, 0.87, gain + "\n" + NOTE, fontsize=8.6, color=INK2, ha="left", va="center")
fig.subplots_adjust(left=0.08, right=0.98, top=0.76, bottom=0.2)
fig.savefig(OUT + "fig2_bar_wellbeing_v3.png", dpi=200)
plt.close(fig)

# ------------------------------------------------------------- Figure 3: BOTG grid
PANELS = [  # variable, title, scale, ylim, note
    ("Perceived_Stress", "Perceived academic stress", 100, (0, 100), "lower = better"),
    ("Rumination", "Rumination", 100, (0, 100), "lower = better"),
    ("Liver_Qi_Stagnation", "Liver Qi Stagnation 肝气郁结", 100, (0, 100), "lower = better"),
    ("Spleen_Function", "Spleen Function (Spleen Qi)", 100, (0, 100), ""),
    ("Qi_Blood_Generation", "Qi & Blood Generation 气血生化", 100, (0, 100), ""),
    ("Heart_Blood_Malnourishment", "Heart Blood / Shen Malnourishment", 100, (0, 100), "lower = better"),
    ("Calm_Shen", "Calm Shen", 100, (0, 100), ""),
    ("Sleep_Quality", "Sleep quality", 100, (0, 100), ""),
    ("Fatigue", "Fatigue (true, unmasked)", 100, (0, 100), "lower = better"),
    ("Body_Awareness", "Body Awareness 身体觉察", 100, (0, 50), ""),
    ("Mindfulness", "Mindfulness", 100, (0, 60), ""),
    ("Unhealthy_Habits", "Unhealthy habits", 100, (0, 100), "lower = better"),
    ("Self_Care_Engagement", "Self-care engagement", 100, (0, 100), ""),
    ("TCM_Practice", "TCM practice (acupoint, Baduanjin)", 100, (0, 100), ""),
    ("Servings_Eaten", "Congee servings eaten / week", 1, (0, 7), "plan: S3 = 2, S4 = 7"),
    ("Cooking_Workload", "Cooking workload (hours / week)", 1, (0, 4), ""),
]
fig, axs = plt.subplots(4, 4, figsize=(16, 13.5), sharex=True, gridspec_kw=dict(hspace=0.42, wspace=0.22))
for ax, (v, t, sc, yl, note) in zip(axs.ravel(), PANELS):
    shade(ax, label=(ax in axs[0]), short=True)
    ax.set_ylim(*yl)
    lines(ax, v, scale=sc, labels=False, lw=1.8)
    ax.set_xticks([1, 4, 7, 10, 13, 16, 18])
    ax.set_title(t, loc="left", fontsize=10.5, color=INK, pad=16 if ax in axs[0] else 6)
    if note:
        ax.text(0.99, 0.97, note, transform=ax.transAxes, ha="right", va="top", fontsize=7.8, color=INK2)
for ax in axs[-1]:
    ax.set_xlabel("Semester week")
handles = [Line2D([0], [0], color=COL[n], lw=2.4, marker="o", ms=4) for n in names]
fig.legend(handles, [SHORT[n] for n in names], loc="lower center", ncol=4, frameon=False, fontsize=10,
           bbox_to_anchor=(0.5, 0.005))
fig.suptitle("Behaviour-over-time graphs (BOTG): how each part of the system moves in the four scenarios",
             x=0.05, ha="left", fontsize=14, color=INK, y=0.985)
fig.text(0.05, 0.965, "Index 0-100 unless stated. R = recess / reading week, Mid = midterms, Subm. = submission weeks, "
         "Fin = finals.\n" + NOTE, fontsize=8.8, color=INK2, ha="left", va="top", linespacing=1.4)
fig.subplots_adjust(left=0.05, right=0.985, top=0.885, bottom=0.07)
fig.savefig(OUT + "fig3_BOTG_v3.png", dpi=180)
plt.close(fig)

# ------------------------------------------------------------- Figure 4: constitution switch
cons = summ["constitution_finals"]
labs = [lab for lab, _, _ in m.CONSTITUTION.values()]
MK = dict(zip(labs, ["o", "^", "s"]))
fig, axs = plt.subplots(1, 4, figsize=(15, 4.6), sharey=True, gridspec_kw=dict(wspace=0.12))
for ax, (v, t, sc) in zip(axs, [("Sleep_Quality", "Sleep quality", 100), ("Fatigue", "Fatigue (lower = better)", 100),
                                ("Physical_Wellbeing", "Physical wellbeing", 1), ("Mental_Wellbeing", "Mental wellbeing", 1)]):
    for i, n in enumerate(names):
        y = len(names) - 1 - i
        vals = [cons[n][lab][v] * sc for lab in labs]
        ax.plot([min(vals), max(vals)], [y, y], color=GRID, lw=3, zorder=1)
        for lab, val in zip(labs, vals):
            ax.scatter(val, y, marker=MK[lab], s=70, color=COL[n], edgecolor="white", linewidth=1.2, zorder=3)
    ax.set_title(t + " at finals", loc="left", fontsize=10.5, color=INK)
    ax.grid(axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
axs[0].set_yticks(range(len(names)))
axs[0].set_yticklabels([TINY[n] for n in names[::-1]])
handles = [Line2D([0], [0], marker=MK[lab], color="#7d7c78", ls="none", ms=8) for lab in labs]
fig.legend(handles, ["Balanced constitution", "Yin deficiency (sleep links x1.5)", "Yang deficiency (fatigue build-up x1.5)"],
           loc="lower center", ncol=3, frameon=False, fontsize=9.5)
fig.suptitle("Individual constitution (个体体质) as a parameter switch: same stressors, different weak point",
             x=0.06, ha="left", fontsize=13, color=INK, y=0.98)
fig.text(0.06, 0.905, "Finals weeks, median of 1,000 students. Yin-deficient students lose more sleep; "
         "Yang-deficient students build more fatigue. Congee lifts every constitution, but the gap between them\n"
         "stays about the same: this recipe is not tailored to Yin or Yang deficiency (a pattern-matched diet, "
         "bian zheng shi shan, would be needed).", fontsize=8.8, color=INK2, ha="left", va="top", linespacing=1.4)
fig.subplots_adjust(left=0.08, right=0.99, top=0.76, bottom=0.2)
fig.savefig(OUT + "fig4_constitution_v3.png", dpi=200)
plt.close(fig)
print("saved 4 figures")

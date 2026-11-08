"""Draw CLD v3 (TCM holistic) from cld_v3.py. Run: python draw_cld_v3.py -> ../1_CLD/congee_cld_v3_holistic.png"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from cld_v3 import NODES, EDGES, NAMED, audit
plt.rcParams['font.family'] = ['DejaVu Sans', 'Microsoft YaHei']

# group colours (same scheme as v1: amber = TCM, teal = psychological, grey = shared) + green = outcomes
EDGE = {"T": "#9A4A00", "P": "#006D77", "S": "#4A4A4A", "O": "#2E6B30", "B": "#9A4A00"}
FILL = {"T": "#FFE6BF", "P": "#D3EEF2", "S": "#EDEDED", "O": "#DDEFD9", "B": "#D3EEF2"}
INK = "#111111"
RED, GREEN = "#B00020", "#1B5E20"

POS = {  # hand layout, data units (x 0-200, y 0-125)
    "PF": (46, 124), "CR": (39, 104), "SE": (9, 74), "CW": (46, 80), "RB": (66, 70), "NPI": (22, 47),
    "BA": (24, 24), "SC": (52, 9), "SSE": (78, 124), "SHE": (78, 104), "SF": (118, 118), "LQS": (160, 118),
    "CRD": (196, 124), "QB": (106, 92), "HBM": (144, 98), "CS": (112, 74), "SL": (150, 76), "FT": (152, 50),
    "CON": (196, 64), "AD": (198, 42), "UH": (190, 96), "PW": (110, 48), "MW": (78, 30), "MI": (90, 10),
    "BAW": (128, 32), "RU": (150, 14), "PAS": (184, 18),
}
RAD = {("CW", "CR"): 0.55, ("CR", "CW"): 0.55, ("SE", "CR"): -0.2, ("PF", "CR"): 0.1, ("CR", "SSE"): -0.1,
       ("CR", "SHE"): 0.05, ("SSE", "SF"): -0.05, ("SHE", "CS"): 0.1, ("CR", "BA"): 0.1, ("CR", "UH"): -0.3,
       ("UH", "FT"): 0.22, ("FT", "UH"): 0.22, ("FT", "BAW"): 0.2, ("BAW", "FT"): 0.2, ("MI", "BAW"): 0.1,
       ("RU", "SF"): -0.25, ("RU", "LQS"): 0.12, ("LQS", "SF"): 0.0, ("NPI", "QB"): -0.12,
       ("SF", "QB"): 0.0, ("SF", "HBM"): 0.15, ("QB", "HBM"): -0.1, ("HBM", "SL"): 0.0, ("HBM", "RU"): -0.32,
       ("SF", "MW"): 0.28, ("QB", "PW"): -0.12, ("QB", "FT"): -0.12, ("CS", "SL"): 0.0, ("CS", "MW"): 0.0,
       ("RU", "CS"): 0.12, ("RU", "MW"): -0.08, ("SL", "RU"): 0.0, ("SL", "FT"): 0.1, ("SL", "PW"): 0.1,
       ("FT", "PW"): 0.0, ("FT", "PAS"): -0.12, ("AD", "PAS"): 0.05, ("AD", "FT"): 0.0, ("AD", "CRD"): 0.12,
       ("CRD", "SF"): -0.12, ("CRD", "CS"): 0.08, ("CRD", "SL"): 0.1, ("PAS", "RU"): 0.1, ("PAS", "UH"): 0.12,
       ("PAS", "MW"): -0.12, ("MI", "RU"): 0.15, ("MI", "MW"): -0.15, ("BA", "SC"): 0.15, ("SC", "MW"): -0.1,
       ("PW", "SE"): -0.25, ("MW", "SE"): -0.15, ("CW", "FT"): -0.12, ("CW", "MI"): 0.25, ("RB", "FT"): 0.06,
       ("CW", "RB"): -0.05, ("SE", "NPI"): 0.1, ("UH", "SL"): 0.0, ("UH", "SF"): -0.08, ("CON", "SL"): 0.1,
       ("CON", "FT"): -0.1}
CTRL = {("UH", "SE"): [(150, 150), (-16, 140)],
        ("CW", "PAS"): [(46, -18), (160, -20)],
        ("SC", "PAS"): [(80, -6), (150, -6)],
        ("NPI", "LQS"): [(16, 152), (150, 152)],
        ("PAS", "LQS"): [(205, 40), (195, 105)]}

LOOPS = [  # (label, short name, x, y)
    ("R1", "stress-Spleen", 167, 40), ("R2", "activation-control", 38, 36), ("R3", "ingredients", 92, 113),
    ("R4", "rumination-sleep", 136, 60), ("R5", "Heart-Spleen", 131, 109), ("R6", "cooking-mindfulness", 64, 20),
    ("R7", "recovery break", 84, 60), ("R8", "habits injure Spleen", 176, 74),
    ("R9", "Liver overacts Spleen", 174, 103), ("R10", "Liver-Heart-Spleen", 158, 88),
    ("R11", "TCM practice", 60, 45), ("R13", "mindful awareness", 108, 18),
    ("B1", "masking quick fix", 178, 58), ("B2", "time-cost brake", 56, 66), ("B3", "workload brake", 43, 93),
    ("B4", "Zhi Wei Bing", 143, 40),
]

fig, ax = plt.subplots(figsize=(19, 16))
ax.set_xlim(-10, 212)
ax.set_ylim(-30, 156)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.01)
renderer = fig.canvas.get_renderer()
inv = ax.transData.inverted()

boxes = {}
for nid, (label, grp, exo) in NODES.items():
    x, y = POS[nid]
    t = ax.text(x, y, label, ha="center", va="center", fontsize=9.6, color=INK, zorder=5,
                fontweight="bold" if nid in ("PW", "MW", "SF", "CR", "LQS", "QB", "HBM") else "normal", linespacing=1.15)
    bb = t.get_window_extent(renderer)
    (x0, y0), (x1, y1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    w, h = (x1 - x0) + 3.2, (y1 - y0) + 2.4
    box = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=1.6",
                         fc="white" if exo else FILL[grp], ec=EDGE[grp], lw=2.4 if nid in ("PW", "MW", "LQS") else 1.4,
                         ls=(0, (4, 2)) if exo else "-", zorder=4)
    ax.add_patch(box)
    boxes[nid] = (box, x, y, w, h)


def inside(px, py, nid, pad=0.6):
    _, x, y, w, h = boxes[nid]
    return abs(px - x) <= w / 2 + pad and abs(py - y) <= h / 2 + pad


def bezier(pts, n=400):
    """General Bezier through control points (de Casteljau)."""
    pts = np.array(pts, float)
    t = np.linspace(0, 1, n)[:, None, None]
    P = np.repeat(pts[None], n, axis=0)
    while P.shape[1] > 1:
        P = (1 - t) * P[:, :-1] + t * P[:, 1:]
    return P[:, 0]


def edge_curve(s, d):
    p0, p2 = POS[s], POS[d]
    if (s, d) in CTRL:
        return bezier([p0, *CTRL[(s, d)], p2])
    rad = RAD.get((s, d), 0.12)
    (x1, y1), (x2, y2) = p0, p2
    c = ((x1 + x2) / 2 + rad * (y2 - y1), (y1 + y2) / 2 - rad * (x2 - x1))
    return bezier([p0, c, p2])


for s, d, pol, delay, note in EDGES:
    gs, gd = NODES[s][1], NODES[d][1]
    col = EDGE[gs] if gs == gd and gs != "B" else EDGE["S"]
    curve = edge_curve(s, d)
    keep = [i for i, (px, py) in enumerate(curve) if not inside(px, py, s) and not inside(px, py, d)]
    a, b = keep[0], keep[-1]
    seg = curve[a:b + 1]
    lw = 1.9 if gs != gd else 1.5
    ls = "-"
    if pol == "m":
        col, lw, ls = "#7a7a7a", 1.4, (0, (2, 2))
    # draw the trimmed bezier as a polyline + arrowhead on the last short piece
    arc = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(seg, axis=0).T))])
    total = arc[-1]
    head = int(np.searchsorted(arc, total - 2.2))
    ax.plot(seg[:head + 1, 0], seg[:head + 1, 1], color=col, lw=lw, zorder=3, solid_capstyle="round", ls=ls)
    ax.add_patch(FancyArrowPatch(seg[head], seg[-1], arrowstyle="-|>", mutation_scale=15, color=col, lw=lw,
                                 zorder=3, shrinkA=0, shrinkB=0))
    # polarity sign ~4.5 units back from the arrowhead, offset to the left of travel direction
    k = int(np.searchsorted(arc, max(total - 4.6, total * 0.5)))
    px, py = seg[k]
    dx, dy = seg[min(k + 4, len(seg) - 1)] - seg[max(k - 4, 0)]
    nrm = np.hypot(dx, dy) or 1
    ox, oy = -dy / nrm * 1.8, dx / nrm * 1.8
    if pol == "m":
        ax.text(px + ox * 2.4, py + oy * 2.4, "Yin def. \u2013" if d == "SL" else "Yang def. +", ha="center",
                va="center", fontsize=8.5, color="#4a4a4a", style="italic", zorder=6,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))
        continue
    sign = "+" if pol == "+" else "\u2013"
    ax.text(px + ox, py + oy, sign, ha="center", va="center", fontsize=13, fontweight="bold",
            color=RED if pol == "-" else INK, zorder=6,
            bbox=dict(boxstyle="circle,pad=0.05", fc="white", ec="none", alpha=0.85))
    if delay:
        m = int(np.searchsorted(arc, total / 2))
        mx, my = seg[m]
        tx, ty = seg[m + 3] - seg[m - 3]
        tn = np.hypot(tx, ty) or 1
        tx, ty = tx / tn, ty / tn
        for off in (-0.55, 0.55):
            cx, cy = mx + tx * off, my + ty * off
            ax.plot([cx - ty * 1.5, cx + ty * 1.5], [cy + tx * 1.5, cy - tx * 1.5], color=INK, lw=2.2, zorder=6)

for lab, name, x, y in LOOPS:
    c = RED if lab[0] == "R" else GREEN
    ax.add_patch(Circle((x, y), 3.3, fc="white", ec=c, lw=1.8, zorder=2))
    ax.annotate("", xy=(x + 2.1, y + 2.15), xytext=(x - 2.1, y + 2.15), zorder=2,
                arrowprops=dict(arrowstyle="-|>", color=c, lw=1.2, connectionstyle="arc3,rad=-0.55"))
    ax.text(x, y, lab, ha="center", va="center", fontsize=10, fontweight="bold", color=c, zorder=2)
    ax.text(x, y - 4.4, name, ha="center", va="top", fontsize=7.6, color=c, zorder=7, style="italic",
            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))

ax.text(-9, 155, "CLD v3 (TCM holistic): Chinese yam, lotus seed and red date congee for time-constrained NUS students",
        fontsize=15, color=INK, ha="left", va="top", fontweight="bold")
ax.text(-9, 151, "Holism (整体观) and treating the undiseased (治未病): Liver–Spleen (Five Elements), qi & blood, Heart–Spleen, circadian rhythm (天人合一), TCM self-care, body awareness, constitution. 27 variables, 63 causal links + 2 moderators.",
        fontsize=10, color="#52514e", ha="left", va="top")

legend = ("Amber = TCM physiological   Teal = psychological / behavioural   Teal box, amber border = "
          "psychological\u2013physiological bridge   Grey = shared driver   Green = wellbeing outcome   "
          "Dashed box = exogenous input\n"
          "+ same direction   \u2013 opposite direction   || = time delay   Grey (thicker) arrows = cross-subsystem coupling"
          "   Dotted grey arrow = moderator (parameter switch)\n"
          "Red circle R = reinforcing loop (even number of \u2013)   Green circle B = balancing loop (odd number of \u2013)"
          "   R3 = R3a/R3b, R12 (TCM practice soothes Liver) and STB-R are listed in CLD_v3_holistic.md")
ax.text(-9, -20, legend, fontsize=9, color=INK, ha="left", va="top", linespacing=1.6,
        bbox=dict(boxstyle="round,pad=0.6", fc="#FAFAFA", ec="#9E9E9E", lw=0.8))

if __name__ == "__main__":
    audit(verbose=False)
    fig.savefig("../1_CLD/congee_cld_v3_holistic.png", dpi=180)
    fig.savefig("../1_CLD/congee_cld_v3_holistic.svg")
    print("saved")

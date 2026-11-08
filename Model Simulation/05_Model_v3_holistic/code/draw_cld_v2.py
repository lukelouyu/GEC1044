"""Draw the v2 CLD from cld_v2.py. Run: python draw_cld_v2.py -> ../1_CLD/congee_cld_v2.png (+ .svg)"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from cld_v2 import NODES, EDGES, NAMED, audit

# group colours (same scheme as v1: amber = TCM, teal = psychological, grey = shared) + green = outcomes
EDGE = {"T": "#9A4A00", "P": "#006D77", "S": "#4A4A4A", "O": "#2E6B30"}
FILL = {"T": "#FFE6BF", "P": "#D3EEF2", "S": "#EDEDED", "O": "#DDEFD9"}
INK = "#111111"
RED, GREEN = "#B00020", "#1B5E20"

POS = {  # hand layout, data units (x 0-170, y 0-100)
    "PF": (44, 102), "CR": (34, 84), "SE": (10, 62), "CW": (42, 60), "RB": (66, 52), "BA": (24, 30),
    "SC": (46, 14), "MI": (78, 14), "RU": (112, 22), "SSE": (70, 94), "SHE": (68, 77),
    "SF": (100, 92), "CS": (106, 68), "SL": (134, 74), "FT": (132, 46), "PW": (98, 42), "MW": (66, 30),
    "AD": (165, 58), "PAS": (150, 25), "UH": (156, 86),
}
# curvature per edge (matplotlib arc3 convention); default 0.12
RAD = {("CR", "SSE"): -0.1, ("CR", "SHE"): 0.05, ("SSE", "SF"): -0.05, ("SHE", "CS"): 0.05,
       ("RU", "SF"): 0.30, ("UH", "SF"): 0.1, ("UH", "SL"): -0.05, ("UH", "FT"): 0.22, ("FT", "UH"): 0.22,
       ("PAS", "UH"): -0.1, ("CW", "CR"): 0.55, ("CR", "CW"): 0.55, ("SE", "CR"): -0.2, ("PF", "CR"): 0.1,
       ("CR", "UH"): -0.28, ("CW", "FT"): -0.12, ("CW", "MI"): 0.25, ("RB", "FT"): 0.0, ("SF", "MW"): 0.05,
       ("SF", "PW"): 0.15, ("SF", "FT"): -0.1, ("SF", "CS"): 0.0, ("CS", "MW"): -0.05, ("RU", "MW"): 0.05,
       ("RU", "CS"): -0.1, ("SL", "RU"): 0.0, ("SL", "FT"): 0.1, ("SL", "PW"): 0.08, ("FT", "PW"): 0.0,
       ("FT", "PAS"): -0.1, ("AD", "PAS"): -0.1, ("AD", "FT"): 0.0, ("PAS", "RU"): -0.12, ("PAS", "MW"): -0.2,
       ("MI", "RU"): 0.05, ("MI", "MW"): -0.15, ("BA", "SC"): 0.15, ("SC", "MW"): -0.1, ("PW", "SE"): -0.25,
       ("MW", "SE"): -0.15, ("CR", "BA"): 0.12, ("CS", "SL"): -0.05, ("CW", "RB"): -0.05, ("CR", "SSE"): -0.1}
# long links routed along the margins as cubic curves: explicit control points
CTRL = {("UH", "SE"): [(130, 128), (-14, 122)],
        ("CW", "PAS"): [(44, -14), (140, -16)],
        ("SC", "PAS"): [(70, 0), (130, 2)]}

LOOPS = [  # (label, short name, x, y)
    ("R1", "stress-Spleen", 139, 37), ("R2", "activation-control", 35, 34), ("R3", "ingredients", 85, 82),
    ("R4", "rumination-sleep", 123, 34), ("R5", "Heart-Spleen", 115, 53), ("R6", "cooking-mindfulness", 90, 24),
    ("R7", "recovery break", 82, 58), ("R8", "habits injure Spleen", 126, 84), ("B1", "masking quick fix", 147, 64),
    ("B2", "time-cost brake", 56, 67), ("B3", "workload brake", 38.5, 73),
]

fig, ax = plt.subplots(figsize=(17, 13.4))
ax.set_xlim(-6, 178)
ax.set_ylim(-20, 124)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.01)
renderer = fig.canvas.get_renderer()
inv = ax.transData.inverted()

boxes = {}
for nid, (label, grp, exo) in NODES.items():
    x, y = POS[nid]
    t = ax.text(x, y, label, ha="center", va="center", fontsize=9.6, color=INK, zorder=5,
                fontweight="bold" if nid in ("PW", "MW", "SF", "CR") else "normal", linespacing=1.15)
    bb = t.get_window_extent(renderer)
    (x0, y0), (x1, y1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    w, h = (x1 - x0) + 3.2, (y1 - y0) + 2.4
    box = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=1.6",
                         fc="white" if exo else FILL[grp], ec=EDGE[grp], lw=2.2 if nid in ("PW", "MW") else 1.4,
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
    col = EDGE[gs] if gs == gd else EDGE["S"]
    curve = edge_curve(s, d)
    keep = [i for i, (px, py) in enumerate(curve) if not inside(px, py, s) and not inside(px, py, d)]
    a, b = keep[0], keep[-1]
    seg = curve[a:b + 1]
    lw = 1.9 if gs != gd else 1.5
    # draw the trimmed bezier as a polyline + arrowhead on the last short piece
    arc = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(seg, axis=0).T))])
    total = arc[-1]
    head = int(np.searchsorted(arc, total - 2.2))
    ax.plot(seg[:head + 1, 0], seg[:head + 1, 1], color=col, lw=lw, zorder=3, solid_capstyle="round")
    ax.add_patch(FancyArrowPatch(seg[head], seg[-1], arrowstyle="-|>", mutation_scale=15, color=col, lw=lw,
                                 zorder=3, shrinkA=0, shrinkB=0))
    # polarity sign ~4.5 units back from the arrowhead, offset to the left of travel direction
    k = int(np.searchsorted(arc, max(total - 4.6, total * 0.5)))
    px, py = seg[k]
    dx, dy = seg[min(k + 4, len(seg) - 1)] - seg[max(k - 4, 0)]
    nrm = np.hypot(dx, dy) or 1
    ox, oy = -dy / nrm * 1.8, dx / nrm * 1.8
    sign = "+" if pol == "+" else "–"
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
    ax.add_patch(Circle((x, y), 3.0, fc="white", ec=c, lw=1.8, zorder=2))
    ax.annotate("", xy=(x + 2.1, y + 2.15), xytext=(x - 2.1, y + 2.15), zorder=2,
                arrowprops=dict(arrowstyle="-|>", color=c, lw=1.2, connectionstyle="arc3,rad=-0.55"))
    ax.text(x, y, lab, ha="center", va="center", fontsize=10, fontweight="bold", color=c, zorder=2)
    ax.text(x, y - 4.4, name, ha="center", va="top", fontsize=7.6, color=c, zorder=7, style="italic",
            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))

ax.text(-5, 123, "CLD v2: Chinese yam, lotus seed and red date congee for time-constrained NUS students",
        fontsize=15, color=INK, ha="left", va="top", fontweight="bold")
ax.text(-5, 119.2, "New: cooking workload (time cost vs recovery break), mindfulness of cooking, Spleen function "
        "→ physical and mental wellbeing, unhealthy habits. 20 variables, 46 links.",
        fontsize=10, color="#52514e", ha="left", va="top")

legend = ("Amber = TCM physiological   Teal = psychological / behavioural   Grey = shared driver   "
          "Green = wellbeing outcome   Dashed box = exogenous input\n"
          "+ same direction   – opposite direction   || = time delay on that link   "
          "Grey (thicker) arrows = cross-subsystem coupling   "
          "Red circle R = reinforcing loop (even number of –)   Green circle B = balancing loop (odd number of –)")
ax.text(-5, -10, legend, fontsize=9, color=INK, ha="left", va="top", linespacing=1.6,
        bbox=dict(boxstyle="round,pad=0.6", fc="#FAFAFA", ec="#9E9E9E", lw=0.8))

if __name__ == "__main__":
    audit(verbose=False)
    fig.savefig("../1_CLD/congee_cld_v2.png", dpi=200)
    fig.savefig("../1_CLD/congee_cld_v2.svg")
    print("saved")

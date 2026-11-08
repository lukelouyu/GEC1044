"""Stock-and-flow diagram (SFD) v2 for Stella Architect.

Run: python sfd_v2.py
  -> ../2_SFD_Stella/congee_model_v3.stmx   (open in Stella Architect / Stella Professional; XMILE format)
  -> ../2_SFD_Stella/congee_sfd_v3.png      (picture of the same diagram, drawn in Stella's visual style)

Equations come from model_v3.py (same source as the Python simulation), with nominal parameter values and the
calibrated values from calibration_v3.json. The diagram layout below is shared by the .stmx and the PNG.
Stella conventions used: stocks = rectangles, flows = pipes with valves, clouds = outside the model boundary,
converters = circles, connectors = curved arrows, ghosts (aliases, dashed) = copies of a variable placed
elsewhere to avoid long connectors.
"""
import json
import math
import uuid
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, FancyBboxPatch, Polygon
from matplotlib.path import Path
import model_v3 as m

OUT = "../2_SFD_Stella/"
SW, SH = 76, 44            # stock size (px)
AUX_R = 15                 # converter radius (px)
VALVE_R = 9
PIPE = 142                 # pipe length from stock edge to cloud

disp = lambda n: n.replace("_", " ")

# ------------------------------------------------------------------ layout (Stella px, y down)
SECTORS = [  # title, x0, y0, x1, y1, colour
    ("1  Congee plan, adherence and cooking workload", 20, 28, 560, 640, "#e8f1fb"),
    ("2  TCM organs: Liver, Spleen, qi & blood, Heart, sleep", 580, 28, 1240, 790, "#fdf1e2"),
    ("3  Fatigue: study effort, recovery and body awareness", 1260, 28, 1820, 360, "#fdf1e2"),
    ("4  Unhealthy habits (caffeine, cigarettes, alcohol, junk food)", 1260, 375, 1820, 690, "#f1f1f1"),
    ("5  Stress, rumination, mindfulness; circadian rhythm and constitution", 580, 805, 1240, 1295, "#e6f4f1"),
    ("6  Self-care, TCM practice and sense of control", 20, 655, 560, 1295, "#e6f4f1"),
    ("7  Wellbeing outcomes (0-100)", 1260, 705, 1820, 1295, "#e9f4e6"),
]
STOCK_POS = {
    "Congee_Habit": (340, 285), "Liver_Qi_Stagnation": (860, 150), "Spleen_Function": (860, 300),
    "Calm_Shen": (860, 560), "Sleep_Quality": (860, 700), "Fatigue": (1540, 150), "Unhealthy_Habits": (1540, 510),
    "Perceived_Stress": (1110, 920), "Rumination": (1110, 1070), "Mindfulness": (1110, 1215),
    "Self_Care_Engagement": (340, 790), "Sense_of_Control": (340, 1050),
}
AUX_POS = {
    "Scenario": (60, 95), "Congee_Plan": (160, 95), "Planned_Servings": (265, 95), "Adherence": (455, 232),
    "Servings_Eaten": (330, 150), "Batches_Cooked": (470, 370), "Cooking_Workload": (470, 470),
    "Recovery_Break": (330, 430), "Mindful_Cooking": (330, 530),
    "Spleen_Strengthening_Effect": (650, 225), "Qi_Blood_Generation": (860, 410),
    "Heart_Blood_Malnourishment": (1010, 430), "Shen_Calming_Effect": (650, 495),
    "Felt_Fatigue": (1540, 262), "Body_Awareness": (1690, 290), "Lifestyle_Propensity": (1385, 615),
    "Academic_Demands": (630, 870), "Course_Load": (630, 965), "Study_Load": (745, 915),
    "Circadian_Disruption": (745, 1010), "Free_Hours": (630, 1065), "Time_Squeeze": (760, 1120),
    "Constitution": (630, 1240), "Yin_Deficiency_Factor": (735, 1250), "Yang_Deficiency_Factor": (840, 1250),
    "TCM_Practice": (470, 920), "Behavioural_Activation": (420, 1185),
    "Physical_Wellbeing": (1540, 820), "Mental_Wellbeing": (1540, 1130),
}
GHOSTS = {  # id: (variable, x, y)
    "g_SE1": ("Self_Care_Engagement", 410, 70), "g_PAS1": ("Perceived_Stress", 525, 265),
    "g_PAS4": ("Perceived_Stress", 655, 98), "g_RU3": ("Rumination", 755, 88), "g_NPI1": ("TCM_Practice", 1050, 92),
    "g_RU1": ("Rumination", 1065, 228), "g_UH1": ("Unhealthy_Habits", 1150, 258),
    "g_CRD1": ("Circadian_Disruption", 1125, 360), "g_NPI2": ("TCM_Practice", 745, 425),
    "g_SVS2": ("Servings_Eaten", 620, 420), "g_RU4": ("Rumination", 1065, 500),
    "g_UH4": ("Unhealthy_Habits", 1150, 535), "g_CRD2": ("Circadian_Disruption", 1120, 625),
    "g_UH2": ("Unhealthy_Habits", 640, 630), "g_HBM1": ("Heart_Blood_Malnourishment", 760, 615),
    "g_CRD3": ("Circadian_Disruption", 650, 760), "g_YIN": ("Yin_Deficiency_Factor", 790, 760),
    "g_STL": ("Study_Load", 1300, 82), "g_YANG": ("Yang_Deficiency_Factor", 1395, 70),
    "g_CW1": ("Cooking_Workload", 1300, 232), "g_SL1": ("Sleep_Quality", 1610, 66),
    "g_QB1": ("Qi_Blood_Generation", 1715, 66), "g_RB": ("Recovery_Break", 1785, 210),
    "g_MI1": ("Mindfulness", 1785, 320),
    "g_PAS2": ("Perceived_Stress", 1320, 425), "g_SCN": ("Scenario", 1300, 615),
    "g_SVS": ("Servings_Eaten", 1665, 615), "g_SE2": ("Self_Care_Engagement", 1770, 610),
    "g_FF": ("Felt_Fatigue", 1010, 848), "g_SC1": ("Sense_of_Control", 905, 852),
    "g_CW2": ("Cooking_Workload", 640, 1160), "g_SL2": ("Sleep_Quality", 1205, 1000),
    "g_HBM2": ("Heart_Blood_Malnourishment", 1205, 1140), "g_MC": ("Mindful_Cooking", 965, 1160),
    "g_PW": ("Physical_Wellbeing", 110, 715), "g_MW": ("Mental_Wellbeing", 230, 715),
    "g_UH3": ("Unhealthy_Habits", 470, 718), "g_BC": ("Batches_Cooked", 520, 1185),
    "g_QB2": ("Qi_Blood_Generation", 1380, 775), "g_SL3": ("Sleep_Quality", 1380, 870), "g_FT": ("Fatigue", 1700, 800),
    "g_SF2": ("Spleen_Function", 1540, 985), "g_PAS3": ("Perceived_Stress", 1360, 1040),
    "g_RU2": ("Rumination", 1360, 1130), "g_MI2": ("Mindfulness", 1360, 1220),
    "g_SC2": ("Sense_of_Control", 1720, 1060), "g_CS": ("Calm_Shen", 1720, 1180),
}
GHOST_FOR = {  # (target, dependency) -> ghost id
    ("Adherence", "Self_Care_Engagement"): "g_SE1", ("Adherence", "Perceived_Stress"): "g_PAS1",
    ("Qi_Stagnation_Buildup", "Perceived_Stress"): "g_PAS4", ("Qi_Stagnation_Buildup", "Rumination"): "g_RU3",
    ("Liver_Qi_Soothing", "TCM_Practice"): "g_NPI1",
    ("Spleen_Depletion", "Rumination"): "g_RU1", ("Spleen_Depletion", "Unhealthy_Habits"): "g_UH1",
    ("Spleen_Depletion", "Circadian_Disruption"): "g_CRD1", ("Qi_Blood_Generation", "TCM_Practice"): "g_NPI2",
    ("Shen_Calming_Effect", "Servings_Eaten"): "g_SVS2",
    ("Shen_Disturbance", "Rumination"): "g_RU4", ("Shen_Disturbance", "Unhealthy_Habits"): "g_UH4",
    ("Shen_Disturbance", "Circadian_Disruption"): "g_CRD2",
    ("Change_in_Sleep", "Unhealthy_Habits"): "g_UH2", ("Change_in_Sleep", "Heart_Blood_Malnourishment"): "g_HBM1",
    ("Change_in_Sleep", "Circadian_Disruption"): "g_CRD3", ("Change_in_Sleep", "Yin_Deficiency_Factor"): "g_YIN",
    ("Fatigue_Accumulation", "Study_Load"): "g_STL", ("Fatigue_Accumulation", "Cooking_Workload"): "g_CW1",
    ("Fatigue_Accumulation", "Yang_Deficiency_Factor"): "g_YANG",
    ("Fatigue_Recovery", "Sleep_Quality"): "g_SL1", ("Fatigue_Recovery", "Qi_Blood_Generation"): "g_QB1",
    ("Fatigue_Recovery", "Recovery_Break"): "g_RB", ("Body_Awareness", "Mindfulness"): "g_MI1",
    ("Habit_Uptake", "Perceived_Stress"): "g_PAS2", ("Habit_Quitting", "Self_Care_Engagement"): "g_SE2",
    ("Habit_Quitting", "Servings_Eaten"): "g_SVS", ("Lifestyle_Propensity", "Scenario"): "g_SCN",
    ("Change_in_Stress", "Felt_Fatigue"): "g_FF", ("Change_in_Stress", "Sense_of_Control"): "g_SC1",
    ("Time_Squeeze", "Cooking_Workload"): "g_CW2", ("Change_in_Rumination", "Sleep_Quality"): "g_SL2",
    ("Change_in_Rumination", "Heart_Blood_Malnourishment"): "g_HBM2", ("Change_in_Mindfulness", "Mindful_Cooking"): "g_MC",
    ("Change_in_Self_Care", "Physical_Wellbeing"): "g_PW", ("Change_in_Self_Care", "Mental_Wellbeing"): "g_MW",
    ("Change_in_Self_Care", "Unhealthy_Habits"): "g_UH3", ("Behavioural_Activation", "Batches_Cooked"): "g_BC",
    ("Physical_Wellbeing", "Qi_Blood_Generation"): "g_QB2", ("Physical_Wellbeing", "Sleep_Quality"): "g_SL3",
    ("Physical_Wellbeing", "Fatigue"): "g_FT", ("Mental_Wellbeing", "Spleen_Function"): "g_SF2",
    ("Mental_Wellbeing", "Perceived_Stress"): "g_PAS3", ("Mental_Wellbeing", "Rumination"): "g_RU2",
    ("Mental_Wellbeing", "Mindfulness"): "g_MI2", ("Mental_Wellbeing", "Sense_of_Control"): "g_SC2",
    ("Mental_Wellbeing", "Calm_Shen"): "g_CS",
}
# connector bend in degrees (positive = takeoff rotated counter-clockwise on screen); default 0 = straight
BEND = {
    ("Adherence", "Congee_Habit_Change"): -18, ("Planned_Servings", "Adherence"): -20,
    ("Spleen_Function", "Spleen_Nourishment"): 35, ("Spleen_Function", "Spleen_Depletion"): -35,
    ("Liver_Qi_Stagnation", "Qi_Stagnation_Buildup"): 35, ("Liver_Qi_Stagnation", "Liver_Qi_Soothing"): -35,
    ("Calm_Shen", "Shen_Settling"): 35, ("Calm_Shen", "Shen_Disturbance"): -35,
    ("Sleep_Quality", "Change_in_Sleep"): 35, ("Fatigue", "Fatigue_Accumulation"): 35,
    ("Fatigue", "Fatigue_Recovery"): -35, ("Unhealthy_Habits", "Habit_Uptake"): -35,
    ("Unhealthy_Habits", "Habit_Quitting"): 35, ("Congee_Habit", "Congee_Habit_Change"): -35,
    ("Perceived_Stress", "Change_in_Stress"): 35, ("Rumination", "Change_in_Rumination"): 35,
    ("Mindfulness", "Change_in_Mindfulness"): -35, ("Self_Care_Engagement", "Change_in_Self_Care"): 35,
    ("Sense_of_Control", "Change_in_Control"): 35, ("Perceived_Stress", "Change_in_Rumination"): 15,
    ("Mindfulness", "Change_in_Rumination"): -15, ("Felt_Fatigue", "Habit_Uptake"): 10,
    ("Unhealthy_Habits", "Felt_Fatigue"): 25, ("Liver_Qi_Stagnation", "Spleen_Depletion"): -12,
    ("Calm_Shen", "Change_in_Sleep"): 15, ("Spleen_Function", "Heart_Blood_Malnourishment"): -10,
    ("Servings_Eaten", "Spleen_Strengthening_Effect"): 6, ("Study_Load", "Change_in_Stress"): 14,
    ("Time_Squeeze", "Change_in_Stress"): -8, ("Behavioural_Activation", "Change_in_Control"): -15,
    ("Felt_Fatigue", "Body_Awareness"): -15, ("Body_Awareness", "Fatigue_Recovery"): 10,
    ("Self_Care_Engagement", "TCM_Practice"): -15, ("Constitution", "Yang_Deficiency_Factor"): -28,
    ("Constitution", "Yin_Deficiency_Factor"): -8,
}


def flow_geometry():
    """Pipe end points for every flow: inflows come from a cloud on the left, outflows go to a cloud on the right."""
    geo = {}
    for s, st in m.STOCKS.items():
        x, y = STOCK_POS[s]
        for f in st["inflows"]:
            geo[f] = dict(pts=[(x - SW / 2 - PIPE, y), (x - SW / 2, y)], cloud="start", stock=s)
        for f in st["outflows"]:
            geo[f] = dict(pts=[(x + SW / 2, y), (x + SW / 2 + PIPE, y)], cloud="end", stock=s)
    for f, g in geo.items():
        (x0, y0), (x1, y1) = g["pts"]
        g["valve"] = ((x0 + x1) / 2, (y0 + y1) / 2)
    return geo


FLOW_GEO = flow_geometry()


def pos(name):
    if name in STOCK_POS:
        return STOCK_POS[name]
    if name in AUX_POS:
        return AUX_POS[name]
    if name in FLOW_GEO:
        return FLOW_GEO[name]["valve"]
    if name in GHOSTS:
        return GHOSTS[name][1:]
    raise KeyError(name)


def connectors():
    """(source element id, target variable, bend). Source may be a ghost id."""
    out = []
    for target, spec in list(m.FLOWS.items()) + list(m.AUXES.items()):
        for dep in m.deps(spec["eqn"]):
            src = GHOST_FOR.get((target, dep), dep)
            out.append((src, target, BEND.get((dep, target), 0)))
    return out


CONN = connectors()


def start_angle(src, dst, bend):
    (x0, y0), (x1, y1) = pos(src), pos(dst)
    return math.degrees(math.atan2(-(y1 - y0), x1 - x0)) + bend   # screen angle, counter-clockwise, y up


# ------------------------------------------------------------------ XMILE (.stmx) export
def fmt(v):
    v = float(v)
    return str(int(v)) if v == int(v) else repr(round(v, 4))


def fill(eqn, p):
    import re
    return re.sub(r"\{(\w+)\}", lambda mm: fmt(p[mm.group(1)]), eqn)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write_stmx(p, path):
    L = ['<?xml version="1.0" encoding="utf-8"?>',
         '<xmile version="1.0" xmlns="http://docs.oasis-open.org/xmile/ns/XMILE/v1.0" xmlns:isee="http://iseesystems.com/XMILE">',
         '\t<header>', '\t\t<smile version="1.0" namespace="std, isee"/>',
         '\t\t<name>congee_model_v3</name>', f'\t\t<uuid>{uuid.uuid4()}</uuid>',
         '\t\t<vendor>isee systems, inc.</vendor>', '\t\t<product version="3.0" lang="en">Stella Architect</product>',
         '\t</header>',
         '\t<sim_specs method="Euler" time_units="Weeks">', f'\t\t<start>{m.START}</start>', f'\t\t<stop>{m.STOP}</stop>',
         '\t\t<dt reciprocal="true">7</dt>', '\t</sim_specs>',
         '\t<model>', '\t\t<variables>']
    for s, st in m.STOCKS.items():
        L.append(f'\t\t\t<stock name="{disp(s)}">')
        L.append(f'\t\t\t\t<doc>Index 0-1. Starts the pre-semester holiday (week -8) at this value.</doc>')
        L.append(f'\t\t\t\t<eqn>{fmt(st["init"])}</eqn>')
        for f in st["inflows"]:
            L.append(f'\t\t\t\t<inflow>{f}</inflow>')
        for f in st["outflows"]:
            L.append(f'\t\t\t\t<outflow>{f}</outflow>')
        L.append('\t\t\t</stock>')
    for f, spec in m.FLOWS.items():
        L.append(f'\t\t\t<flow name="{disp(f)}">')
        L.append(f'\t\t\t\t<eqn>{esc(fill(spec["eqn"], p))}</eqn>')
        if not spec.get("biflow"):
            L.append('\t\t\t\t<non_negative/>')
        L.append('\t\t\t</flow>')
    for a, spec in m.AUXES.items():
        L.append(f'\t\t\t<aux name="{disp(a)}">')
        if spec.get("doc"):
            L.append(f'\t\t\t\t<doc>{esc(spec["doc"])}</doc>')
        L.append(f'\t\t\t\t<eqn>{esc(fill(spec["eqn"], p))}</eqn>')
        if spec.get("gf"):
            g = spec["gf"]
            ys = [float(fill(str(v), p)) for v in g["ypts"]]
            L.append('\t\t\t\t<gf type="discrete">')
            L.append(f'\t\t\t\t\t<xscale min="{fmt(g["xmin"])}" max="{fmt(g["xmax"])}"/>')
            L.append(f'\t\t\t\t\t<yscale min="0" max="{fmt(max(1, math.ceil(max(ys))))}"/>')
            L.append('\t\t\t\t\t<ypts>' + ",".join(f"{v:.4f}" for v in ys) + '</ypts>')
            L.append('\t\t\t\t</gf>')
        L.append('\t\t\t</aux>')
    L.append('\t\t</variables>')
    L.append('\t\t<views>')
    L.append('\t\t\t<view isee:show_pages="false" page_width="1840" page_height="1310">')
    uid = 1
    for s, (x, y) in STOCK_POS.items():
        L.append(f'\t\t\t\t<stock x="{x}" y="{y}" width="{SW}" height="{SH}" name="{disp(s)}"/>')
    for f, g in FLOW_GEO.items():
        vx, vy = g["valve"]
        L.append(f'\t\t\t\t<flow x="{vx}" y="{vy}" name="{disp(f)}">')
        L.append('\t\t\t\t\t<pts>')
        for px, py in g["pts"]:
            L.append(f'\t\t\t\t\t\t<pt x="{px}" y="{py}"/>')
        L.append('\t\t\t\t\t</pts>')
        L.append('\t\t\t\t</flow>')
    for a, (x, y) in AUX_POS.items():
        L.append(f'\t\t\t\t<aux x="{x}" y="{y}" name="{disp(a)}"/>')
    ghost_uid = {}
    for gid, (var, x, y) in GHOSTS.items():
        ghost_uid[gid] = uid
        L.append(f'\t\t\t\t<alias font_style="italic" uid="{uid}" x="{x}" y="{y}">')
        L.append(f'\t\t\t\t\t<of>{var}</of>')
        L.append('\t\t\t\t</alias>')
        uid += 1
    for src, dst, bend in CONN:
        ang = start_angle(src, dst, bend) % 360
        frm = f'<alias uid="{ghost_uid[src]}"/>' if src in GHOSTS else src
        L.append(f'\t\t\t\t<connector uid="{uid}" angle="{ang:.2f}">')
        L.append(f'\t\t\t\t\t<from>{frm}</from>')
        L.append(f'\t\t\t\t\t<to>{dst}</to>')
        L.append('\t\t\t\t</connector>')
        uid += 1
    for title, x0, y0, x1, y1, _ in SECTORS:
        L.append(f'\t\t\t\t<text_box uid="{uid}" x="{x0 + 8}" y="{y0 + 4}" width="{x1 - x0 - 16}" height="20">{esc(title)}</text_box>')
        uid += 1
    L += ['\t\t\t</view>', '\t\t</views>', '\t</model>', '</xmile>']
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


# ------------------------------------------------------------------ PNG in Stella's visual style
BLUE, PINK, LABEL = "#1f3fbf", "#e0006f", "#1f3fbf"


def shape_radius(name, direction):
    """Distance from an element's centre to its outline along a unit direction (for trimming connectors)."""
    dx, dy = direction
    if name in STOCK_POS or (name in GHOSTS and GHOSTS[name][0] in STOCK_POS):
        tx = (SW / 2) / abs(dx) if abs(dx) > 1e-9 else 1e9
        ty = (SH / 2) / abs(dy) if abs(dy) > 1e-9 else 1e9
        return min(tx, ty) + 2
    if name in FLOW_GEO:
        return VALVE_R + 3
    return AUX_R + 2


def arc_points(src, dst, bend, n=120):
    S, E = np.array(pos(src), float), np.array(pos(dst), float)
    th = math.radians(start_angle(src, dst, bend))
    t = np.array([math.cos(th), -math.sin(th)])          # screen coords (y down)
    if abs(bend) < 1e-6:
        return S + np.linspace(0, 1, n)[:, None] * (E - S)
    nrm = np.array([-t[1], t[0]])
    d = S - E
    r = -(d @ d) / (2 * (nrm @ d))
    C = S + r * nrm
    a0 = math.atan2(S[1] - C[1], S[0] - C[0])
    a1 = math.atan2(E[1] - C[1], E[0] - C[0])
    # travel direction must match tangent t
    cross = (S - C)[0] * t[1] - (S - C)[1] * t[0]
    if cross > 0:
        while a1 < a0:
            a1 += 2 * math.pi
    else:
        while a1 > a0:
            a1 -= 2 * math.pi
    a = np.linspace(a0, a1, n)
    return np.c_[C[0] + abs(r) * np.cos(a), C[1] + abs(r) * np.sin(a)]


def wrap(text, width=14):
    """Break a long label into two lines at the space nearest the middle."""
    if len(text) <= width or " " not in text:
        return text
    mid = len(text) / 2
    i = min((k for k, c in enumerate(text) if c == " "), key=lambda k: abs(k - mid))
    return text[:i] + "\n" + text[i + 1:]


def draw_cloud(ax, x, y):
    for dx, dy, r in [(-9, 2, 8), (0, -4, 10), (10, 1, 8), (3, 6, 8), (-4, 6, 7)]:
        ax.add_patch(Circle((x + dx, y + dy), r, fc="white", ec=BLUE, lw=1.1, zorder=3))
    for dx, dy, r in [(-9, 2, 6.8), (0, -4, 8.8), (10, 1, 6.8), (3, 6, 6.8), (-4, 6, 5.8)]:
        ax.add_patch(Circle((x + dx, y + dy), r, fc="white", ec="none", zorder=3.1))


def draw_png(path, cal_note):
    fig = plt.figure(figsize=(18.4, 14.1))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1840)
    ax.set_ylim(1410, -100)
    ax.axis("off")
    ax.text(20, -62, "Stella Architect SFD v3 (TCM holistic): congee, cooking workload, Liver-Spleen-Heart, circadian rhythm, constitution",
            fontsize=16, fontweight="bold", color="#111", va="center")
    ax.text(20, -28, "Stocks (rectangles) accumulate; flows (pipes with valves) change them; converters (circles) are "
            "calculated; pink arrows are connectors; dashed italic items are ghosts (copies) of a variable. "
            "Time: week -8 (holiday) to 18, DT = 1 day, Euler.", fontsize=10, color="#52514e", va="center")
    for title, x0, y0, x1, y1, col in SECTORS:
        ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0,rounding_size=10",
                                    fc=col, ec="#c9c8c2", lw=1, zorder=0))
        ax.text(x0 + 10, y0 + 16, title, fontsize=10, fontweight="bold", color="#3b3a37", va="center", zorder=1)
    # flows (pipes)
    for f, g in FLOW_GEO.items():
        (x0, y0), (x1, y1) = g["pts"]
        cloud_pt = (x0, y0) if g["cloud"] == "start" else (x1, y1)
        a, b = np.array([x0, y0], float), np.array([x1, y1], float)
        if g["cloud"] == "start":
            a = a + np.array([14, 0])
        else:
            b = b + np.array([14, 0])
            a = a.copy()
        end = b - np.array([10, 0])
        for off in (-3.2, 3.2):
            ax.plot([a[0], end[0]], [a[1] + off, end[1] + off], color=BLUE, lw=1.2, zorder=2)
        ax.add_patch(Rectangle((a[0], a[1] - 3.2), end[0] - a[0], 6.4, fc="white", ec="none", zorder=1.9))
        ax.add_patch(Polygon([[end[0], end[1] - 8], [b[0] if g["cloud"] == "start" else b[0] - 0, end[1]],
                              [end[0], end[1] + 8]], closed=True, fc="white", ec=BLUE, lw=1.2, zorder=2.1))
        draw_cloud(ax, *cloud_pt)
        vx, vy = g["valve"]
        ax.add_patch(Circle((vx, vy), VALVE_R, fc="white", ec=BLUE, lw=1.3, zorder=4))
        ax.plot([vx, vx], [vy - VALVE_R, vy - VALVE_R - 7], color=BLUE, lw=1.3, zorder=4)
        ax.plot([vx - 6, vx + 6], [vy - VALVE_R - 7, vy - VALVE_R - 7], color=BLUE, lw=1.6, zorder=4)
        ax.text(vx, vy + 22, disp(f), fontsize=8, color=LABEL, ha="center", va="center", zorder=6,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.75))
    # stocks
    for s, (x, y) in STOCK_POS.items():
        ax.add_patch(Rectangle((x - SW / 2, y - SH / 2), SW, SH, fc="white", ec=BLUE, lw=1.6, zorder=4))
        ax.text(x, y - SH / 2 - 11, disp(s), fontsize=9.5, fontweight="bold", color=LABEL, ha="center",
                va="center", zorder=6, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.75))
    # converters
    for a, (x, y) in AUX_POS.items():
        ax.add_patch(Circle((x, y), AUX_R, fc="white", ec=BLUE, lw=1.3, zorder=4))
        if m.AUXES[a].get("gf"):
            ax.plot([x - 7, x - 2, x + 2, x + 7], [y + 5, y + 5, y - 5, y - 5], color=BLUE, lw=1, zorder=5)
        label = wrap(disp(a)).replace("Physical\nWellbeing", "PHYSICAL\nWELLBEING").replace(
            "Mental\nWellbeing", "MENTAL\nWELLBEING")
        bold = a in ("Physical_Wellbeing", "Mental_Wellbeing", "Scenario")
        ax.text(x, y + AUX_R + 6, label, fontsize=8.5 if not bold else 9.5, fontweight="bold" if bold else "normal",
                color=LABEL, ha="center", va="top", zorder=6, linespacing=1.05,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.75))
    # ghosts
    for gid, (var, x, y) in GHOSTS.items():
        if var in STOCK_POS:
            ax.add_patch(Rectangle((x - SW / 2 + 10, y - SH / 2 + 6), SW - 20, SH - 12, fc="white", ec=BLUE, lw=1.1,
                                   ls=(0, (3, 2)), zorder=4))
        else:
            ax.add_patch(Circle((x, y), AUX_R - 2, fc="white", ec=BLUE, lw=1.1, ls=(0, (3, 2)), zorder=4))
        ax.text(x, y + (SH / 2 if var in STOCK_POS else AUX_R) + 3, wrap(disp(var), 18), fontsize=7.6, style="italic",
                color=LABEL, ha="center", va="top", zorder=6,
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.75))
    # connectors
    for src, dst, bend in CONN:
        pts = arc_points(src, dst, bend)
        S, E = pts[0], pts[-1]
        d0 = pts[1] - pts[0]
        d1 = pts[-1] - pts[-2]
        r0 = shape_radius(src, d0 / np.linalg.norm(d0))
        r1 = shape_radius(dst, d1 / np.linalg.norm(d1))
        keep = (np.linalg.norm(pts - S, axis=1) >= r0) & (np.linalg.norm(pts - E, axis=1) >= r1)
        seg = pts[keep]
        if len(seg) < 3:
            continue
        ax.plot(seg[:-3, 0], seg[:-3, 1], color=PINK, lw=0.95, zorder=3.5, alpha=0.9)
        ax.add_patch(FancyArrowPatch(seg[-4], seg[-1], arrowstyle="-|>", mutation_scale=9, color=PINK, lw=0.95,
                                     zorder=3.5, shrinkA=0, shrinkB=0))
    ax.text(20, 1318, cal_note, fontsize=9, color="#52514e", va="top", linespacing=1.5)
    fig.savefig(path, dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    cal = json.load(open("calibration_v3.json"))
    p = m.nominal(cal)
    write_stmx(p, OUT + "congee_model_v3.stmx")
    note = ("Scenario converter: 1 = no congee + bad habits, 2 = no congee + healthy lifestyle, 3 = congee once a week "
            "(1 batch = 2 servings), 4 = congee every day (7 servings = 3.5 batches), 0 = typical NUS student (calibration).\n"
            f"Calibrated: stress intercept b0 = {p['b0']}, workload -> stress = {p['s_AD_PAS']}, cooking link strength k_int = {p['k_int']}, "
            f"bad-habit propensity = {p['L_bad']} (healthy = {p['L_healthy']}). Same equations as model_v3.py; "
            "nominal values = a typical 20-unit student.")
    draw_png(OUT + "congee_sfd_v3.png", note)
    print("connectors:", len(CONN), "ghosts:", len(GHOSTS))

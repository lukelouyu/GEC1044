"""Check that the Stella file (.stmx) reproduces the Python model exactly.

Needs PySD (pip install pysd), which reads XMILE / Stella files. Run: python validate_stella.py
PySD reads Stella's 'discrete' graphical functions as straight-line interpolation, while Stella holds each value
until the next point (a step). For this check only, the weekly Academic Demands table is therefore rewritten as an
explicit step table (two points per week) in a temporary copy; every other equation is read exactly as Stella reads it.
"""
import json
import os
import re
import sys
import tempfile
import numpy as np
import pysd
import model_v3 as m

STMX = "../2_SFD_Stella/congee_model_v3.stmx"


def pysd_copy():
    text = open(STMX, encoding="utf-8").read()
    xs, ys = [], []
    for k, v in enumerate(m.DEMAND_TABLE):
        x0 = m.GF_XMIN + k
        xs += [x0, x0 + 0.9999]
        ys += [v, v]
    block = re.search(r'(<aux name="Academic Demands">.*?)<gf type="discrete">.*?</gf>', text, re.S)
    step = ('<gf type="continuous">\n<xpts>' + ",".join(f"{x:.4f}" for x in xs) + '</xpts>\n<ypts>'
            + ",".join(f"{y:.4f}" for y in ys) + '</ypts>\n</gf>')
    text = text[:block.start()] + block.group(1) + step + text[block.end():]
    path = os.path.join(tempfile.mkdtemp(), "congee_model_v3_pysd.xmile")
    open(path, "w", encoding="utf-8").write(text)
    return path


cal = json.load(open("calibration_v3.json"))
p = m.nominal(cal)
model = pysd.read_xmile(pysd_copy())
cols = ["Physical Wellbeing", "Mental Wellbeing", "Spleen Function", "Liver Qi Stagnation", "Qi Blood Generation",
        "Heart Blood Malnourishment", "Calm Shen", "Sleep Quality", "Fatigue", "Body Awareness", "Unhealthy Habits",
        "Mindfulness", "Rumination", "Perceived Stress", "Cooking Workload", "Servings Eaten"]
worst = 0.0
for constitution in (0, 1, 2):
    for name, sc in [("reference", m.REFERENCE)] + list(m.SCENARIOS.items()):
        st = model.run(params={"Scenario": sc["code"], "Constitution": constitution}, return_columns=cols)
        st = st[st.index > -1e-6].iloc[:-1]                 # semester days, TIME 0 .. 18 - DT
        py = m.run(dict(p, constitution=constitution), sc)
        d = max(float(np.max(np.abs(st[c].to_numpy() - py[c.replace(" ", "_")].ravel())))
                / (100 if "Wellbeing" in c else 1) for c in cols)
        worst = max(worst, d)
        print(f"constitution {constitution}  {name:34s} days={len(st)}  max |Stella file - Python| = {d:.1e}")
print(f"worst difference (0-1 scale): {worst:.1e}  ->  {'PASS' if worst < 1e-6 else 'FAIL'}")
sys.exit(0 if worst < 1e-6 else 1)

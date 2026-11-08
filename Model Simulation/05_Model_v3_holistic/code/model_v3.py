"""
Congee model v3 (TCM holistic) - one equation list used by BOTH the Python simulation and the Stella (.stmx) export.

v2 additions (compared with 04_Code/sim.py)
  * Cooking workload: batches x hours per batch. Costs study time (time squeeze -> stress), adds a little physical
    effort (fatigue accumulation) and works as a recovery break that drains study-induced ("external") fatigue.
  * Mindfulness of cooking: time spent cooking raises state mindfulness -> less rumination, better mental wellbeing.
  * Spleen function -> physical and mental wellbeing; unhealthy-habits stock (caffeine, cigarettes, alcohol, junk food).
v3 holistic additions (Zheng Ti Guan - holism; Zhi Wei Bing - treating the undiseased)
  * Liver Qi Stagnation stock (Five Elements: Liver Wood overacts Spleen Earth), fed by stress and rumination.
  * Qi & Blood Generation (from Spleen function and TCM practice) and Heart Blood / Shen Malnourishment
    (Heart-Spleen link: a weak Spleen and little qi-blood leave the Heart unnourished -> rumination, poor sleep).
  * Circadian Rhythm Disruption (Tian Ren He Yi): late nights driven by academic demands harm Spleen, Shen and sleep.
  * TCM Non-Pharmacological Practice (acupoint massage, Baduanjin) driven by self-care: soothes Liver, builds qi-blood.
  * Body Awareness (mindfulness x felt fatigue): early rest before fatigue becomes severe (balancing loop B4).
  * Individual Constitution (0 balanced, 1 Yin deficiency, 2 Yang deficiency): parameter switch on sleep and fatigue.

Conventions
  * Time unit: weeks. DT = 1/7 week (one day). Euler integration, as in Stella's default.
  * The run starts at week -8 (pre-semester holiday, no congee) so every scenario starts the semester from its own
    steady state. Semester weeks 1-18 are TIME 0-18.
  * State variables are 0-1 indices (1 = high level of that variable). Wellbeing outputs are 0-100.
  * Equations are in Stella/XMILE syntax; names use underscores for spaces. {param} placeholders are numbers:
    Python fills them with Monte-Carlo arrays, the Stella export fills them with nominal values (P0 + calibration).
"""
import re
import numpy as np

DT = 1 / 7
START, STOP = -8, 18
WAKING_H = 168 - 7 * 6.84          # Health@NUS mean sleep 6.84 h/night -> 120.1 waking hours/week


# ---------------------------------------------------------------------------------------------------------------
# Academic calendar (Academic Demands, exogenous): study hours / waking hours. NUS-calibrated shape from v1.
# ---------------------------------------------------------------------------------------------------------------
def _v1_profile():
    d = {w: 0.40 for w in range(1, 19)}
    d.update({1: 0.30, 2: 0.33, 3: 0.37})
    d[7] = 0.20
    d.update({8: 0.80, 9: 0.80})
    d[10] = 0.50
    d.update({11: 0.80, 12: 0.85, 13: 0.88, 14: 0.85})
    d[15] = 0.55
    d.update({16: 0.95, 17: 0.95})
    d[18] = 0.15
    return d


INSTR_WEEKS = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14]


def semester_demand():
    v1 = _v1_profile()
    mean_instr = np.mean([v1[w] for w in INSTR_WEEKS])
    return [v1[w] / mean_instr * 50.0 / WAKING_H for w in range(1, 19)]


HOLIDAY_DEMAND = 0.15
DEMAND_TABLE = [HOLIDAY_DEMAND] * 8 + [round(v, 4) for v in semester_demand()]   # weeks -8 .. 18 (26 values)
GF_XMIN = START - 0.001             # tiny offset so a time like 2.9999999 still reads the right week (float-safe)

PHASE = {**{w: "Teaching" for w in range(1, 19)}, 7: "Recess", 8: "Midterms", 9: "Midterms",
         11: "Submissions", 12: "Submissions", 13: "Submissions", 14: "Submissions",
         15: "Reading", 16: "Finals", 17: "Finals", 18: "Post-exam"}

# Constitution switch: (Yin-deficiency factor, Yang-deficiency factor)
CONSTITUTION = {0: ("Balanced", 1.0, 1.0), 1: ("Yin deficiency", 1.5, 1.0), 2: ("Yang deficiency", 1.0, 1.5)}

# ---------------------------------------------------------------------------------------------------------------
# Nominal parameters (Stella uses these; Monte Carlo samples around them - see sample_params)
# ---------------------------------------------------------------------------------------------------------------
P0 = dict(
    # recipe and workload (low-friction one-pot recipe, 2 portions per batch)
    servings_per_batch=2.0, h_per_batch=1.25, h50_break=2.5, h50_mind=2.5, potency=0.5, S50=3.5,
    # adherence
    a0=0.5, a_SE=0.3, a_H=0.35, b_W=0.25,
    # stress
    b0=0.24, resil=0.0, s_AD_PAS=0.42, s_FT_PAS=0.35, s_SC_PAS=0.30, s_TC_PAS=0.6,
    # rumination and mindfulness
    s_PAS_RU=0.70, s_SL_RU=0.30, s_MI_RU=0.30, s_HBM_RU=0.30, k_int=0.35,
    # Liver Qi Stagnation (Wood overacting Earth)
    l_PAS=0.60, l_RU=0.60, l0=0.60, l_NPI=0.80, k_LQ=1.0,
    # Spleen function (mass action: nourishment fills the gap, depletion drains the level)
    n0=0.22, n_f=0.30, d0=0.02, d_RU=0.10, d_LQS=0.10, d_UH=0.15, d_CRD=0.05, k_SF=1.0,
    # Qi & Blood, Heart Blood / Shen malnourishment
    qb_NPI=0.30, h0=0.645, h_SF=0.25, h_QB=0.25,
    # Calm Shen (Heart)
    c0=0.36, c_f=0.35, cd0=0.015, c_RU=0.40, c_UH=0.15, c_CRD=0.10, k_CS=1.0,
    # sleep
    s_UH_SL=0.30, s_CRD_SL=0.25, s_HBM_SL=0.30,
    # circadian disruption (share of late / all-night study nights rises with study load)
    cr_AD=1.1,
    # fatigue (effort-recovery)
    e_AD=1.43, e_cook=0.004, r0=0.23, r_SL=0.50, r_QB=0.50, r_RB=0.25, r_BAw=0.50, aw=2.0,
    # TCM non-pharmacological practice (acupoint massage, Baduanjin)
    npi0=0.30, npi_SE=0.60,
    # unhealthy habits
    mask=0.30, u_FT=0.50, u_PAS=0.30, u_dep=0.40, q0=0.60, q_SE=0.80, q_CR=0.30, tau_UH=1.5,
    # self-care
    s_PW_SE=0.40, s_MW_SE=0.45, s_UH_SE=0.35,
    # delays (weeks)
    tau_PAS=0.4, tau_RU=0.3, tau_MI=1.0, tau_SL=0.7, tau_SE=0.7, tau_SC=2.0, tau_H=3.0,
    # exogenous
    load=1.0, waking_h=round(WAKING_H, 2), constitution=0,
    # scenario levers (L_bad fitted in calibrate_v3.py)
    L_bad=7.5, L_healthy=0.35,
)

SCENARIOS = {
    "S1 No congee + bad habits": dict(code=1, planned=0.0, L="L_bad"),
    "S2 No congee + healthy lifestyle": dict(code=2, planned=0.0, L="L_healthy"),
    "S3 Congee once a week": dict(code=3, planned=2.0, L="L_healthy"),
    "S4 Congee every day": dict(code=4, planned=7.0, L="L_healthy"),
}
REFERENCE = dict(code=0, planned=0.0, L=1.0)   # typical NUS student, no congee: used for NUS calibration

# ---------------------------------------------------------------------------------------------------------------
# Model structure (Stella syntax)
# ---------------------------------------------------------------------------------------------------------------
STOCKS = {
    "Perceived_Stress":     dict(init=0.35, inflows=["Change_in_Stress"], outflows=[]),
    "Rumination":           dict(init=0.30, inflows=["Change_in_Rumination"], outflows=[]),
    "Mindfulness":          dict(init=0.20, inflows=["Change_in_Mindfulness"], outflows=[]),
    "Liver_Qi_Stagnation":  dict(init=0.35, inflows=["Qi_Stagnation_Buildup"], outflows=["Liver_Qi_Soothing"]),
    "Spleen_Function":      dict(init=0.60, inflows=["Spleen_Nourishment"], outflows=["Spleen_Depletion"]),
    "Calm_Shen":            dict(init=0.60, inflows=["Shen_Settling"], outflows=["Shen_Disturbance"]),
    "Sleep_Quality":        dict(init=0.60, inflows=["Change_in_Sleep"], outflows=[]),
    "Fatigue":              dict(init=0.35, inflows=["Fatigue_Accumulation"], outflows=["Fatigue_Recovery"]),
    "Unhealthy_Habits":     dict(init=0.25, inflows=["Habit_Uptake"], outflows=["Habit_Quitting"]),
    "Congee_Habit":         dict(init=0.0, inflows=["Congee_Habit_Change"], outflows=[]),
    "Self_Care_Engagement": dict(init=0.50, inflows=["Change_in_Self_Care"], outflows=[]),
    "Sense_of_Control":     dict(init=0.40, inflows=["Change_in_Control"], outflows=[]),
}

clip = lambda e: f"MIN(MAX({e}, 0), 1)"

FLOWS = {
    "Change_in_Stress": dict(biflow=True, eqn=(
        "(" + clip("{b0} - {resil} + {s_AD_PAS} * Study_Load + {s_FT_PAS} * (Felt_Fatigue - 0.4)"
                   " + {s_SC_PAS} * (0.45 - Sense_of_Control) + {s_TC_PAS} * Time_Squeeze")
        + " - Perceived_Stress) / {tau_PAS}")),
    "Change_in_Rumination": dict(biflow=True, eqn=(
        "(" + clip("0.05 + {s_PAS_RU} * Perceived_Stress + {s_SL_RU} * (0.6 - Sleep_Quality)"
                   " - {s_MI_RU} * (Mindfulness - 0.2) + {s_HBM_RU} * (Heart_Blood_Malnourishment - 0.35)")
        + " - Rumination) / {tau_RU}")),
    "Change_in_Mindfulness": dict(biflow=True, eqn="(0.2 + 0.6 * {k_int} * Mindful_Cooking - Mindfulness) / {tau_MI}"),
    "Qi_Stagnation_Buildup": dict(eqn=(
        "(1 - Liver_Qi_Stagnation) * ({l_PAS} * Perceived_Stress + {l_RU} * Rumination) * {k_LQ}")),
    "Liver_Qi_Soothing": dict(eqn="Liver_Qi_Stagnation * ({l0} + {l_NPI} * TCM_Practice) * {k_LQ}"),
    "Spleen_Nourishment": dict(eqn="(1 - Spleen_Function) * ({n0} + {n_f} * Spleen_Strengthening_Effect) * {k_SF}"),
    "Spleen_Depletion": dict(eqn=(
        "Spleen_Function * ({d0} + {d_RU} * Rumination + {d_LQS} * Liver_Qi_Stagnation"
        " + {d_UH} * Unhealthy_Habits + {d_CRD} * Circadian_Disruption) * {k_SF}")),
    "Shen_Settling": dict(eqn="(1 - Calm_Shen) * ({c0} + {c_f} * Shen_Calming_Effect) * {k_CS}"),
    "Shen_Disturbance": dict(eqn=(
        "Calm_Shen * ({cd0} + {c_RU} * Rumination + {c_UH} * Unhealthy_Habits + {c_CRD} * Circadian_Disruption)"
        " * {k_CS}")),
    "Change_in_Sleep": dict(biflow=True, eqn=(
        "(" + clip("0.15 + 0.75 * Calm_Shen - {s_UH_SL} * (Unhealthy_Habits - 0.2)"
                   " - {s_CRD_SL} * (Yin_Deficiency_Factor * Circadian_Disruption - 0.45)"
                   " - {s_HBM_SL} * (Yin_Deficiency_Factor * Heart_Blood_Malnourishment - 0.35)")
        + " - Sleep_Quality) / {tau_SL}")),
    "Fatigue_Accumulation": dict(eqn=(
        "(1 - Fatigue) * ({e_AD} * Yang_Deficiency_Factor * Study_Load + {e_cook} * Cooking_Workload)")),
    "Fatigue_Recovery": dict(eqn=(
        "Fatigue * ({r0} + {r_SL} * Sleep_Quality + {r_QB} * Qi_Blood_Generation + {r_RB} * Recovery_Break"
        " + {r_BAw} * Body_Awareness)")),
    "Habit_Uptake": dict(eqn=(
        "(1 - Unhealthy_Habits) * Lifestyle_Propensity * ({u_FT} * Felt_Fatigue + {u_PAS} * Perceived_Stress"
        " + {u_dep} * Unhealthy_Habits) / {tau_UH}")),
    "Habit_Quitting": dict(eqn=(
        "Unhealthy_Habits * ({q0} + {q_SE} * Self_Care_Engagement + {q_CR} * Servings_Eaten / 7) / {tau_UH}")),
    "Congee_Habit_Change": dict(biflow=True, eqn="(Adherence * MIN(Planned_Servings, 1) - Congee_Habit) / {tau_H}"),
    "Change_in_Self_Care": dict(biflow=True, eqn=(
        "(" + clip("0.55 + {s_PW_SE} * (Physical_Wellbeing / 100 - 0.6) + {s_MW_SE} * (Mental_Wellbeing / 100 - 0.55)"
                   " - {s_UH_SE} * (Unhealthy_Habits - 0.3)") + " - Self_Care_Engagement) / {tau_SE}")),
    "Change_in_Control": dict(biflow=True, eqn="(0.2 + 0.75 * Behavioural_Activation - Sense_of_Control) / {tau_SC}"),
}

# 'py' = Python form for converters that use IF/THEN/ELSE or a graphical function (gf) in Stella.
AUXES = {
    "Scenario": dict(eqn="4", py="P['scenario']",
                     doc="1 = no congee + bad habits; 2 = no congee + healthy lifestyle; 3 = congee once a week; "
                         "4 = congee every day; 0 = typical NUS student (calibration reference)"),
    "Constitution": dict(eqn="{constitution}", py="P['constitution']",
                         doc="Individual constitution (ti zhi): 0 = balanced, 1 = Yin deficiency, 2 = Yang deficiency"),
    "Yin_Deficiency_Factor": dict(eqn="Constitution", py="P['yin']", gf=dict(xmin=0, xmax=2, ypts=[1, 1.5, 1]),
                                  doc="Yin deficiency: the same late nights and Heart-blood deficiency disturb sleep 1.5x more"),
    "Yang_Deficiency_Factor": dict(eqn="Constitution", py="P['yang']", gf=dict(xmin=0, xmax=2, ypts=[1, 1, 1.5]),
                                   doc="Yang deficiency: the same study load builds fatigue 1.5x faster"),
    "Academic_Demands": dict(eqn="TIME", py="AD_t",
                             gf=dict(xmin=GF_XMIN, xmax=round(GF_XMIN + len(DEMAND_TABLE) - 1, 3), ypts=DEMAND_TABLE),
                             doc="Study hours / waking hours by semester week (NUS Registrar: 20 units = 50 h/week)"),
    "Course_Load": dict(eqn="{load}", doc="Units taken / 20 units"),
    "Study_Load": dict(eqn="Academic_Demands * Course_Load"),
    "Free_Hours": dict(eqn="{waking_h} * MAX(1 - Study_Load, 0.2)", doc="Waking hours left after study (hours/week)"),
    "Circadian_Disruption": dict(eqn=clip("{cr_AD} * Study_Load"),
                                 doc="Tian Ren He Yi: share of late or all-night study nights; rises with study load"),
    "Congee_Plan": dict(eqn="Scenario", py="P['planned']", gf=dict(xmin=0, xmax=4, ypts=[0, 0, 0, 2, 7]),
                        doc="Servings per week planned in each scenario: 3 -> 2 (one batch a week); 4 -> 7 (one bowl a day)"),
    "Planned_Servings": dict(eqn="IF TIME > -0.001 THEN Congee_Plan ELSE 0",
                             py="np.where(t > -0.001, V['Congee_Plan'], 0.0)",
                             doc="No congee during the pre-semester holiday; the plan starts in week 1"),
    "Lifestyle_Propensity": dict(eqn="Scenario", py="P['L']",
                                 gf=dict(xmin=0, xmax=4, ypts=["1", "{L_bad}", "{L_healthy}", "{L_healthy}", "{L_healthy}"]),
                                 doc="Tendency to cope with caffeine, cigarettes, alcohol and junk food"),
    "Adherence": dict(eqn=clip("{a0} + {a_SE} * (Self_Care_Engagement - 0.5) + {a_H} * Congee_Habit"
                               " - {b_W} * (Planned_Servings / 7) * Perceived_Stress"),
                      doc="Share of planned servings actually cooked and eaten; daily plans are dropped more under stress"),
    "Servings_Eaten": dict(eqn="Planned_Servings * Adherence"),
    "Batches_Cooked": dict(eqn="Servings_Eaten / {servings_per_batch}"),
    "Cooking_Workload": dict(eqn="Batches_Cooked * {h_per_batch}", doc="Hours per week spent preparing congee"),
    "Recovery_Break": dict(eqn="Cooking_Workload / (Cooking_Workload + {h50_break})",
                           doc="Detachment from study while cooking (saturating)"),
    "Mindful_Cooking": dict(eqn="Cooking_Workload / (Cooking_Workload + {h50_mind})",
                            doc="Present-moment attention practised while washing, cutting and simmering"),
    "Time_Squeeze": dict(eqn="Cooking_Workload / Free_Hours", doc="Share of free time used by cooking"),
    "Spleen_Strengthening_Effect": dict(eqn="{potency} * Servings_Eaten / (Servings_Eaten + {S50})",
                                        doc="Chinese yam + red date (jian pi yi qi), saturating dose-response"),
    "Shen_Calming_Effect": dict(eqn="{potency} * Servings_Eaten / (Servings_Eaten + {S50})",
                                doc="Lotus seed + red date (yang xin an shen), saturating dose-response"),
    "TCM_Practice": dict(eqn=clip("{npi0} + {npi_SE} * (Self_Care_Engagement - 0.5)"),
                         doc="TCM non-pharmacological interventions: acupoint massage, Baduanjin / gentle exercise"),
    "Qi_Blood_Generation": dict(eqn=clip("0.1 + 0.8 * Spleen_Function + {qb_NPI} * (TCM_Practice - 0.3)"),
                                doc="Qi and blood made by the Spleen (qi xue sheng hua zhi yuan); movement adds"),
    "Heart_Blood_Malnourishment": dict(eqn=clip("{h0} - {h_SF} * Spleen_Function - {h_QB} * Qi_Blood_Generation"),
                                       doc="Heart blood / shen malnourishment: rises when Spleen and qi-blood are weak"),
    "Behavioural_Activation": dict(eqn="0.25 + 0.6 * {k_int} * Batches_Cooked / (Batches_Cooked + 1)"),
    "Felt_Fatigue": dict(eqn="Fatigue * (1 - {mask} * Unhealthy_Habits)",
                         doc="Fatigue as felt; caffeine and nicotine mask part of it"),
    "Body_Awareness": dict(eqn=clip("{aw} * Mindfulness * Felt_Fatigue"),
                           doc="Zhi Wei Bing: noticing early tiredness (needs mindfulness and a felt signal) -> early rest"),
    "Physical_Wellbeing": dict(eqn="100 * (0.35 * Qi_Blood_Generation + 0.25 * Sleep_Quality + 0.40 * (1 - Fatigue))",
                               doc="0-100; uses true (unmasked) fatigue"),
    "Mental_Wellbeing": dict(eqn=("100 * (0.22 * (1 - Perceived_Stress) + 0.22 * (1 - Rumination)"
                                  " + 0.14 * Sense_of_Control + 0.18 * Calm_Shen + 0.12 * Spleen_Function"
                                  " + 0.12 * Mindfulness)"), doc="0-100, WHO-5-like scale"),
}

ALL_VARS = list(STOCKS) + list(FLOWS) + list(AUXES)
_IDENT = re.compile(r"\{(\w+)\}|\b([A-Za-z_][A-Za-z_0-9]*)\b")


def deps(eqn):
    """Model variables an equation reads (used for evaluation order and diagram connectors)."""
    out = []
    for mm in _IDENT.finditer(eqn):
        name = mm.group(2)
        if name and name in ALL_VARS and name not in out:
            out.append(name)
    return out


def _to_python(eqn):
    def rep(mm):
        if mm.group(1):
            return f"P['{mm.group(1)}']"
        name = mm.group(2)
        if name in ALL_VARS:
            return f"V['{name}']"
        return {"MIN": "np.minimum", "MAX": "np.maximum"}.get(name, name)
    return _IDENT.sub(rep, eqn)


def _aux_order():
    order, seen = [], set()

    def visit(n):
        if n in seen:
            return
        seen.add(n)
        for d in deps(AUXES[n]["eqn"]):
            if d in AUXES:
                visit(d)
        order.append(n)
    for n in AUXES:
        visit(n)
    return order


AUX_ORDER = _aux_order()
_CODE = {n: compile(AUXES[n].get("py") or _to_python(AUXES[n]["eqn"]), n, "eval") for n in AUX_ORDER}
_CODE.update({n: compile(_to_python(f["eqn"]), n, "eval") for n, f in FLOWS.items()})


def scenario_params(p, sc):
    """Attach scenario levers and constitution factors to a parameter dict."""
    q = dict(p)
    q["scenario"] = sc["code"]
    q["planned"] = sc["planned"]
    q["L"] = p[sc["L"]] if isinstance(sc["L"], str) else sc["L"]
    _, q["yin"], q["yang"] = CONSTITUTION[int(np.ravel(p.get("constitution", 0))[0])]
    return q


def run(p, sc, record=("all",), start=START, stop=STOP):
    """Euler integration from week -8 to 18, vectorised over Monte-Carlo samples (arrays in p).
    Returns dict of arrays (n_days, n_samples) for semester days t = 0 .. 18 - DT."""
    P = scenario_params(p, sc)
    shape = np.shape(np.asarray(P["b0"]) + np.asarray(P["tau_H"]) + np.asarray(P["load"]))
    V = {k: np.full(shape, float(s["init"])) for k, s in STOCKS.items()}
    n_steps = int(round((stop - start) / DT))
    rec = ALL_VARS if "all" in record else list(record)
    out = {k: [] for k in rec}
    out["t"] = []
    env = {"np": np, "P": P, "V": V}
    for i in range(n_steps):
        t = start + i * DT
        env["t"] = t
        wk_idx = min(max(int(np.floor(t - GF_XMIN)), 0), len(DEMAND_TABLE) - 1)
        env["AD_t"] = DEMAND_TABLE[wk_idx]           # discrete graphical function of TIME (one value per week)
        for n in AUX_ORDER:
            V[n] = np.broadcast_to(eval(_CODE[n], env), shape).astype(float)
        for n in FLOWS:
            V[n] = np.broadcast_to(eval(_CODE[n], env), shape).astype(float)
        if t > -1e-9:
            out["t"].append(t)
            for k in rec:
                out[k].append(V[k].copy())
        for k, s in STOCKS.items():                    # Euler: all flows computed from the same state, then update
            net = sum(V[f] for f in s["inflows"]) - sum(V[f] for f in s["outflows"])
            V[k] = V[k] + DT * net
    return {k: np.array(v) for k, v in out.items()}


def weekly(x):
    """Average daily values within each semester week -> shape (18, ...)."""
    return x.reshape(18, 7, *x.shape[1:]).mean(axis=1)


def sample_params(n, rng, cal=None, spread=0.3):
    """Monte-Carlo parameters. Link strengths without a direct quantitative source: uniform +/-30%.
    Source-informed distributions where a source exists (see 4_Sources/parameter_sources_v3.csv)."""
    keep = {"servings_per_batch", "waking_h", "L_bad", "L_healthy", "resil", "S50", "constitution"}
    p = {}
    for k, v in P0.items():
        p[k] = np.full(n, float(v)) if k in keep else v * rng.uniform(1 - spread, 1 + spread, n)
    p["tau_H"] = rng.lognormal(np.log(3.0), 0.55, n)            # Singh et al. 2024: median 59-66 days to habit
    p["tau_SL"] = rng.uniform(0.4, 1.2, n)                      # Lo et al. 2016: 2 recovery nights insufficient
    p["k_SF"] = 3.0 / rng.uniform(2.0, 6.0, n)                  # Spleen time constant 2-6 weeks
    p["k_CS"] = 1.67 / rng.uniform(1.0, 4.0, n)                 # Calm Shen time constant 1-4 weeks
    p["potency"] = rng.uniform(0.0, 1.0, n)                     # evidence-limited ingredient effect
    p["s_UH_SL"] = rng.uniform(0.2, 0.4, n)                     # Drake et al. 2013; Ebrahim et al. 2013
    p["h_per_batch"] = rng.uniform(1.0, 1.5, n)                 # recipe time 1.0-1.5 h per batch
    p["load"] = rng.choice([18 / 20, 20 / 20, 23 / 20], size=n, p=[0.10, 0.56, 0.34])   # NUS OSA 2024
    if cal:
        p["b0"] = np.full(n, cal["b0"])
        p["resil"] = rng.normal(0.0, cal["sd_resil"], n)
        p["s_AD_PAS"] = p["s_AD_PAS"] / P0["s_AD_PAS"] * cal["s_AD_PAS"]
        p["k_int"] = np.full(n, cal["k_int"])
        p["L_bad"] = np.full(n, cal["L_bad"])
    return p


def nominal(cal=None):
    """Nominal (single-student) parameter set with calibrated values. This is what the Stella file runs."""
    p = dict(P0)
    if cal:
        for k in ("b0", "s_AD_PAS", "k_int", "L_bad"):
            p[k] = round(float(cal[k]), 4)
    return p

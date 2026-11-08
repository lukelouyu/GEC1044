"""CLD v3, 20-variable version (IE2141 limit). Run: python cld_v3_20.py  -> loop audit

Built from the 27-variable holistic CLD (cld_v3.py) with seven merges. No feedback mechanism is lost; the SFD
(congee_model_v3.stmx) keeps the full detail.
  1. Planned Frequency      -> parameter tag on Congee Routine (scenario lever, not a variable)
  2. Individual Constitution -> parameter tag on Sleep Quality and Fatigue (moderator, not a variable)
  3. Spleen-Strengthening Effect + Shen-Calming Effect -> Food-Therapy Effect (yam, lotus seed, red date)
  4. Calm Shen -> folded into Heart Blood / Shen Malnourishment (its inverse); polarities flipped accordingly
  5. Behavioural Activation -> folded into Sense of Control (Congee Routine -> Sense of Control)
  6. Recovery Break -> net link Cooking Workload -(-) Fatigue (recovery break outweighs the small preparation effort)
  7. TCM Non-Pharmacological Interventions -> placed under Self-Care Engagement (Self-Care -> Liver, -> Qi & Blood)
"""
import networkx as nx

# id: (label, group, exogenous)   group: T = TCM, P = psychological/behavioural, S = shared, O = outcome, B = bridge
NODES = {
    "AD":  ("Academic Demands", "S", True),
    "CRD": ("Circadian Rhythm Disruption /\nAll-nighters (昼夜节律紊乱/熬夜)", "S", True),
    "PAS": ("Perceived\nAcademic Stress", "S", False),
    "UH":  ("Unhealthy Habits\n(caffeine, cigarettes,\nalcohol, junk food)", "S", False),
    "LQS": ("Liver Qi Stagnation\n(肝气郁结)", "B", False),
    "FTE": ("Food-Therapy Effect\n(yam, lotus seed, red date)", "T", False),
    "SF":  ("Spleen Function\n(Spleen Qi)", "T", False),
    "QB":  ("Qi & Blood Generation\n(气血生化)", "T", False),
    "HBM": ("Heart Blood / Shen\nMalnourishment (心血/心神失养)", "T", False),
    "SL":  ("Sleep Quality", "T", False),
    "FT":  ("Fatigue", "T", False),
    "PW":  ("Physical\nWellbeing", "O", False),
    "MW":  ("Mental\nWellbeing", "O", False),
    "CR":  ("Congee Routine\n(servings eaten)", "P", False),
    "CW":  ("Cooking Workload\n(prep hours/week)", "P", False),
    "MI":  ("Mindfulness", "P", False),
    "BAW": ("Body Awareness\n(身体觉察)", "P", False),
    "RU":  ("Rumination", "P", False),
    "SC":  ("Sense of Control\n(behavioural activation)", "P", False),
    "SE":  ("Self-Care Engagement\n(congee + TCM practice:\nacupoint massage, Baduanjin)", "P", False),
}

# (src, dst, polarity, delay, note)
EDGES = [
    ("AD", "PAS", "+", False, ""),
    ("AD", "FT", "+", False, "study effort = external fatigue"),
    ("AD", "CRD", "+", False, "exam weeks -> late nights"),
    ("CRD", "SF", "-", True, "staying up late consumes Yang qi"),
    ("CRD", "HBM", "+", False, "shen cannot return to the Heart at night (was CRD - Calm Shen)"),
    ("CRD", "SL", "-", False, ""),
    ("PAS", "RU", "+", False, ""),
    ("PAS", "LQS", "+", False, ""),
    ("PAS", "UH", "+", False, ""),
    ("PAS", "MW", "-", False, ""),
    ("RU", "LQS", "+", False, ""),
    ("RU", "SF", "-", True, "si lu shang pi"),
    ("RU", "HBM", "+", False, "worry disturbs the shen (was RU - Calm Shen)"),
    ("RU", "MW", "-", False, ""),
    ("LQS", "SF", "-", True, "Liver Wood overacts Spleen Earth"),
    ("SF", "QB", "+", False, ""),
    ("SF", "HBM", "-", False, ""),
    ("SF", "MW", "+", False, ""),
    ("QB", "HBM", "-", False, ""),
    ("QB", "FT", "-", False, ""),
    ("QB", "PW", "+", False, ""),
    ("HBM", "RU", "+", False, ""),
    ("HBM", "SL", "-", True, "sleep needs several nights to recover (was Calm Shen + || Sleep)"),
    ("HBM", "MW", "-", False, "(was Calm Shen + Mental Wellbeing)"),
    ("SL", "RU", "-", False, ""),
    ("SL", "FT", "-", False, ""),
    ("SL", "PW", "+", False, ""),
    ("FT", "PW", "-", False, ""),
    ("FT", "PAS", "+", False, ""),
    ("FT", "UH", "+", False, ""),
    ("FT", "BAW", "+", False, "early tiredness is a signal to notice (closes B4)"),
    ("UH", "SL", "-", False, ""),
    ("UH", "SF", "-", True, ""),
    ("UH", "FT", "-", False, "masks FELT fatigue (symptomatic fix)"),
    ("UH", "SE", "-", False, "reliance erodes self-care"),
    ("FTE", "SF", "+", True, "yam, red date: jian pi yi qi"),
    ("FTE", "HBM", "-", True, "lotus seed, red date: yang xin an shen"),
    ("CR", "FTE", "+", False, ""),
    ("CR", "CW", "+", False, ""),
    ("CR", "SC", "+", False, "each batch is a completed task (behavioural activation)"),
    ("CR", "UH", "-", False, "home-cooked meal replaces junk food"),
    ("CW", "FT", "-", False, "recovery break from study (net of the small preparation effort)"),
    ("CW", "MI", "+", False, "mindfulness of cooking"),
    ("CW", "PAS", "+", False, "time squeeze"),
    ("CW", "CR", "-", False, "preparation burden lowers adherence"),
    ("MI", "RU", "-", False, ""),
    ("MI", "MW", "+", False, ""),
    ("MI", "BAW", "+", False, ""),
    ("BAW", "FT", "-", False, "early rest (Zhi Wei Bing)"),
    ("SC", "PAS", "-", False, ""),
    ("SC", "MW", "+", False, ""),
    ("PW", "SE", "+", False, ""),
    ("MW", "SE", "+", False, ""),
    ("SE", "CR", "+", True, "habit formation"),
    ("SE", "LQS", "-", False, "TCM practice soothes the Liver"),
    ("SE", "QB", "+", False, "gentle movement builds qi and blood"),
]

# parameter tags drawn as notes, not variables: (text, anchor node)
TAGS = [("Scenario lever (parameter): planned frequency\nnone / once a week / every day", "CR"),
        ("Constitution switch (parameter): Yin deficiency x1.5 on\nsleep links; Yang deficiency x1.5 on fatigue build-up", "FT")]

NAMED = {
    "R1  stress-Spleen vicious cycle": ["PAS", "RU", "SF", "QB", "FT"],
    "R2  activation-control": ["CR", "SC", "MW", "SE"],
    "R3a ingredients -> Spleen -> qi & blood": ["CR", "FTE", "SF", "QB", "PW", "SE"],
    "R3b ingredients -> Shen -> sleep": ["CR", "FTE", "HBM", "SL", "FT", "PW", "SE"],
    "R4  rumination-sleep spiral": ["RU", "HBM", "SL"],
    "R5  Heart-Spleen deficiency": ["RU", "SF", "HBM"],
    "R5b worry-shen spiral": ["RU", "HBM"],
    "R6  cooking-mindfulness": ["CW", "MI", "RU", "MW", "SE", "CR"],
    "R7  recovery break": ["CW", "FT", "PW", "SE", "CR"],
    "R8  habits injure the Spleen": ["UH", "SF", "QB", "FT"],
    "R9  Liver Wood overacts Spleen Earth": ["PAS", "LQS", "SF", "QB", "FT"],
    "R10 Liver-Spleen-Heart rumination": ["RU", "LQS", "SF", "HBM"],
    "R11 TCM practice builds qi & blood": ["SE", "QB", "PW"],
    "R12 TCM practice soothes the Liver": ["SE", "LQS", "SF", "QB", "PW"],
    "R13 mindful awareness": ["CW", "MI", "BAW", "FT", "PW", "SE", "CR"],
    "B1  masking quick fix": ["FT", "UH"],
    "B2  time-cost brake": ["CR", "CW", "PAS", "MW", "SE"],
    "B3  workload brake": ["CR", "CW"],
    "B4  Zhi Wei Bing early-warning brake": ["FT", "BAW"],
    "STB-R dependency erodes self-care": ["UH", "SE", "CR", "FTE", "SF", "QB", "FT"],
}

# where each CLD variable lives in the Stella SFD (congee_model_v3.stmx)
SFD_MAP = {
    "Academic Demands": "Academic Demands (graphical function of TIME), Course Load, Study Load, Free Hours",
    "Circadian Rhythm Disruption": "Circadian Disruption",
    "Perceived Academic Stress": "stock Perceived Stress",
    "Unhealthy Habits": "stock Unhealthy Habits; Lifestyle Propensity; Felt Fatigue",
    "Liver Qi Stagnation": "stock Liver Qi Stagnation",
    "Food-Therapy Effect": "Spleen Strengthening Effect + Shen Calming Effect",
    "Spleen Function": "stock Spleen Function",
    "Qi & Blood Generation": "Qi Blood Generation",
    "Heart Blood / Shen Malnourishment": "Heart Blood Malnourishment + stock Calm Shen (inverse)",
    "Sleep Quality": "stock Sleep Quality",
    "Fatigue": "stock Fatigue; Felt Fatigue",
    "Physical / Mental Wellbeing": "Physical Wellbeing, Mental Wellbeing",
    "Congee Routine": "Congee Plan, Planned Servings, Adherence, Servings Eaten, stock Congee Habit",
    "Cooking Workload": "Batches Cooked, Cooking Workload, Recovery Break, Time Squeeze",
    "Mindfulness": "stock Mindfulness; Mindful Cooking",
    "Body Awareness": "Body Awareness",
    "Rumination": "stock Rumination",
    "Sense of Control": "stock Sense of Control + Behavioural Activation",
    "Self-Care Engagement": "stock Self Care Engagement + TCM Practice",
    "(parameters)": "Scenario (planned frequency, lifestyle); Constitution, Yin / Yang Deficiency Factor",
}


def graph():
    g = nx.DiGraph()
    for s, d, p, dl, note in EDGES:
        g.add_edge(s, d, pol=p, delay=dl)
    return g


def loop_type(g, path):
    negs = sum(g[path[i]][path[(i + 1) % len(path)]]["pol"] == "-" for i in range(len(path)))
    return negs, ("R" if negs % 2 == 0 else "B")


def audit(verbose=True):
    g = graph()
    assert len(NODES) == 20, len(NODES)
    assert set(g.nodes) == set(NODES), set(NODES) ^ set(g.nodes)
    rows = []
    for name, path in NAMED.items():
        for i in range(len(path)):
            assert g.has_edge(path[i], path[(i + 1) % len(path)]), (name, path[i], path[(i + 1) % len(path)])
        negs, t = loop_type(g, path)
        expected = name.split()[0].replace("STB-", "")[0]
        assert t == expected, (name, negs)
        rows.append((name, negs, t))
    cycles = list(nx.simple_cycles(g))
    n_r = sum(loop_type(g, c)[1] == "R" for c in cycles)
    if verbose:
        for name, negs, t in rows:
            print(f"{name:42s} negatives={negs} -> {t}")
        print(f"\nvariables={len(NODES)} (exogenous {sum(v[2] for v in NODES.values())}) links={len(EDGES)} "
              f"feedback cycles={len(cycles)} (reinforcing {n_r}, balancing {len(cycles) - n_r})")
    return rows, len(cycles), n_r


if __name__ == "__main__":
    audit()

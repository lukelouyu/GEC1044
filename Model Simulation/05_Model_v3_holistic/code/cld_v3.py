"""CLD v3 (TCM holistic): edge list and loop audit. Run: python cld_v3.py

Builds on CLD v2 (cld_v2.py) with the holistic TCM revision:
  + Liver Qi Stagnation (Five Elements: Liver Wood overacts Spleen Earth)
  + Qi & Blood Generation (replaces the v1 'Physical Energy'; Spleen Function now acts on Fatigue and Physical
    Wellbeing through it) and Heart Blood / Shen Malnourishment (replaces the v2 link Spleen Function -> Calm Shen;
    same Heart-Spleen rationale, now explicit)
  + Circadian Rhythm Disruption / all-nighters (Tian Ren He Yi), driven by Academic Demands
  + TCM Non-Pharmacological Interventions (acupoint massage, Baduanjin), driven by Self-Care Engagement
  + Body Awareness (Zhi Wei Bing early-warning loop B4). Fatigue -> Body Awareness (+) is added so that B4 closes:
    with only Mindfulness -> Body Awareness -> Fatigue the loop back to Mindfulness has two negative links (reinforcing).
  + Individual Constitution (exogenous parameter switch: Yin deficiency -> sleep, Yang deficiency -> fatigue)
"""
import networkx as nx

# id: (label, group, exogenous)   group: T = TCM, P = psychological/behavioural, S = shared, O = outcome, B = bridge
NODES = {
    "AD":  ("Academic Demands", "S", True),
    "CRD": ("Circadian Rhythm Disruption /\nAll-nighters (昼夜节律紊乱/熬夜)", "S", True),
    "CON": ("Individual Constitution (个体体质)\nYin deficiency / Yang deficiency", "T", True),
    "PF":  ("Planned Frequency\n(none / weekly / daily)", "P", True),
    "PAS": ("Perceived\nAcademic Stress", "S", False),
    "UH":  ("Unhealthy Habits\n(caffeine, cigarettes,\nalcohol, junk food)", "S", False),
    "LQS": ("Liver Qi Stagnation\n(肝气郁结)", "B", False),
    "SSE": ("Spleen-Strengthening\nEffect (yam, red date)", "T", False),
    "SHE": ("Shen-Calming Effect\n(lotus seed, red date)", "T", False),
    "SF":  ("Spleen Function\n(Spleen Qi)", "T", False),
    "QB":  ("Qi & Blood Generation\n(气血生化)", "T", False),
    "HBM": ("Heart Blood / Shen\nMalnourishment (心血/心神失养)", "T", False),
    "CS":  ("Calm Shen", "T", False),
    "SL":  ("Sleep Quality", "T", False),
    "FT":  ("Fatigue", "T", False),
    "PW":  ("Physical\nWellbeing", "O", False),
    "MW":  ("Mental\nWellbeing", "O", False),
    "CR":  ("Congee Routine\n(servings eaten)", "P", False),
    "CW":  ("Cooking Workload\n(prep hours/week)", "P", False),
    "RB":  ("Recovery Break\n(detachment)", "P", False),
    "MI":  ("Mindfulness", "P", False),
    "BAW": ("Body Awareness\n(身体觉察)", "P", False),
    "RU":  ("Rumination", "P", False),
    "BA":  ("Behavioural\nActivation", "P", False),
    "SC":  ("Sense of Control", "P", False),
    "SE":  ("Self-Care\nEngagement", "P", False),
    "NPI": ("TCM Non-Pharmacological\nInterventions (中医非药物干预)\nacupoint massage, Baduanjin", "P", False),
}

# (src, dst, polarity, delay, note). polarity 'm' = moderator (parameter switch), excluded from loop analysis.
EDGES = [
    ("AD", "PAS", "+", False, ""),
    ("AD", "FT", "+", False, "study effort = external fatigue"),
    ("AD", "CRD", "+", False, "NEW: exam weeks -> late nights and all-nighters"),
    ("CRD", "SF", "-", True, "NEW: staying up late consumes Yang qi and harms Spleen"),
    ("CRD", "CS", "-", False, "NEW: shen cannot return to the Heart at night"),
    ("CRD", "SL", "-", False, "NEW"),
    ("PAS", "RU", "+", False, ""),
    ("PAS", "LQS", "+", False, "NEW: emotional strain constrains Liver qi"),
    ("RU", "LQS", "+", False, "NEW: brooding stagnates qi"),
    ("LQS", "SF", "-", True, "NEW: Liver Wood overacts Spleen Earth (gan mu cheng pi)"),
    ("RU", "SF", "-", True, "si lu shang pi: overthinking injures the Spleen"),
    ("RU", "CS", "-", False, ""),
    ("SF", "QB", "+", False, "NEW: Spleen is the source of qi and blood"),
    ("SF", "HBM", "-", False, "NEW: healthy Spleen = material basis for the Heart"),
    ("QB", "HBM", "-", False, "NEW"),
    ("HBM", "RU", "+", False, "NEW: unnourished shen -> worry, overthinking"),
    ("HBM", "SL", "-", False, "NEW: blood fails to house shen at night -> insomnia"),
    ("QB", "FT", "-", False, "qi-blood = energy for recovery"),
    ("QB", "PW", "+", False, ""),
    ("SF", "MW", "+", False, "Spleen houses yi; brain-gut axis"),
    ("CS", "SL", "+", True, "sleep needs several nights to recover"),
    ("SL", "RU", "-", False, ""),
    ("SL", "FT", "-", False, ""),
    ("SL", "PW", "+", False, ""),
    ("FT", "PW", "-", False, ""),
    ("FT", "PAS", "+", False, "fatigue erodes coping capacity"),
    ("FT", "UH", "+", False, "tired -> kopi, energy drinks, cigarettes"),
    ("FT", "BAW", "+", False, "NEW (added to close B4): early tiredness is a signal to notice"),
    ("PAS", "UH", "+", False, "stress coping with alcohol, smoking, comfort food"),
    ("UH", "SL", "-", False, "caffeine, alcohol, nicotine disturb sleep"),
    ("UH", "SF", "-", True, "irregular, greasy, cold food and alcohol injure Spleen and Stomach"),
    ("UH", "FT", "-", False, "masks FELT fatigue in the short term (symptomatic fix)"),
    ("UH", "SE", "-", False, "reliance erodes self-care (Shifting the Burden)"),
    ("SSE", "SF", "+", True, "food-therapy tonification is cumulative"),
    ("SHE", "CS", "+", True, "shen-calming builds with repeated intake"),
    ("CR", "SSE", "+", False, ""),
    ("CR", "SHE", "+", False, ""),
    ("CR", "CW", "+", False, "more servings -> more batches to cook"),
    ("CR", "BA", "+", False, "each batch is a completed, valued task"),
    ("CR", "UH", "-", False, "a home-cooked meal replaces a takeaway or junk-food meal"),
    ("CW", "RB", "+", False, "cooking is a break from study"),
    ("RB", "FT", "-", False, "recovery drains study-induced fatigue"),
    ("CW", "FT", "+", False, "small physical effort of preparation"),
    ("CW", "MI", "+", False, "washing, cutting, stirring and waiting = informal mindfulness"),
    ("CW", "PAS", "+", False, "time squeeze: hours not spent studying"),
    ("CW", "CR", "-", False, "preparation burden lowers adherence, more so under stress"),
    ("MI", "RU", "-", False, ""),
    ("MI", "MW", "+", False, "present-moment calm and positive affect"),
    ("MI", "BAW", "+", False, "NEW: mindfulness sharpens interoception"),
    ("BAW", "FT", "-", False, "NEW: early rest / self-care before fatigue becomes severe"),
    ("BA", "SC", "+", False, ""),
    ("SC", "PAS", "-", False, ""),
    ("SC", "MW", "+", False, ""),
    ("PAS", "MW", "-", False, ""),
    ("RU", "MW", "-", False, ""),
    ("CS", "MW", "+", False, ""),
    ("PW", "SE", "+", False, ""),
    ("MW", "SE", "+", False, ""),
    ("SE", "CR", "+", True, "habit formation (median 59-66 days)"),
    ("SE", "NPI", "+", False, "NEW: self-care also takes non-food TCM forms"),
    ("NPI", "LQS", "-", False, "NEW: acupoint massage / Baduanjin soothe the Liver (shu gan)"),
    ("NPI", "QB", "+", False, "NEW: gentle movement generates Yang and qi-blood"),
    ("PF", "CR", "+", False, "scenario lever"),
    ("CON", "SL", "m", False, "Yin deficiency: same stressors -> worse insomnia"),
    ("CON", "FT", "m", False, "Yang deficiency: same study load -> more fatigue"),
]

NAMED = {
    "R1  stress-Spleen vicious cycle": ["PAS", "RU", "SF", "QB", "FT"],
    "R2  activation-control": ["CR", "BA", "SC", "MW", "SE"],
    "R3a ingredient -> Spleen -> qi & blood": ["CR", "SSE", "SF", "QB", "PW", "SE"],
    "R3b ingredient -> Shen": ["CR", "SHE", "CS", "SL", "FT", "PW", "SE"],
    "R4  rumination-sleep spiral": ["RU", "CS", "SL"],
    "R5  Heart-Spleen deficiency (xin pi liang xu)": ["RU", "SF", "HBM"],
    "R6  cooking-mindfulness": ["CW", "MI", "RU", "MW", "SE", "CR"],
    "R7  recovery break": ["CW", "RB", "FT", "PW", "SE", "CR"],
    "R8  habits injure the Spleen (Fixes that Fail)": ["UH", "SF", "QB", "FT"],
    "R9  Liver Wood overacts Spleen Earth (new)": ["PAS", "LQS", "SF", "QB", "FT"],
    "R10 Liver-Spleen-Heart rumination loop (new)": ["RU", "LQS", "SF", "HBM"],
    "R11 TCM practice builds qi & blood (new)": ["SE", "NPI", "QB", "PW"],
    "R12 TCM practice soothes the Liver (new)": ["SE", "NPI", "LQS", "SF", "QB", "PW"],
    "R13 mindful awareness loop (new)": ["CW", "MI", "BAW", "FT", "PW", "SE", "CR"],
    "B1  masking quick fix (STB symptomatic)": ["FT", "UH"],
    "B2  time-cost brake": ["CR", "CW", "PAS", "MW", "SE"],
    "B3  workload brake": ["CR", "CW"],
    "B4  Zhi Wei Bing early-warning brake (new)": ["FT", "BAW"],
    "STB-R dependency erodes self-care": ["UH", "SE", "CR", "SSE", "SF", "QB", "FT"],
}


def graph():
    g = nx.DiGraph()
    for s, d, p, dl, note in EDGES:
        if p != "m":
            g.add_edge(s, d, pol=p, delay=dl)
    return g


def loop_type(g, path):
    negs = sum(g[path[i]][path[(i + 1) % len(path)]]["pol"] == "-" for i in range(len(path)))
    return negs, ("R" if negs % 2 == 0 else "B")


def audit(verbose=True):
    g = graph()
    used = {s for s, *_ in EDGES} | {d for _, d, *_ in EDGES}
    assert used == set(NODES), used ^ set(NODES)
    rows = []
    for name, path in NAMED.items():
        for i in range(len(path)):
            assert g.has_edge(path[i], path[(i + 1) % len(path)]), (name, path[i], path[(i + 1) % len(path)])
        negs, t = loop_type(g, path)
        expected = name.split()[0].replace("STB-", "")[0]
        assert t == expected, (name, negs)         # loop letter must match the count of negative links
        rows.append((name, negs, t))
    # the user-specified B4 links alone (without Fatigue -> Body Awareness) give a reinforcing loop:
    g2 = g.copy()
    g2.remove_edge("FT", "BAW")
    b4_alone = [c for c in nx.simple_cycles(g2) if "BAW" in c]
    cycles = list(nx.simple_cycles(g))
    n_r = sum(loop_type(g, c)[1] == "R" for c in cycles)
    if verbose:
        for name, negs, t in rows:
            print(f"{name:50s} negatives={negs} -> {t}")
        print(f"\nvariables={len(NODES)} (exogenous {sum(v[2] for v in NODES.values())}) links={len(EDGES)} "
              f"(causal {g.number_of_edges()}, moderator {len(EDGES) - g.number_of_edges()}) "
              f"feedback cycles={len(cycles)} (reinforcing {n_r}, balancing {len(cycles) - n_r})")
        print(f"cycles through Body Awareness WITHOUT Fatigue -> Body Awareness: {len(b4_alone)}, "
              f"balancing: {sum(loop_type(g2, c)[1] == 'B' for c in b4_alone)}")
    return rows, len(cycles), n_r


if __name__ == "__main__":
    audit()

"""CLD v2: edge list, loop audit and figure. Run: python cld_v2.py  -> ../1_CLD/congee_cld_v2.png + loop audit printout.

20 variables (IE2141 limit). Changes from v1:
  + Cooking Workload and Recovery Break (preparation time: costs study time, but gives a break that drains
    study-induced fatigue), Academic Demands -> Fatigue (external fatigue)
  + Mindfulness now comes from time spent cooking (Cooking Workload -> Mindfulness) and feeds Mental Wellbeing
  + Spleen Function -> Calm Shen, Physical Wellbeing and Mental Wellbeing (explicit outcome variables)
  + Unhealthy Habits (caffeine, cigarettes, alcohol, junk food) inside the main CLD (was an overlay)
  + Planned Frequency (exogenous; the scenario lever: none / weekly / daily)
  - Coping Capacity (now Fatigue -> Stress directly), Available Study Time (now Cooking Workload -> Stress),
    Physical Energy (folded into Spleen Function and Physical Wellbeing), Low-Friction Cooking (now the
    hours-per-batch parameter of Cooking Workload), Quick-Relief Use / Reliance (merged into Unhealthy Habits)
"""
import networkx as nx

# id: (label, group, exogenous)   group: T = TCM, P = psychological/behavioural, S = shared, O = outcome
NODES = {
    "AD":  ("Academic Demands", "S", True),
    "PF":  ("Planned Frequency\n(none / weekly / daily)", "P", True),
    "PAS": ("Perceived\nAcademic Stress", "S", False),
    "UH":  ("Unhealthy Habits\n(caffeine, cigarettes,\nalcohol, junk food)", "S", False),
    "SSE": ("Spleen-Strengthening\nEffect (yam, red date)", "T", False),
    "SHE": ("Shen-Calming Effect\n(lotus seed, red date)", "T", False),
    "SF":  ("Spleen Function\n(Spleen Qi)", "T", False),
    "CS":  ("Calm Shen", "T", False),
    "SL":  ("Sleep Quality", "T", False),
    "FT":  ("Fatigue", "T", False),
    "PW":  ("Physical\nWellbeing", "O", False),
    "MW":  ("Mental\nWellbeing", "O", False),
    "CR":  ("Congee Routine\n(servings eaten)", "P", False),
    "CW":  ("Cooking Workload\n(prep hours/week)", "P", False),
    "RB":  ("Recovery Break\n(detachment)", "P", False),
    "MI":  ("Mindfulness", "P", False),
    "RU":  ("Rumination", "P", False),
    "BA":  ("Behavioural\nActivation", "P", False),
    "SC":  ("Sense of Control", "P", False),
    "SE":  ("Self-Care\nEngagement", "P", False),
}

# (src, dst, polarity, delay, note)
EDGES = [
    ("AD", "PAS", "+", False, ""),
    ("AD", "FT", "+", False, "study effort = external fatigue"),
    ("PAS", "RU", "+", False, ""),
    ("RU", "SF", "-", True, "si lu shang pi: overthinking injures the Spleen"),
    ("RU", "CS", "-", False, ""),
    ("SF", "CS", "+", False, "Spleen makes qi and blood that nourish the Heart (Heart-Spleen link)"),
    ("SF", "FT", "-", False, "Spleen governs the limbs; Spleen qi = energy for recovery"),
    ("SF", "PW", "+", False, "NEW: Spleen -> physical wellbeing"),
    ("SF", "MW", "+", False, "NEW: Spleen -> mental wellbeing (Spleen houses yi; brain-gut axis)"),
    ("CS", "SL", "+", True, "sleep needs several nights to recover"),
    ("SL", "RU", "-", False, ""),
    ("SL", "FT", "-", False, ""),
    ("SL", "PW", "+", False, ""),
    ("FT", "PW", "-", False, ""),
    ("FT", "PAS", "+", False, "fatigue erodes coping capacity"),
    ("FT", "UH", "+", False, "tired -> kopi, energy drinks, cigarettes"),
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
    ("RB", "FT", "-", False, "NEW: recovery drains study-induced fatigue"),
    ("CW", "FT", "+", False, "NEW: small physical effort of preparation"),
    ("CW", "MI", "+", False, "NEW: washing, cutting, stirring and waiting = informal mindfulness"),
    ("CW", "PAS", "+", False, "time squeeze: hours not spent studying"),
    ("CW", "CR", "-", False, "NEW: preparation burden lowers adherence, more so under stress"),
    ("MI", "RU", "-", False, ""),
    ("MI", "MW", "+", False, "NEW: present-moment calm and positive affect"),
    ("BA", "SC", "+", False, ""),
    ("SC", "PAS", "-", False, ""),
    ("SC", "MW", "+", False, ""),
    ("PAS", "MW", "-", False, ""),
    ("RU", "MW", "-", False, ""),
    ("CS", "MW", "+", False, ""),
    ("PW", "SE", "+", False, ""),
    ("MW", "SE", "+", False, ""),
    ("SE", "CR", "+", True, "habit formation (median 59-66 days)"),
    ("PF", "CR", "+", False, "scenario lever"),
]

NAMED = {
    "R1  stress-Spleen vicious cycle": ["PAS", "RU", "SF", "FT"],
    "R2  activation-control": ["CR", "BA", "SC", "MW", "SE"],
    "R3a ingredient -> Spleen": ["CR", "SSE", "SF", "PW", "SE"],
    "R3b ingredient -> Shen": ["CR", "SHE", "CS", "SL", "FT", "PW", "SE"],
    "R4  rumination-sleep spiral": ["RU", "CS", "SL"],
    "R5  Heart-Spleen loop (new)": ["RU", "SF", "CS", "SL"],
    "R6  cooking-mindfulness loop (new)": ["CW", "MI", "RU", "MW", "SE", "CR"],
    "R7  recovery-break loop (new)": ["CW", "RB", "FT", "PW", "SE", "CR"],
    "R8  habits injure the Spleen (Fixes that Fail)": ["UH", "SF", "FT"],
    "B1  masking quick fix (STB symptomatic)": ["FT", "UH"],
    "B2  time-cost brake": ["CR", "CW", "PAS", "MW", "SE"],
    "B3  workload brake (new)": ["CR", "CW"],
    "STB-R dependency erodes self-care": ["UH", "SE", "CR", "SSE", "SF", "FT"],
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
    assert len(NODES) <= 20, len(NODES)
    assert set(g.nodes) == set(NODES), set(NODES) ^ set(g.nodes)
    rows = []
    for name, path in NAMED.items():
        for i in range(len(path)):
            assert g.has_edge(path[i], path[(i + 1) % len(path)]), (name, path[i], path[(i + 1) % len(path)])
        negs, t = loop_type(g, path)
        expected = name.split()[0].replace("STB-", "")[0]
        assert t == expected, (name, negs)         # label letter must match the negative-link count
        rows.append((name, negs, t))
    cycles = list(nx.simple_cycles(g))
    n_r = sum(loop_type(g, c)[1] == "R" for c in cycles)
    if verbose:
        for name, negs, t in rows:
            print(f"{name:48s} negatives={negs} -> {t}")
        print(f"\nvariables={len(NODES)} links={len(EDGES)} feedback cycles={len(cycles)} "
              f"(reinforcing {n_r}, balancing {len(cycles) - n_r})")
    return rows, len(cycles), n_r


if __name__ == "__main__":
    audit()

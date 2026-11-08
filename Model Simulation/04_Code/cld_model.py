"""IE2141 CLD: congee intervention. Single source of truth for edges, loop audit and Mermaid output."""
import networkx as nx

NODES = {
    # id: (label, subsystem, exogenous?)
    "AD":  ("Academic Demands", "S", True),
    "PAS": ("Perceived Academic Stress", "S", False),
    "CC":  ("Coping Capacity", "S", False),
    "SQ":  ("Spleen Qi", "T", False),
    "SSE": ("Spleen-Strengthening Effect<br/>(yam, red date)", "T", False),
    "SHE": ("Shen-Calming Effect<br/>(lotus seed, red date)", "T", False),
    "CS":  ("Calm Shen", "T", False),
    "SL":  ("Sleep Quality", "T", False),
    "PE":  ("Physical Energy", "T", False),
    "FT":  ("Fatigue", "T", False),
    "RU":  ("Rumination", "P", False),
    "MI":  ("Mindfulness", "P", False),
    "CR":  ("Congee Routine<br/>(adherence)", "P", False),
    "BA":  ("Behavioural Activation", "P", False),
    "SC":  ("Sense of Control", "P", False),
    "SE":  ("Self-Care Engagement", "P", False),
    "LF":  ("Low-Friction Cooking", "P", True),
    "AT":  ("Available Study Time", "S", False),
}

# (src, dst, polarity, delay, designed_link)
EDGES = [
    ("AD", "PAS", "+", False, False),
    ("PAS", "RU", "+", False, False),
    ("RU", "SQ", "-", True, False),    # 思虑伤脾
    ("SQ", "PE", "+", False, False),
    ("PE", "FT", "-", False, False),
    ("SL", "FT", "-", False, False),
    ("FT", "CC", "-", False, False),
    ("CC", "PAS", "-", False, False),
    ("RU", "CS", "-", False, False),
    ("CS", "SL", "+", True, False),    # sleep recovery
    ("SL", "RU", "-", False, False),
    ("SSE", "SQ", "+", True, False),   # cumulative tonification
    ("SHE", "CS", "+", True, False),   # cumulative shen-calming
    ("CR", "SSE", "+", False, False),
    ("CR", "SHE", "+", False, False),
    ("PE", "SE", "+", False, False),
    ("FT", "SE", "-", False, False),
    ("SE", "CR", "+", True, False),    # habit formation
    ("LF", "CR", "+", False, False),
    ("CR", "BA", "+", False, False),
    ("BA", "SC", "+", False, False),
    ("SC", "PAS", "-", False, False),
    ("PAS", "SE", "-", False, False),
    ("CR", "MI", "+", False, False),
    ("MI", "RU", "-", False, False),
    ("RU", "CR", "+", False, True),    # designed 'simmer-as-pause' cue
    ("CR", "AT", "-", False, False),   # time cost of soaking/simmering
    ("AT", "PAS", "-", False, False),
]

NAMED = {
    "R1": ["PAS", "RU", "SQ", "PE", "FT", "CC"],
    "R2": ["CR", "BA", "SC", "PAS", "SE"],
    "B1": ["RU", "CR", "MI"],
    "R3a": ["CR", "SSE", "SQ", "PE", "SE"],
    "R3b": ["CR", "SHE", "CS", "SL", "FT", "SE"],
    "R4": ["RU", "CS", "SL"],
    "B2": ["CR", "AT", "PAS", "SE"],
}


def graph():
    g = nx.DiGraph()
    for s, d, p, dl, des in EDGES:
        g.add_edge(s, d, pol=p, delay=dl, designed=des)
    return g


def audit():
    g = graph()
    assert len(NODES) <= 20
    cycles = list(nx.simple_cycles(g))
    rows = []
    for c in cycles:
        negs = sum(g[c[i]][c[(i + 1) % len(c)]]["pol"] == "-" for i in range(len(c)))
        des = any(g[c[i]][c[(i + 1) % len(c)]]["designed"] for i in range(len(c)))
        rows.append((len(c), "R" if negs % 2 == 0 else "B", negs, des, c))
    # check named loops are actual cycles
    for name, path in NAMED.items():
        for i in range(len(path)):
            assert g.has_edge(path[i], path[(i + 1) % len(path)]), (name, path[i])
        negs = sum(g[path[i]][path[(i + 1) % len(path)]]["pol"] == "-" for i in range(len(path)))
        print(f"{name}: negs={negs} -> {'R' if negs % 2 == 0 else 'B'}")
    print(f"\nvariables={len(NODES)} links={len(EDGES)} cycles={len(cycles)}")
    for r in sorted(rows):
        print(r[1], r[2], "designed" if r[3] else "", " -> ".join(NODES[n][0].split('<br/>')[0] for n in r[4]))
    # loops if the designed cue link is removed
    g2 = g.copy(); g2.remove_edge("RU", "CR")
    b = [c for c in nx.simple_cycles(g2)
         if sum(g2[c[i]][c[(i + 1) % len(c)]]["pol"] == "-" for i in range(len(c))) % 2]
    print("\nbalancing loops without designed cue:", len(b))
    for c in b: print("   ", " -> ".join(NODES[n][0].split('<br/>')[0] for n in c))


if __name__ == "__main__":
    audit()

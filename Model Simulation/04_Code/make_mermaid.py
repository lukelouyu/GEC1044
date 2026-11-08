"""Generate the two Mermaid diagrams from cld_model.py so labels, polarity and colour indices never drift."""
from cld_model import NODES, EDGES

INIT = '%%{init: {"theme": "base", "themeVariables": {"fontSize": "15px", "edgeLabelBackground": "#FFFFFF", "lineColor": "#4A4A4A"}, "themeCSS": ".edgeLabel, .edgeLabel p, .edgeLabel span { font-size: 20px !important; font-weight: 700; color: #111111; }", "flowchart": {"curve": "basis", "nodeSpacing": 45, "rankSpacing": 70}}}%%'
DASH = "–"
COL = {"T": "#9A4A00", "P": "#006D77", "S": "#4A4A4A"}   # edge colours
CLASSDEFS = """    classDef tcm fill:#FFE6BF,stroke:#9A4A00,stroke-width:2px,color:#2E1A00;
    classDef psy fill:#D3EEF2,stroke:#006D77,stroke-width:2px,color:#00262A;
    classDef shared fill:#EDEDED,stroke:#4A4A4A,stroke-width:2px,color:#111111;
    classDef exo fill:#FFFFFF,stroke:#4A4A4A,stroke-width:2px,stroke-dasharray:6 3,color:#111111;
    classDef exoPsy fill:#FFFFFF,stroke:#006D77,stroke-width:2px,stroke-dasharray:6 3,color:#00262A;
    classDef loopR fill:#FFFFFF,stroke:#B00020,stroke-width:2px,color:#B00020,font-weight:bold;
    classDef loopB fill:#FFFFFF,stroke:#1B5E20,stroke-width:2px,color:#1B5E20,font-weight:bold;
    classDef legend fill:#FAFAFA,stroke:#9E9E9E,stroke-width:1px,color:#111111,text-align:left;"""


def node_decl(nid):
    label, sub, exo = NODES[nid]
    cls = {"T": "tcm", "P": "psy", "S": "shared"}[sub]
    if exo:
        cls = "exoPsy" if sub == "P" else "exo"
        return f'{nid}[["{label}<br/><i>exogenous</i>"]]:::{cls}'
    return f'{nid}("{label}"):::{cls}'


def edge_line(s, d, pol, delay, designed):
    lab = ("+" if pol == "+" else DASH) + (" ||" if delay else "")
    if designed:
        return f'{s} -. "{lab}" .-> {d}'
    return f'{s} -- "{lab}" --> {d}'


def edge_colour(s, d):
    a, b = NODES[s][1], NODES[d][1]
    return COL[a] if a == b else COL["S"]   # cross-subsystem -> neutral


def main_cld():
    L = ["%% IE2141 CLD: congee intervention for time-constrained NUS students",
         "%% Generated from cld_model.py. 18 variables, 28 causal links.",
         INIT, "flowchart LR"]
    L.append('    subgraph A["Subsystem A: TCM Physiological"]')
    for n in ["SSE", "SHE", "SQ", "CS", "PE", "SL", "FT"]:
        L.append("        " + node_decl(n))
    L.append("    end")
    L.append('    subgraph SH["Shared drivers and coupling"]')
    for n in ["AD", "PAS", "CC", "AT"]:
        L.append("        " + node_decl(n))
    L.append("    end")
    L.append('    subgraph B["Subsystem B: Psychological / Behavioural"]')
    for n in ["LF", "SE", "CR", "BA", "SC", "MI", "RU"]:
        L.append("        " + node_decl(n))
    L.append("    end")

    styles, idx = [], 0
    L.append("    %% ---- causal links (polarity on every edge; || = material delay; dotted = designed decision rule)")
    for e in EDGES:
        L.append("    " + edge_line(*e))
        w = "2.5px" if NODES[e[0]][1] != NODES[e[1]][1] else "2px"
        extra = ",stroke-dasharray:5 4" if e[4] else ""
        styles.append(f"    linkStyle {idx} stroke:{edge_colour(e[0], e[1])},stroke-width:{w}{extra};")
        idx += 1

    # loop markers, tethered by invisible links (these also count as link indices)
    loops = [("R1", "R1 · stress–Spleen<br/>vicious cycle", "loopR", "FT"),
             ("R2", "R2 · activation–control<br/>virtuous loop", "loopR", "SC"),
             ("B1", "B1 · simmer-as-pause<br/>mindfulness brake", "loopB", "MI"),
             ("R3", "R3a/R3b · ingredient<br/>reinforcement", "loopR", "SSE"),
             ("R4", "R4 · rumination–sleep<br/>spiral (secondary)", "loopR", "SL"),
             ("B2", "B2 · time-cost brake<br/>(secondary)", "loopB", "AT")]
    L.append("    %% ---- loop identifiers (annotations, not variables)")
    for lid, text, cls, anchor in loops:
        L.append(f'    {lid}_lbl(("{text}")):::{cls}')
        L.append(f"    {anchor} ~~~ {lid}_lbl")
        idx += 1

    L.append('    subgraph LEG["Legend"]')
    L.append("        direction TB")
    L.append('        LG1["<b>Amber node</b> = TCM physiological variable<br/><b>Teal node</b> = psychological / behavioural variable<br/><b>Grey node</b> = shared driver or coupling variable<br/><b>Dashed box</b> = exogenous input (not in any loop)"]:::legend')
    L.append('        LG2["<b>+</b> = same-direction change · <b>–</b> = opposite-direction change<br/><b>||</b> on a label = material time delay on that link<br/><b>Amber / teal edge</b> = link inside one subsystem<br/><b>Grey edge (thicker)</b> = cross-subsystem coupling<br/><b>Dotted edge</b> = designed decision rule (intervention)"]:::legend')
    L.append('        LG3["<b>Red circle R</b> = reinforcing loop (even number of – links)<br/><b>Green circle B</b> = balancing loop (odd number of – links)"]:::legend')
    L.append("        LG1 ~~~ LG2 ~~~ LG3")
    idx += 2
    L.append("    end")
    L.append(CLASSDEFS)
    L.extend(styles)
    return "\n".join(L) + "\n"


def stb():
    lab = {"FT": "Fatigue<br/>(problem symptom)",
           "QR": "Quick-Relief Use<br/>(kopi / energy drinks, delivery<br/>or skipped meals, scrolling)",
           "DEP": "Reliance on Quick Relief<br/>(side effect)",
           "SE": "Self-Care Engagement",
           "CR": "Congee Routine<br/>(fundamental solution)",
           "SSE": "Spleen-Strengthening Effect",
           "SQ": "Spleen Qi", "PE": "Physical Energy", "SL": "Sleep Quality"}
    cls = {"FT": "tcm", "QR": "shared", "DEP": "shared", "SE": "psy", "CR": "psy",
           "SSE": "tcm", "SQ": "tcm", "PE": "tcm", "SL": "tcm"}
    E = [("FT", "QR", "+", False, False, "S"),
         ("QR", "FT", "-", False, False, "S"),
         ("FT", "SE", "+", False, True, "S"),
         ("SE", "CR", "+", True, False, "P"),
         ("CR", "SSE", "+", False, False, "S"),
         ("SSE", "SQ", "+", True, False, "T"),
         ("SQ", "PE", "+", False, False, "T"),
         ("PE", "FT", "-", False, False, "T"),
         ("QR", "DEP", "+", True, False, "S"),
         ("DEP", "SE", "-", False, False, "S"),
         ("QR", "SL", "-", False, False, "S"),
         ("SL", "FT", "-", False, False, "T")]
    L = ["%% Shifting the Burden overlay (archetype loops labelled STB-* to avoid clashing with R1-R4, B1-B2)",
         INIT, "flowchart LR"]
    for n, t in lab.items():
        L.append(f'    {n}("{t}"):::{cls[n]}')
    styles = []
    for i, (s, d, p, dl, des, k) in enumerate(E):
        L.append("    " + edge_line(s, d, p, dl, des))
        extra = ",stroke-dasharray:5 4" if des else ""
        styles.append(f"    linkStyle {i} stroke:{COL[k]},stroke-width:2px{extra};")
    n = len(E)
    for lid, text, c, anc in [("SYM", "STB-B_sym<br/>quick relief", "loopB", "QR"),
                              ("FUND", "STB-B_fund<br/>slow fundamental fix", "loopB", "SSE"),
                              ("DEPL", "STB-R_dep<br/>dependency erodes<br/>self-care", "loopR", "DEP"),
                              ("FTF", "FtF-R<br/>caffeine → sleep<br/>(Fixes that Fail)", "loopR", "SL")]:
        L.append(f'    {lid}(("{text}")):::{c}')
        L.append(f"    {anc} ~~~ {lid}")
        n += 1
    L.append(CLASSDEFS)
    L.extend(styles)
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    open("congee_cld.mmd", "w").write(main_cld())
    open("congee_stb.mmd", "w").write(stb())
    print("ok")

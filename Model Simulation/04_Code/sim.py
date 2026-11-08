"""
Semester simulation of the IE2141 congee CLD (qualitative model -> illustrative stock-flow).
Time unit: weeks. dt = 1 day. All variables are 0-1 indices (1 = high level of the variable).

Every causal term below corresponds to a CLD link; the sign of the coefficient is the link polarity.
Stocks (first-order adjustment) implement the CLD delays (||) and short perception lags.
"""
import numpy as np

DT = 1 / 7
WEEKS = 18

# ---------------- academic calendar (Academic Demands, exogenous) ----------------
# wk1-6 teaching, wk7 recess, wk8-14 teaching (8-9 midterms, 11-14 submissions),
# wk15 recess/reading, wk16-17 finals, wk18 post-exam.
def _v1_profile():
    d = {w: 0.40 for w in range(1, 19)}
    d.update({1: 0.30, 2: 0.33, 3: 0.37})          # semester ramp-up
    d[7] = 0.20                                      # recess
    d.update({8: 0.80, 9: 0.80})                     # midterms
    d[10] = 0.50
    d.update({11: 0.80, 12: 0.85, 13: 0.88, 14: 0.85})  # submission weeks
    d[15] = 0.55                                     # reading week (revision)
    d.update({16: 0.95, 17: 0.95})                   # final exams
    d[18] = 0.15                                     # after exams
    return d

def demand_profile_v1():
    return _v1_profile()


# ---- NUS workload calibration ----
# NUS Registrar: 1 unit = 2.5 h study/week; typical 20 units (5 x 4-unit courses) -> 50 h/week over 13 instructional weeks.
# Waking hours/week from Health@NUS mean sleep 6.84 h/night: 168 - 7*6.84 = 120.1 h.
# Demand index = study hours / waking hours. Weekly shape (midterm, submission, exam peaks) kept from the v1
# calendar profile, rescaled so the instructional-week mean equals 50 h (20 units).
WAKING_H = 168 - 7 * 6.84
INSTR_WEEKS = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14]


def demand_profile():
    v1 = _v1_profile()
    mean_instr = np.mean([v1[w] for w in INSTR_WEEKS])
    return {w: v1[w] / mean_instr * 50.0 / WAKING_H for w in v1}


def study_hours(units=20):
    d = demand_profile()
    return {w: d[w] * WAKING_H * units / 20 for w in d}


PHASE = {**{w: "Teaching" for w in range(1, 19)}, 7: "Recess", 8: "Midterms", 9: "Midterms",
         11: "Submissions", 12: "Submissions", 13: "Submissions", 14: "Submissions",
         15: "Reading", 16: "Finals", 17: "Finals", 18: "Post-exam"}

# ---------------- nominal parameters ----------------
P0 = dict(
    # delays (weeks)
    tau_SQ=3.0,      # Rumination -> Spleen Qi and Spleen-strengthening -> Spleen Qi (||)
    tau_HS=2.0,      # Shen-calming effect -> Calm Shen (||)
    tau_SL=0.7,      # Calm Shen -> Sleep Quality (|| sleep recovery)
    tau_H=3.0,       # Self-Care Engagement -> Congee Routine (|| habit formation)
    tau_PAS=0.4, tau_RU=0.3, tau_QR=0.3, tau_DEP=6.0, tau_BA=1.0, tau_SC=2.0, tau_MI=1.0, tau_SE=0.7,
    # link strengths
    s_RU_SQ=0.55,    # Rumination -(||)-> Spleen Qi  (思虑伤脾)
    s_SSE_SQ=0.40,   # Spleen-strengthening effect +(||)-> Spleen Qi
    s_RU_CS=0.50,    # Rumination -> Calm Shen (-)
    s_SHE_CS=0.35,   # Shen-calming effect -> Calm Shen (+)
    s_SL_RU=0.30,    # Sleep -> Rumination (-)
    s_MI_RU=0.30,    # Mindfulness -> Rumination (-)
    s_PAS_RU=0.70,   # Stress -> Rumination (+)
    s_AD_PAS=0.70,   # Demands -> Stress (+)
    s_CC_PAS=0.35,   # Coping -> Stress (-)
    s_SC_PAS=0.30,   # Sense of control -> Stress (-)
    s_TC_PAS=0.12,   # Congee time cost -> less study time -> Stress (B2)
    s_PE_SE=0.40, s_FT_SE=0.35, s_PAS_SE=0.45, s_DEP_SE=0.35,
    s_QR_FT=0.20,    # Quick relief masks felt fatigue (-)
    s_QR_SL=0.20,    # caffeine / late screens -> Sleep (-)  (Fixes that Fail)
    potency=1.0,     # ingredient evidence multiplier (sampled 0-1 in MC: weak/preclinical evidence)
    b0=0.08,         # stress intercept (calibrated to NPHS 2024 / NYMHS prevalence)
    resil=0.0,       # between-student resilience offset (calibrated spread)
    k_int=1.0,
    load=1.0,        # course load / 20 units (NUS OSA 2024: 56% recommended, 34% overload, 10% underload)       # scale on behavioural links (BA, mindfulness) - bounded by meta-analytic effect sizes
    LF=0.8,          # low-friction recipe (exogenous)
)

SCENARIOS = {
    "S0 No congee (quick relief only)": dict(congee=False, rules=False, potency=1.0),
    "S1 Congee routine": dict(congee=True, rules=False, potency=1.0),
    "S2 Congee + decision rules": dict(congee=True, rules=True, potency=1.0),
    "S3 Congee, double ingredient dose": dict(congee=True, rules=False, potency=2.0),
}

clip = lambda x: np.minimum(np.maximum(x, 0.0), 1.0)


def run(p, congee, rules, potency, init=None, demand=None, weeks=WEEKS):
    """Euler integration. Vectorised over Monte-Carlo samples (each p[k] may be an array)."""
    n = int(round(weeks / DT))
    shape = np.shape(p["tau_SQ"])
    s = init.copy() if init is not None else dict(
        SQ=np.full(shape, 0.60), HS=np.zeros(shape), SL=np.full(shape, 0.60), H=np.zeros(shape),
        PAS=np.full(shape, 0.35), RU=np.full(shape, 0.30), QR=np.full(shape, 0.25),
        DEP=np.full(shape, 0.25), BA=np.full(shape, 0.25), SC=np.full(shape, 0.40),
        MI=np.full(shape, 0.20), SE=np.full(shape, 0.50))
    dem = demand or demand_profile()
    LF = p["LF"] if congee else 0.0
    d = potency                                     # dose relative to recipe (1 = 10 g lotus, 7.5 g date, 100 g fresh yam per portion)
    pot = p["potency"] * 2 * d / (1 + d)            # Emax dose-response: recipe sits mid-pharmacopoeia range, doubling gives +33% not +100%
    kint = p["k_int"]
    out = {k: [] for k in ["t", "AD", "PAS", "RU", "MI", "CR", "BA", "SC", "SE", "SQ", "CS", "SL",
                           "PE", "FT", "FT_true", "QR", "DEP", "AT"]}
    for i in range(n):
        t = i * DT
        wk = min(int(t) + 1, weeks)
        AD = (dem.get(wk, 0.25) if isinstance(dem, dict) else dem) * p["load"]

        # ---- auxiliaries ----
        # Congee Routine: intention (SE, via low friction) + habit stock H  (SE -> CR delayed through H)
        CR = LF * (0.35 * s["SE"] + 0.65 * s["H"])
        if rules and congee:
            CR = np.maximum(CR, 0.45 * LF)                              # pre-committed weekly batch slots
            CR = CR + 0.5 * LF * np.maximum(s["RU"] - 0.45, 0)          # simmer-as-pause cue (RU -> CR, +)
        CR = clip(CR)
        SSE = pot * CR                                                  # CR -> spleen-strengthening (+)
        SHE = pot * CR                                                  # CR -> shen-calming (+)
        AT = 1 - 0.6 * CR                                               # CR -> Available Study Time (-)
        CS = clip(0.62 + s["HS"] - p["s_RU_CS"] * (s["RU"] - 0.3))     # RU -> CS (-), HS stock carries SHE (||)
        PE = clip(0.1 + 0.9 * s["SQ"])                                  # SQ -> PE (+)
        FT_true = clip(1 - (0.55 * PE + 0.45 * s["SL"]))                # PE -> FT (-), SL -> FT (-)
        FT = clip(FT_true - p["s_QR_FT"] * s["QR"])                     # quick relief masks felt fatigue
        CC = 1 - FT                                                     # FT -> Coping (-)

        # ---- indicated (target) values for stocks ----
        PAS_t = clip(p["b0"] - p["resil"] + p["s_AD_PAS"] * AD + p["s_CC_PAS"] * (0.55 - CC)
                     + p["s_SC_PAS"] * (0.45 - s["SC"]) + p["s_TC_PAS"] * (1 - AT) / 0.6)
        RU_t = clip(0.05 + p["s_PAS_RU"] * s["PAS"]
                    + p["s_SL_RU"] * (0.6 - s["SL"]) - p["s_MI_RU"] * (s["MI"] - 0.2))
        MI_t = clip(0.2 + 0.6 * kint * CR)                                     # CR -> MI (+)
        SQ_t = clip(0.62 - p["s_RU_SQ"] * (s["RU"] - 0.3) + p["s_SSE_SQ"] * SSE * 0.6)
        HS_t = p["s_SHE_CS"] * SHE * 0.6
        SL_t = clip(0.15 + 0.75 * CS - p["s_QR_SL"] * (s["QR"] - 0.2))  # CS -> SL (+ ||), QR -> SL (-)
        BA_t = clip(0.25 + 0.6 * kint * CR)                                    # CR -> BA (+)
        SC_t = clip(0.2 + 0.75 * s["BA"])                               # BA -> SC (+)
        trig = 0.30 * FT if (rules and congee) else 0.0                 # designed trigger FT -> SE (+)
        SE_t = clip(0.55 + p["s_PE_SE"] * (PE - 0.6) - p["s_FT_SE"] * (FT - 0.35) * (1 - 0.5 * LF)
                    - p["s_PAS_SE"] * (s["PAS"] - 0.35) - p["s_DEP_SE"] * (s["DEP"] - 0.25) + trig)
        QR_t = clip(0.05 + 0.65 * FT + 0.30 * s["DEP"] + 0.15 * s["PAS"])  # FT -> QR (+), DEP sustains use
        if rules and congee:
            QR_t = np.minimum(QR_t, 0.35)                               # capped quick relief

        # ---- integrate ----
        for k, tgt, tau in [("PAS", PAS_t, "tau_PAS"), ("RU", RU_t, "tau_RU"), ("MI", MI_t, "tau_MI"),
                            ("SQ", SQ_t, "tau_SQ"), ("HS", HS_t, "tau_HS"), ("SL", SL_t, "tau_SL"),
                            ("BA", BA_t, "tau_BA"), ("SC", SC_t, "tau_SC"), ("SE", SE_t, "tau_SE"),
                            ("QR", QR_t, "tau_QR"), ("DEP", s["QR"], "tau_DEP"), ("H", CR, "tau_H")]:
            s[k] = s[k] + DT * (tgt - s[k]) / p[tau]

        for k, v in dict(t=t, AD=AD, PAS=s["PAS"], RU=s["RU"], MI=s["MI"], CR=CR, BA=s["BA"], SC=s["SC"],
                         SE=s["SE"], SQ=s["SQ"], CS=CS, SL=s["SL"], PE=PE, FT=FT, FT_true=FT_true,
                         QR=s["QR"], DEP=s["DEP"], AT=AT).items():
            out[k].append(np.array(v, dtype=float) * np.ones(shape))
    return {k: np.array(v) for k, v in out.items()}, s


def indices(o):
    """Composite wellbeing indices (0-100). Physical uses TRUE fatigue, not caffeine-masked fatigue."""
    phys = 100 * (o["PE"] + o["SL"] + o["SQ"] + (1 - o["FT_true"])) / 4
    ment = 100 * ((1 - o["PAS"]) + (1 - o["RU"]) + o["SC"] + o["CS"]) / 4
    return phys, ment


def weekly(x):
    """Average daily values within each week -> shape (18, ...)."""
    return x.reshape(WEEKS, 7, *x.shape[1:]).mean(axis=1)


def sample_params(n, rng, spread=0.3):
    """Monte-Carlo: every strength and delay drawn uniformly within +/- spread of nominal."""
    p = {}
    for k, v in P0.items():
        if k in ("potency", "LF"):
            p[k] = np.full(n, v) if k == "potency" else rng.uniform(0.65, 0.95, n)
        else:
            p[k] = v * rng.uniform(1 - spread, 1 + spread, n)
    return p


def burn_in(p, n_weeks=8):
    """Pre-semester holiday at low demand so every run starts from its own consistent state."""
    _, s = run(p, congee=False, rules=False, potency=1.0, demand=0.15, weeks=n_weeks)
    return s


def sample_params_v2(n, rng, b0=0.08, sd_resil=0.0, k_int=1.0):
    """Source-informed distributions (see parameter_sources.csv).
    Link strengths without a direct quantitative source keep +/-30% uniform uncertainty."""
    p = sample_params(n, rng, spread=0.3)
    # delays
    p["tau_H"] = rng.lognormal(np.log(3.0), 0.55, n)          # Singh et al. 2024: median 59-66 d to 95% automaticity -> tau ~3 wk; wide spread
    p["tau_SL"] = rng.uniform(0.4, 1.2, n)                     # Lo et al. 2016 (Duke-NUS): 2 recovery nights insufficient
    p["tau_SQ"] = rng.uniform(2.0, 6.0, n)                     # food-therapy / jujube trials run 4-12 wk; slow tonification
    p["tau_HS"] = rng.uniform(1.0, 4.0, n)
    # ingredient evidence: preclinical (yam) / small mixed trials (jujube, lotus) -> anywhere from null to prior effect
    p["potency"] = rng.uniform(0.0, 1.0, n)
    # caffeine -> sleep: Drake et al. 2013, 400 mg even 6 h pre-bed cut >1 h of ~7 h sleep
    p["s_QR_SL"] = rng.uniform(0.2, 0.4, n)
    # calibrated
    p["b0"] = np.full(n, b0)
    p["resil"] = rng.normal(0.0, sd_resil, n)
    p["k_int"] = np.full(n, k_int)
    p["load"] = rng.choice([18 / 20, 20 / 20, 23 / 20], size=n, p=[0.10, 0.56, 0.34])   # NUS OSA 2024 workload split
    return p

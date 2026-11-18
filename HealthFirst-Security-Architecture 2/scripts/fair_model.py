"""FAIR-style Monte Carlo model for HealthFirst's six largest loss scenarios (inherent vs residual).

Document 1, Section 7.5. Run from the project folder:  python3 scripts/fair_model.py
Requires numpy and matplotlib. Writes charts/fair-results.json and the two FAIR charts (SVG + PNG).
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

_inter = False
for w in ["Regular", "Medium", "SemiBold", "Bold"]:   # use the Inter font when it is installed, else the default
    try:
        font_manager.fontManager.addfont(f"/usr/share/fonts/opentype/inter/Inter-{w}.otf")
        _inter = True
    except (FileNotFoundError, OSError, RuntimeError):
        pass
if _inter:
    plt.rcParams["font.family"] = "Inter"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": "#A0AEC0",
                     "axes.labelcolor": "#2D3748", "xtick.color": "#4A5568", "ytick.color": "#4A5568",
                     "axes.spines.top": False, "axes.spines.right": False})

RNG = np.random.default_rng(20261117)
N = 100_000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "charts")

# id, name, risks, LEF_inh, LM_inh ($M), LEF_res, LM_res ($M)
SCEN = [
    ("S1", "Enterprise ransomware with clinical downtime & extortion", "R01, R09, R14",
     (0.08, 0.25, 0.60), (20, 65, 250), (0.02, 0.06, 0.15), (6, 18, 80)),
    ("S2", "Large-scale PHI exfiltration (external / cloud)", "R02, R07, R10",
     (0.20, 0.50, 1.20), (3, 10, 60), (0.05, 0.15, 0.40), (2, 6, 30)),
    ("S3", "IoMT compromise affecting clinical operations", "R03",
     (0.05, 0.15, 0.40), (1, 6, 40), (0.01, 0.04, 0.12), (0.5, 3, 20)),
    ("S4", "Patient / clinician account takeover on telemedicine", "R04, R11",
     (1.0, 3.0, 8.0), (0.1, 0.5, 3), (0.3, 1.0, 3.0), (0.05, 0.2, 1)),
    ("S5", "Business-associate / third-party compromise", "R06",
     (0.10, 0.30, 0.70), (2, 15, 90), (0.08, 0.25, 0.60), (1, 6, 40)),
    ("S6", "Insider privacy violations (inappropriate access)", "R05",
     (2.0, 6.0, 15.0), (0.02, 0.15, 2), (1.0, 3.0, 8.0), (0.01, 0.08, 1)),
]
PROGRAM_COST = 13.8  # $M per year, 3-year average (licences, people, services) - planning assumption
RETENTION, LIMIT = 5.0, 50.0  # cyber insurance: $5M per-event retention, $50M per-event limit (assumption)
PREMIUM = 3.2              # $M per year (assumption)


def pert(mn, ml, mx, size, lam=4.0):
    a = 1 + lam * (ml - mn) / (mx - mn)
    b = 1 + lam * (mx - ml) / (mx - mn)
    return mn + RNG.beta(a, b, size) * (mx - mn)


def simulate(lef, lm, with_net=False):
    rate = pert(*lef, N)
    n = RNG.poisson(rate)
    tot, net = np.zeros(N), np.zeros(N)
    idx = np.repeat(np.arange(N), n)
    if idx.size:
        losses = pert(*lm, idx.size)
        np.add.at(tot, idx, losses)
        retained = np.minimum(losses, RETENTION) + np.maximum(0, losses - RETENTION - LIMIT)
        np.add.at(net, idx, retained)
    return (tot, net) if with_net else tot


res = {"iterations": N, "program_cost_musd": PROGRAM_COST, "scenarios": []}
tot_inh, tot_res, tot_net = np.zeros(N), np.zeros(N), np.zeros(N)
for sid, name, risks, li, mi, lr, mr in SCEN:
    a = simulate(li, mi)
    b, bn = simulate(lr, mr, with_net=True)
    tot_inh += a
    tot_res += b
    tot_net += bn
    res["scenarios"].append({"id": sid, "name": name, "risks": risks,
                             "lef_inh": li, "lm_inh": mi, "lef_res": lr, "lm_res": mr,
                             "ale_inh": round(float(a.mean()), 2), "ale_res": round(float(b.mean()), 2),
                             "p90_inh": round(float(np.percentile(a, 90)), 2),
                             "p90_res": round(float(np.percentile(b, 90)), 2)})


def stats(x):
    return {"mean": round(float(x.mean()), 2), "p50": round(float(np.percentile(x, 50)), 2),
            "p90": round(float(np.percentile(x, 90)), 2), "p95": round(float(np.percentile(x, 95)), 2),
            "p99": round(float(np.percentile(x, 99)), 2),
            "prob_gt_20": round(float((x > 20).mean()), 3), "prob_gt_50": round(float((x > 50).mean()), 3),
            "prob_gt_100": round(float((x > 100).mean()), 3)}


res["total_inh"], res["total_res"], res["total_res_net_insurance"] = stats(tot_inh), stats(tot_res), stats(tot_net)
res["insurance"] = {"retention": RETENTION, "limit": LIMIT, "premium": PREMIUM}
red = res["total_inh"]["mean"] - res["total_res"]["mean"]
res["ale_reduction"] = round(red, 2)
res["rosi"] = round((red - PROGRAM_COST) / PROGRAM_COST, 2)
json.dump(res, open(OUT + "/fair-results.json", "w"), indent=2)
print(json.dumps({k: v for k, v in res.items() if k != "scenarios"}, indent=2))
for s in res["scenarios"]:
    print(s["id"], s["ale_inh"], s["ale_res"], s["p90_inh"], s["p90_res"])

# ---------------------------------------------------------------- chart 1: loss exceedance curve
fig, ax = plt.subplots(figsize=(8.6, 4.4), dpi=100)
xs = np.logspace(-1, np.log10(600), 400)
for data, col, lab, ls in [(tot_inh, "#C53030", "Inherent (current state)", "-"),
                          (tot_res, "#2B6CB0", "Residual (target architecture)", "-"),
                          (tot_net, "#1E8C7E", "Residual, net of cyber insurance", "--")]:
    ys = [(data > x).mean() * 100 for x in xs]
    ax.plot(xs, ys, color=col, lw=2.4, label=lab, ls=ls)
ax.scatter([20], [10], s=90, color="#6B46C1", zorder=5, marker="D")
ax.annotate("Board risk tolerance:\n≤ 10 % chance of losing > $20M in a year", xy=(20, 10), xytext=(0.13, 9),
            fontsize=9.5, color="#4C2F94", arrowprops=dict(arrowstyle="-|>", color="#6B46C1", lw=1.2))
ax.set_xscale("log")
ax.set_xticks([0.1, 1, 5, 10, 20, 50, 100, 250, 500])
ax.set_xticklabels(["$0.1M", "$1M", "$5M", "$10M", "$20M", "$50M", "$100M", "$250M", "$500M"])
ax.set_ylim(0, 100)
ax.set_ylabel("Probability annual loss exceeds X (%)")
ax.set_xlabel("Annual loss X (USD, log scale)")
ax.grid(True, which="major", color="#E2E8F0", lw=0.8)
ax.legend(frameon=False, loc="upper right")
ax.set_title("Loss exceedance curve — top six loss scenarios combined (100,000 simulated years)",
             fontsize=11, color="#1A202C", loc="left", fontweight="semibold")
fig.tight_layout()
fig.savefig(OUT + "/fair-loss-exceedance.svg")
fig.savefig(OUT + "/fair-loss-exceedance.png", dpi=220)
plt.close(fig)

# ---------------------------------------------------------------- chart 2: ALE by scenario
fig, ax = plt.subplots(figsize=(8.6, 3.9), dpi=100)
labels = [f'{s["id"]} · {s["name"]}' for s in res["scenarios"]][::-1]
inh = [s["ale_inh"] for s in res["scenarios"]][::-1]
rsd = [s["ale_res"] for s in res["scenarios"]][::-1]
y = np.arange(len(labels))
ax.barh(y + 0.19, inh, height=0.36, color="#C53030", label="Inherent ALE")
ax.barh(y - 0.19, rsd, height=0.36, color="#2B6CB0", label="Residual ALE")
for yi, v in zip(y, inh):
    ax.text(v + 0.3, yi + 0.19, f"${v:.1f}M", va="center", fontsize=8.5, color="#2D3748")
for yi, v in zip(y, rsd):
    ax.text(v + 0.3, yi - 0.19, f"${v:.1f}M", va="center", fontsize=8.5, color="#2D3748")
ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=9)
ax.set_xlabel("Annualized loss expectancy (USD millions, mean of simulation)")
ax.grid(True, axis="x", color="#E2E8F0", lw=0.8)
ax.legend(frameon=False, loc="lower right")
ax.set_title("Annualized loss expectancy by scenario — inherent vs residual", fontsize=11, color="#1A202C",
             loc="left", fontweight="semibold")
fig.tight_layout()
fig.savefig(OUT + "/fair-ale-by-scenario.svg")
fig.savefig(OUT + "/fair-ale-by-scenario.png", dpi=220)
plt.close(fig)
print("charts saved")

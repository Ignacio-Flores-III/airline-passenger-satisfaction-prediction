import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap

if not hasattr(np, "long"):
    np.long = int

pipeline = joblib.load("artifacts/model.joblib")
df = pd.read_csv("data/test.csv").dropna().sample(n=500, random_state=42)
X = df.drop(columns=[c for c in ["Unnamed: 0", "id", "satisfaction"] if c in df.columns])

preprocessor = pipeline.named_steps[list(pipeline.named_steps.keys())[0]]
clf = pipeline.named_steps[list(pipeline.named_steps.keys())[-1]]

X_trans = preprocessor.transform(X)
if hasattr(X_trans, "toarray"):
    X_trans = X_trans.toarray()

try:
    feat_names = [f.split("__")[-1] for f in preprocessor.get_feature_names_out()]
except Exception:
    feat_names = [f"Feature_{i}" for i in range(X_trans.shape[1])]

explainer = shap.TreeExplainer(clf)
shap_vals = explainer.shap_values(X_trans)
if isinstance(shap_vals, list):
    sv = shap_vals[0]
elif shap_vals.ndim == 3:
    sv = shap_vals[:, :, 0]
else:
    sv = shap_vals

plt.figure(figsize=(10, 6))
shap.summary_plot(sv, X_trans, feature_names=feat_names, max_display=10, show=False)
plt.title("SHAP Feature Impact on Passenger Defection Risk (Top 10 Drivers)", fontsize=12, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig("assets/shap_summary.png", dpi=300, bbox_inches="tight")
plt.close()

rng = np.random.default_rng(42)
n_trials = 1000
at_risk_cohort = 10778
fares = rng.normal(450, 55, n_trials)
trips = rng.uniform(3.2, 4.8, n_trials)
save_rates = rng.beta(11, 9, n_trials)
capex = rng.uniform(6.0, 8.0, n_trials)
voucher_cost = 25

net_value_m = ((at_risk_cohort * save_rates * fares * trips) - (at_risk_cohort * voucher_cost)) / 1e6 - capex
ci_low, ci_med, ci_high = np.percentile(net_value_m, [2.5, 50, 97.5])

plt.figure(figsize=(10, 5))
plt.hist(net_value_m, bins=35, color="#1f4e78", edgecolor="white", alpha=0.9)
plt.axvline(ci_low, color="#c00000", linestyle="--", linewidth=2, label=f"2.5th Pct: ${ci_low:.2f}M")
plt.axvline(ci_med, color="#2e75b6", linestyle="-", linewidth=2.5, label=f"Median Net ROI: ${ci_med:.2f}M")
plt.axvline(ci_high, color="#385723", linestyle="--", linewidth=2, label=f"97.5th Pct: ${ci_high:.2f}M")
plt.title("Monte Carlo Sensitivity Analysis (1,000 Trials): Year-1 Net Value After $6M–$8M Digital Capex", fontsize=11, fontweight="bold")
plt.xlabel("Net Value Created ($ Millions)", fontsize=10)
plt.ylabel("Simulation Frequency", fontsize=10)
plt.legend()
plt.tight_layout()
plt.savefig("assets/monte_carlo_roi.png", dpi=300)
plt.close()

print(f"Saved SHAP and Monte Carlo assets. 95% CI Net Value: [${ci_low:.2f}M, ${ci_high:.2f}M]")
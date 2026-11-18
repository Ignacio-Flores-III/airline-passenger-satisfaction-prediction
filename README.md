# Predictive Customer Churn & Capital Allocation in Commercial Aviation

**Author:** Ignacio Flores III

## Project Overview
Combining structured survey records ($N = 124,685$) with unprompted airline reviews, this pipeline proves digital friction (**Online Boarding & Inflight Wi-Fi**) drives >32% of retention power vs. <5% for physical **Seat Comfort**.

* **Artifact (`artifacts/model.joblib`):** Unified `ColumnTransformer` + Random Forest (**96.34%** Acc | **0.9576** F1 | **0.9939** ROC-AUC)

## Repository Structure
```text
airline-passenger-satisfaction-prediction/
├── artifacts/
│   └── model.joblib                                  # Unified ColumnTransformer + Random Forest pipeline
├── assets/                                           # Diagnostic charts, feature importance, and ROI visuals
├── notebooks/
│   └── airline_satisfaction_walkthrough.ipynb        # Interactive model artifact & diagnostic visual walkthrough
├── reports/
│   ├── Airline_Satisfaction_Technical_Report.pdf     # Executive technical report and econometric benchmark
│   ├── Stakeholder_Presentation.pdf                  # Stakeholder slide deck (PDF)
│   └── Stakeholder_Presentation.pptx                 # Editable stakeholder presentation (PPTX)
├── src/                                              # Modular training, NLP pipeline, and report generation scripts
├── .gitignore                                        # Excludes local data/, .venv/, and cache files
├── README.md                                         # Project documentation and reproduction guide
└── requirements.txt                                  # Python package dependencies
```

## Independent Peer Reproduction

1. Clone the repository:
   ```bash
   git clone https://github.com/Ignacio-Flores-III/airline-passenger-satisfaction-prediction.git && cd airline-passenger-satisfaction-prediction
   ```
2. Set up the virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
   ```
3. Run standalone inference check:
   ```bash
   python src/test_artifact.py
   ```
4. Optional full rebuild:
   ```bash
   python src/build_pipeline.py && python src/generate_pipeline_diagram.py && python src/generate_p2_report.py && python src/generate_p2_deck.py
   ```
5. Explore the walkthrough notebook & executive deliverables:
   * Open `notebooks/airline_satisfaction_walkthrough.ipynb` to inspect `artifacts/model.joblib` and inline diagnostic plots.
   * Review `reports/Airline_Satisfaction_Technical_Report.pdf` and `reports/Stakeholder_Presentation.pdf` for full findings and capital allocation recommendations.
---

## Live Interactive Capex & Churn Simulator

* **Live Production App:** [Launch Airline Churn & Capex Simulator](https://airline-passenger-satisfaction-prediction-his2mrr2ykcvmsfsyucn.streamlit.app/)
* **Capabilities:**
  * **Tab 1 — Passenger Friction Simulator:** Real-time inference against `artifacts/model.joblib` showing how upgrading digital touchpoints (`Online boarding`, `Inflight wifi service`) shifts individual defection probability.
  * **Tab 2 — Capex & Recovery ROI Optimizer:** Interactive sensitivity sliders and 1,000-trial Monte Carlo simulation modeling Year-1 net value after a $6M–$8M digital infrastructure investment.

## Explainable AI (SHAP) & Monte Carlo Risk Analysis

* **SHAP Feature Attribution (`assets/shap_summary.png`):** TreeExplainer confirms `Online boarding` and `Inflight wifi service` exert the strongest marginal downward pull on passenger defection probability, outperforming physical cabin upgrades on a per-dollar basis.
* **Monte Carlo Sensitivity (`assets/monte_carlo_roi.png`):** Across 1,000 stochastic trials varying airfare, repeat trip frequency, recovery save rate, and $6M–$8M upfront digital Capex, Year-1 net value spans a 95% confidence interval of **[$-1.75M, $9.30M]** (before recurring Year-2+ cash flows).
* **MLOps Verification:** Automated `pytest` inference suite (`tests/test_pipeline.py`) and Population Stability Index drift monitoring (`src/monitor_drift.py`, confirming `Online boarding` PSI = `0.0005` and `Inflight wifi service` PSI = `0.0002`).

![SHAP Feature Impact](assets/shap_summary.png)
![Monte Carlo ROI Distribution](assets/monte_carlo_roi.png)

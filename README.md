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
   git clone [https://github.com/Ignacio-Flores-III/airline-passenger-satisfaction-prediction.git](https://github.com/Ignacio-Flores-III/airline-passenger-satisfaction-prediction.git) && cd airline-passenger-satisfaction-prediction
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
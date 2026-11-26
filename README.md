# Predictive Customer Satisfaction & Capital Allocation in Commercial Aviation

**Author:** Ignacio Flores III

## Project Overview
Combining structured passenger survey records ($N = 124,685$) with unprompted airline reviews, this pipeline demonstrates that digital touchpoint friction (**Online Boarding & Inflight Wi-Fi**) accounts for **>32%** of predictive feature importance for stated satisfaction—outperforming physical **Seat Comfort (<5%)**. Because the underlying dataset consists of cross-sectional satisfaction surveys rather than longitudinal booking records, all retention and financial figures below explicitly separate **directly observed model performance** from **modeled economic scenario assumptions**.

- **Artifact (`artifacts/model.joblib`):** Unified `ColumnTransformer` + Random Forest (**96.34%** Acc | **0.9576** F1 | **0.9939** ROC-AUC)

## Repository Structure
```text
airline-passenger-satisfaction-prediction/
├── artifacts/
│   └── model.joblib                                  # Unified ColumnTransformer + Random Forest pipeline
├── assets/                                           # Diagnostic charts, feature importance, and ROI visuals
├── checkpoints/
│   ├── p1/                                           # Archived P1 rendered PDF & infographic checkpoint
│   └── p2/                                           # Archived P2 signed peer validation form
├── notebooks/
│   └── airline_satisfaction_walkthrough.ipynb        # Interactive model artifact & diagnostic visual walkthrough
├── reports/
│   ├── Airline_Satisfaction_Report.html              # Self-contained rendered HTML notebook report
│   ├── Airline_Satisfaction_Technical_Report.pdf     # Executive technical report and econometric benchmark
│   ├── Stakeholder_Presentation.pdf                  # Stakeholder slide deck (PDF)
│   └── Stakeholder_Presentation.pptx                 # Editable stakeholder presentation (PPTX)
├── src/                                              # Modular training, NLP pipeline, and report generation scripts
├── tests/                                            # Automated pytest inference & artifact validation suite
├── .gitignore                                        # Excludes local data/, .venv/, and cache files
├── README.md                                         # Project documentation and reproduction guide
└── requirements.txt                                  # Python package dependencies
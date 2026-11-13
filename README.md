# Predictive Customer Churn & Capital Allocation in Commercial Aviation
**Author:** Ignacio Flores III | **Course:** MSBA 265 – Applied Analytics

## Project Overview
Combining structured survey records (N = 124,685) with unprompted airline reviews, this pipeline proves digital friction (**Online Boarding** & **Inflight Wi-Fi**) drives >32% of retention power vs. <5% for physical **Seat Comfort**.
* **Artifact (`artifacts/model.joblib`):** Unified `ColumnTransformer` + Random Forest (`96.34%` Acc | `0.9576` F1 | `0.9939` ROC-AUC)

## Independent Peer Reproduction
1. `git clone https://github.com/Ignacio-Flores-III/airline-passenger-satisfaction-prediction.git && cd airline-passenger-satisfaction-prediction`
2. `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
3. Run standalone inference check: `python src/test_artifact.py`
4. Optional full rebuild: `python src/build_pipeline.py && python src/generate_pipeline_diagram.py && python src/generate_p2_report.py && python src/generate_p2_deck.py`

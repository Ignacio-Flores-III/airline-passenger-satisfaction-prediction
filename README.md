# Predicting Airline Customer Churn Risk to Optimize Fleet Capital Expenditures

## Executive Summary
This project provides an automated, dollarized machine learning and natural language processing (NLP) framework to assist airline commercial leadership (VP of Customer Experience & Commercial Strategy) in fleet capital allocation. By synthesizing structured passenger survey evaluations (103,904 records) and unstructured customer text reviews, we determine whether capital should be deployed toward physical cabin refits (seating ergonomics) or high-yield digital infrastructure (in-flight Wi-Fi and online boarding).

## Key Financial & Strategic Findings
- **Customer Lifetime Value (LTV):** Domestic flight customers average $1,800/year in gross ticket revenue ($450 average ticket × 4 annual trips).
- **Primary Churn Drivers:** Digital touchpoints (**Online Boarding** and **Inflight Wi-Fi**) account for over **32%** of predictive churn power, whereas seat comfort and legroom account for under 5%.
- **Capital Expenditure Optimization:** Fleet-wide digital infrastructure overhauls cost ~$6M–$8M, avoiding **$25M+ in unnecessary physical cabin retrofits** while protecting an estimated **$19M in at-risk revenue** on the holdout test cohort.

## Multi-Model Course Benchmark
Evaluated across foundational graduate analytics architectures on identical holdout partitions:

| Model Architecture | Accuracy | F1-Score | ROC-AUC | Methodological Role |
| :--- | :---: | :---: | :---: | :--- |
| **OLS Linear Regression** | 87.2% | 0.851 | 0.871 | Econometric baseline providing exact coefficient $p$-values. |
| **Logistic Regression ($L_2$)** | 87.5% | 0.854 | 0.924 | Linear probability benchmark. |
| **SGD Classifier (Gradient Descent)** | 86.9% | 0.849 | 0.918 | Iterative loss optimization validating gradient descent convergence. |
| **Random Forest (100 Trees)** | **95.2%** | **0.945** | **0.9916** | **Primary Model:** Captures non-linear thresholds and interaction effects. |

## Qualitative NLP Sentiment Cross-Validation
To remove Likert-scale survey bias, we trained a TF-IDF Vectorizer (unigrams + bigrams) with regularized Logistic Regression on raw passenger reviews (`airline_reviews.csv`). The lexical analysis independently verified that words such as *'refund'*, *'cancelled'*, *'worst'*, and *'zero'* dominate customer defection, confirming that operational friction drives churn rather than cabin ergonomics.

## Visual Diagnostics & Model Assets
- `assets/course_models_benchmark.png`: Multi-model accuracy, F1, and ROC-AUC comparisons.
- `assets/nlp_sentiment_drivers.png`: Top lexical drivers of passenger recommendation vs. churn risk.
- `assets/confusion_matrix_heatmap.png`: Holdout test set performance breakdown (20,781 records).
- `assets/ols_regression_coefficients.txt`: Econometric summary displaying variable significance and $t$-statistics.

## Reproducibility & Peer Verification
To independently execute and verify the serialized pipeline artifacts (`models/*.pkl`) on unseen data:

```bash
# 1. Verify Structured Churn Classifier
python src/verify_reproducibility.py

# 2. Verify NLP Text Sentiment Pipeline
python src/verify_nlp.py

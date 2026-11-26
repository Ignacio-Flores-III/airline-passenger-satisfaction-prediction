import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

os.makedirs("reports", exist_ok=True)
pdf_filename = "reports/Airline_Satisfaction_Technical_Report.pdf"
doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    leftMargin=42,
    rightMargin=42,
    topMargin=42,
    bottomMargin=42
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle("TitleCustom", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=colors.HexColor("#1a365d"))
sub_style = ParagraphStyle("SubCustom", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=colors.HexColor("#2b6cb0"), spaceAfter=4)
h1_style = ParagraphStyle("H1Custom", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=colors.HexColor("#0f2942"), spaceBefore=10, spaceAfter=4)
body_style = ParagraphStyle("BodyCustom", parent=styles["Normal"], fontName="Helvetica", fontSize=9.2, leading=13, textColor=colors.HexColor("#2d3748"), spaceAfter=5)
bullet_style = ParagraphStyle("BulletCustom", parent=body_style, leftIndent=14, firstLineIndent=-9, spaceAfter=3)
code_style = ParagraphStyle("CodeCustom", parent=styles["Normal"], fontName="Courier", fontSize=8, leading=10.5, textColor=colors.HexColor("#1a202c"), backColor=colors.HexColor("#edf2f7"), leftIndent=10, rightIndent=10, spaceBefore=3, spaceAfter=6)
th_style = ParagraphStyle("TH", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8.3, leading=11, textColor=colors.white)
td_style = ParagraphStyle("TD", parent=styles["Normal"], fontName="Helvetica", fontSize=8.0, leading=10.5, textColor=colors.HexColor("#2d3748"))

story = []

# HEADER
story.append(Paragraph("MSBA 265: Applied Analytics | Final Project Delivery Technical Report", sub_style))
story.append(Paragraph("Predictive Customer Satisfaction & Capital Allocation in Commercial Aviation", title_style))
story.append(Paragraph("<b>Author:</b> Ignacio Flores III &nbsp;|&nbsp; <b>Repository:</b> github.com/Ignacio-Flores-III/airline-passenger-satisfaction-prediction", body_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1a365d"), spaceBefore=4, spaceAfter=10))

# 1. EXECUTIVE SUMMARY
story.append(Paragraph("1. Executive Summary", h1_style))
story.append(Paragraph(
    "Commercial airlines allocate tens of millions of dollars annually toward fleet upgrades, frequently debating between physical cabin overhauls (new seats and legroom) and digital infrastructure (high-speed satellite Wi-Fi and seamless mobile boarding). Analyzing 124,685 cross-sectional passenger survey records alongside unprompted customer reviews, this project builds a unified machine learning, explainable AI (SHAP), and natural language processing (NLP) framework to identify the strongest predictive correlates of stated passenger satisfaction.",
    body_style
))
story.append(Paragraph(
    "<b>Key Result & Recommendation:</b> The ensemble Random Forest pipeline achieves <b>96.34% holdout accuracy</b> and <b>0.9939 ROC-AUC</b>, outperforming linear econometric baselines by over 9 percentage points. Both SHAP feature attribution and NLP review modeling demonstrate that digital touchpoint friction—specifically <b>Online Boarding</b> (t = 73.68, p &lt; 0.001) and <b>Inflight Wi-Fi</b> (t = 55.34, p &lt; 0.001)—accounts for over 32% of predictive importance for stated satisfaction, whereas physical <b>Seat Comfort</b> contributes less than 5%. Executive leadership should validate these predictive signals via a <b>6-month randomized hub-route A/B pilot</b> ($6M–$8M digital upgrade scope vs. $25M–$50M physical seat retrofits) tracking loyalty ID repeat bookings before fleet-wide Capex commitment.",
    body_style
))

# 2. BUSINESS CONTEXT AND OBJECTIVE
story.append(Paragraph("2. Business Context and Objective", h1_style))
story.append(Paragraph("• <b>Primary Stakeholder:</b> Vice President of Customer Experience & Commercial Strategy, responsible for annual fleet retrofit capital expenditure (Capex) budgets and service-recovery interventions.", bullet_style))
story.append(Paragraph("• <b>Scenario Economic Framing:</b> Because the public survey dataset records stated satisfaction rather than longitudinal repeat bookings, financial exposure is modeled using external industry benchmarks: Bureau of Transportation Statistics (BTS, 2023) domestic round-trip airfare averages ($450) across 4 annual trips per repeat flyer ($1,800/year illustrative LTV). Across 11,403 dissatisfied holdout passengers, Monte Carlo simulations model Year-1 net value under user-calibrated satisfaction-to-retention conversion assumptions.", bullet_style))
story.append(Paragraph("• <b>Project Objective & Success Criteria:</b> Deliver a reproducible predictive pipeline exceeding 0.90 out-of-sample ROC-AUC with SHAP explanations, PSI drift governance, and an interactive Streamlit Capex scenario simulator.", bullet_style))

# 3. INDIVIDUAL PROJECT OWNERSHIP
story.append(Paragraph("3. Individual Project Ownership", h1_style))
story.append(Paragraph(
    "As a former Division I student-athlete and current M.S. in Data Analytics candidate with a B.A. in Business Marketing, I designed this project to bridge technical machine learning rigor with disciplined capital budgeting. All stages—problem framing, data ingestion, econometric OLS benchmarking, Random Forest pipeline serialization, TF-IDF text modeling, SHAP attribution, PSI drift monitoring, Streamlit deployment, and stakeholder slide synthesis—were executed independently by the author.",
    body_style
))

# 4. TOPIC AND INDUSTRY CONTEXT
story.append(Paragraph("4. Topic and Industry Context", h1_style))
story.append(Paragraph(
    "Customer experience analytics evolved from static post-flight Net Promoter Score (NPS) surveys in the 1980s to modern hybrid pipelines combining tree-based ensembles (Breiman, 2001) with TF-IDF text mining (Salton & Buckley, 1988). Industry leaders such as Delta Air Lines have committed over $1B toward high-speed Wi-Fi and mobile app integration (Delta News Hub, 2023), reflecting an industry shift toward frictionless digital journeys.",
    body_style
))

# 5. DATA AND PREPARATION
story.append(Paragraph("5. Data and Preparation", h1_style))
story.append(Paragraph("• <b>Structured Survey Data:</b> Kaggle <i>Airline Passenger Satisfaction</i> dataset (103,904 training rows; 20,781 holdout test rows; 23 attributes). <b>Unit of Analysis:</b> One completed passenger flight leg (cross-sectional stated satisfaction).", bullet_style))
story.append(Paragraph("• <b>Unstructured Review Data:</b> Kaggle <i>Airline Reviews</i> dataset (public, unprompted passenger text reviews and overall ratings) used to triangulate survey findings against spontaneous customer language.", bullet_style))
story.append(Paragraph("• <b>Cleaning & Pipeline Transformations:</b> Missing values in <i>Arrival Delay in Minutes</i> (310 records) are imputed using median/departure values inside a scikit-learn <code>ColumnTransformer</code>. Categorical variables (<i>Gender</i>, <i>Customer Type</i>, <i>Type of Travel</i>, <i>Class</i>) undergo <code>OneHotEncoder(handle_unknown='ignore')</code>, while numeric attributes are standardized via <code>StandardScaler</code>. Text reviews undergo lowercasing, regex punctuation removal, stopword filtering, and unigram/bigram TF-IDF vectorization.", bullet_style))
story.append(Paragraph("• <b>Privacy & Governance:</b> Both sources are publicly licensed under CC0 / Open Database with anonymized keys and zero Personally Identifiable Information (PII). Rendered P1 milestone artifacts are archived in <code>checkpoints/p1/MSBA265_P1_Ignacio_Flores.pdf</code>.", bullet_style))

story.append(PageBreak())

# 6. METHOD AND IMPLEMENTATION
story.append(Paragraph("6. Method and Implementation", h1_style))
story.append(Paragraph(
    "To ensure rigorous model selection, four architectures from MSBA 265 coursework were evaluated on identical train/test splits: (1) Ordinary Least Squares (OLS) for exact econometric p-values, (2) L2-regularized Logistic Regression, (3) Stochastic Gradient Descent (SGD) Classifier, and (4) an ensemble Random Forest Classifier (100 trees, random_state=42) bundled inside a unified preprocessing pipeline with SHAP TreeExplainer and Population Stability Index (PSI) drift monitoring.",
    body_style
))

pipe_img = "assets/data_to_action_pipeline.png"
if os.path.exists(pipe_img):
    story.append(Spacer(1, 4))
    story.append(Image(pipe_img, width=7.0*inch, height=3.2*inch))
    story.append(Paragraph("<i>Figure 1: End-to-End Data-to-Action & MLOps Pipeline covering preprocessing, Random Forest & NLP modeling, SHAP attribution, PSI drift governance, and interactive Streamlit scenario simulation.</i>", body_style))

# 7. EVALUATION, FINDINGS & OBSERVATIONAL BOUNDARIES
story.append(Paragraph("7. Evaluation, Findings & Observational Boundaries", h1_style))
story.append(Paragraph("Models were evaluated across Accuracy, F1-Score, and ROC-AUC on the 20,781-row holdout partition:", body_style))

bench_data = [
    [Paragraph("<b>Model Architecture</b>", th_style), Paragraph("<b>Accuracy</b>", th_style), Paragraph("<b>F1-Score</b>", th_style), Paragraph("<b>ROC-AUC</b>", th_style), Paragraph("<b>Diagnostic Interpretation</b>", th_style)],
    [Paragraph("OLS Linear Baseline", td_style), Paragraph("87.20%", td_style), Paragraph("0.8510", td_style), Paragraph("0.8710", td_style), Paragraph("Confirms statistical significance (R² = 0.552); plateaus on non-linear interactions.", td_style)],
    [Paragraph("Logistic Regression (L2)", td_style), Paragraph("87.50%", td_style), Paragraph("0.8540", td_style), Paragraph("0.9240", td_style), Paragraph("Strong parametric log-odds benchmark; misses conditional delay/Wi-Fi thresholds.", td_style)],
    [Paragraph("SGD Classifier (Log-Loss)", td_style), Paragraph("86.90%", td_style), Paragraph("0.8490", td_style), Paragraph("0.9180", td_style), Paragraph("Validates scalable gradient convergence across 103k records.", td_style)],
    [Paragraph("<b>Unified Random Forest</b>", td_style), Paragraph("<b>96.34%</b>", td_style), Paragraph("<b>0.9576</b>", td_style), Paragraph("<b>0.9939</b>", td_style), Paragraph("<b>Selected Model:</b> Captures non-linear interaction thresholds (+8.8% accuracy lift).", td_style)]
]
t_bench = Table(bench_data, colWidths=[1.55*inch, 0.72*inch, 0.72*inch, 0.75*inch, 3.26*inch])
t_bench.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a365d")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e0")),
    ("TOPPADDING", (0,0), (-1,-1), 3.5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3.5),
]))
story.append(t_bench)
story.append(Spacer(1, 5))

story.append(Paragraph(
    "<b>Econometric, SHAP & NLP Triangulation:</b> OLS regression confirms <b>Online Boarding</b> (coef = 0.0795, t = 73.68, p &lt; 0.001) and <b>Inflight Wi-Fi</b> (coef = 0.0673, t = 55.34, p &lt; 0.001) exhibit roughly 9x the marginal association with stated satisfaction compared to <b>Seat Comfort</b> (coef = 0.0080, t = 6.65), while <b>Flight Distance</b> is statistically insignificant (p = 0.339). SHAP TreeExplainer confirms these two digital touchpoints exert the strongest downward pull on predicted dissatisfaction risk, while TF-IDF + Logistic Regression extracts operational breakdown terms (<i>refund</i>, <i>cancelled</i>, <i>worst</i>) as top negative review predictors.",
    body_style
))

story.append(Paragraph("<b>Distinction Between Directly Observed Data and Modeled Economic Assumptions:</b>", body_style))
ev_data = [
    [Paragraph("<b>Analytical Dimension</b>", th_style), Paragraph("<b>Directly Observed in Project Data</b>", th_style), Paragraph("<b>Modeled Scenario Assumption (External / Simulated)</b>", th_style)],
    [Paragraph("Customer Outcome", td_style), Paragraph("Binary stated post-flight satisfaction (<i>Satisfied</i> vs. <i>Neutral/Dissatisfied</i>) across N = 124,685 surveys.", td_style), Paragraph("Assumed conversion from improved satisfaction into longitudinal repeat ticket purchases.", td_style)],
    [Paragraph("Feature Effects", td_style), Paragraph("Predictive associations, OLS t-stats, Random Forest Gini importance, and SHAP attributions.", td_style), Paragraph("Causal lift from upgrading Wi-Fi/boarding UX (requires controlled A/B testing to verify).", td_style)],
    [Paragraph("Financial & Capex ROI", td_style), Paragraph("Holdout dissatisfied cohort count (11,403 passengers) and predicted risk probabilities.", td_style), Paragraph("BTS $450 airfare, 4 trips/yr ($1,800 LTV), recovery save rates, and $6M–$8M Capex (Monte Carlo 95% CI: [$-1.75M, $9.30M]).", td_style)]
]
t_ev = Table(ev_data, colWidths=[1.45*inch, 2.75*inch, 2.80*inch])
t_ev.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2b6cb0")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e0")),
    ("TOPPADDING", (0,0), (-1,-1), 3.5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3.5),
]))
story.append(t_ev)

# 8. ADVANCED COMPONENT, MLOPS GOVERNANCE & REPRODUCIBILITY
story.append(Paragraph("8. Advanced Component, MLOps Governance & Reproducibility", h1_style))
story.append(Paragraph(
    "All preprocessing transformers and the fitted 100-tree Random Forest estimator are serialized into <code>artifacts/model.joblib</code> (<code>src/build_pipeline.py</code>). Automated <code>pytest</code> suites (<code>tests/test_pipeline.py</code>) validate schema integrity and prediction bounds, while <code>src/monitor_drift.py</code> tracks Population Stability Index (PSI) drift (<code>Online boarding</code> PSI = 0.0005; <code>Inflight wifi service</code> PSI = 0.0002) under explicit governance thresholds: <b>PSI &lt; 0.10</b> (stable), <b>0.10 &le; PSI &le; 0.25</b> (monitor & alert), and <b>PSI &gt; 0.25</b> (trigger automated model retraining).",
    body_style
))
story.append(Paragraph(
    "$ python src/test_artifact.py &amp;&amp; pytest<br/>"
    "Successfully loaded pipeline from artifacts/model.joblib (scikit-learn v1.9.1)<br/>"
    "Passenger 1 -&gt; Prediction: Neutral or Dissatisfied (Dissatisfaction Risk) | Satisfaction Probability: 0.00%<br/>"
    "Passenger 2 -&gt; Prediction: Satisfied | Satisfaction Probability: 95.00%",
    code_style
))

# 9. RECOMMENDATION, LIMITATIONS, AND NEXT STEPS
story.append(Paragraph("9. Recommendation, Limitations, and Next Steps", h1_style))
story.append(Paragraph("• <b>Phased Capital & Pilot Recommendation:</b> Prior to committing $6M–$8M fleet-wide, execute a <b>6-month randomized hub-route A/B pilot</b> upgrading Wi-Fi throughput and mobile boarding UX on treatment routes while tracking actual repeat bookings via frequent-flyer loyalty IDs. Deploy automated service-recovery vouchers when predicted dissatisfaction probability exceeds 82%.", bullet_style))
story.append(Paragraph("• <b>Known Limitations & Risks:</b> The structured dataset is cross-sectional, lacks individual ticket fare paid, and measures stated satisfaction rather than observed longitudinal churn. Price-elasticity differences across fare classes cannot be isolated without CRM booking logs.", bullet_style))

# 10. REFERENCES & FEEDBACK REVISION LOG
story.append(Paragraph("10. References & Instructor Feedback Revision Log", h1_style))
story.append(Paragraph("• Breiman, L. (2001). Random Forests. <i>Machine Learning</i>, 45(1), 5–32. &nbsp;|&nbsp; Salton, G., &amp; Buckley, C. (1988). Term-weighting approaches in automatic text retrieval. <i>IP&amp;M</i>, 24(5), 513–523.", bullet_style))
story.append(Paragraph("• Bureau of Transportation Statistics (BTS). (2023). <i>Annual U.S. Domestic Average Itinerary Fare</i>. &nbsp;|&nbsp; Delta News Hub (2023); Kaggle <i>Airline Passenger Satisfaction</i> &amp; <i>Airline Reviews</i> (CC0).", bullet_style))
story.append(Spacer(1, 4))

rev_data = [
    [Paragraph("<b>Checkpoint &amp; Deduction</b>", th_style), Paragraph("<b>Instructor Feedback</b>", th_style), Paragraph("<b>Revision Implemented</b>", th_style), Paragraph("<b>Artifact Location</b>", th_style)],
    [Paragraph("P1 Package (-5.0 provisional)", td_style), Paragraph("Rendered P1 infographic &amp; PDF missing from repository.", td_style), Paragraph("Exported and archived complete P1 PDF &amp; 1-page infographic.", td_style), Paragraph("checkpoints/p1/MSBA265_P1_Ignacio_Flores.pdf", td_style)],
    [Paragraph("P1 &amp; P2 Causal Framing (-3.0)", td_style), Paragraph("Survey satisfaction lacks observed retention; causal &amp; ROI claims overstated.", td_style), Paragraph("Reframed to predictive associations; added Observed vs. Modeled table &amp; 6-month A/B pilot.", td_style), Paragraph("README.md; Report Sec. 1, 2, 7, 9; Slides 4–7; app.py", td_style)],
    [Paragraph("P2 Peer Checklist (-1.0 provisional)", td_style), Paragraph("Three verification checkboxes on P2 validation PDF appeared blank.", td_style), Paragraph("Marked all 3 peer verification checkboxes (☑) on P2 form + completed new Final form.", td_style), Paragraph("checkpoints/p2/P2_Assignment_Validation_Signed.pdf", td_style)]
]
t_rev = Table(rev_data, colWidths=[1.45*inch, 1.85*inch, 2.05*inch, 1.65*inch])
t_rev.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a365d")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e0")),
    ("TOPPADDING", (0,0), (-1,-1), 3.5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3.5),
]))
story.append(t_rev)

doc.build(story)
print(f"Successfully generated Final Technical Report: {pdf_filename}")
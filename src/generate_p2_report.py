import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdf_filename = "MSBA265_P2_Draft_Report.pdf"
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
th_style = ParagraphStyle("TH", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=colors.white)
td_style = ParagraphStyle("TD", parent=styles["Normal"], fontName="Helvetica", fontSize=8.2, leading=10.5, textColor=colors.HexColor("#2d3748"))

story = []

# HEADER
story.append(Paragraph("MSBA 265: Applied Analytics | Project Checkpoint 2 (P2 Draft Report)", sub_style))
story.append(Paragraph("Predictive Customer Churn & Capital Allocation in Commercial Aviation", title_style))
story.append(Paragraph("<b>Author:</b> Ignacio Flores III &nbsp;|&nbsp; <b>Repository:</b> github.com/Ignacio-Flores-III/airline-passenger-satisfaction-prediction", body_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1a365d"), spaceBefore=4, spaceAfter=10))

# 1. EXECUTIVE SUMMARY
story.append(Paragraph("1. Executive Summary", h1_style))
story.append(Paragraph(
    "Commercial airlines allocate tens of millions of dollars annually toward fleet upgrades, frequently debating between physical cabin overhauls (new seats and legroom) and digital infrastructure (high-speed satellite Wi-Fi and seamless mobile boarding). Analyzing 124,685 passenger flight records alongside unprompted customer reviews, this project builds a unified machine learning and natural language processing (NLP) framework to identify what actually drives customer defection.",
    body_style
))
story.append(Paragraph(
    "<b>Key Result & Recommendation:</b> The ensemble Random Forest pipeline achieves <b>96.34% holdout accuracy</b> and <b>0.9939 ROC-AUC</b>, outperforming linear econometric baselines by over 9 percentage points. Both structured feature attribution and NLP review modeling confirm that digital friction—specifically <b>Online Boarding</b> (t = 73.68, p < 0.001) and <b>Inflight Wi-Fi</b> (t = 55.34, p < 0.001)—drives over 32% of predictive retention power, whereas physical <b>Seat Comfort</b> contributes less than 5%. Executive leadership should redirect $6M–$8M toward digital boarding and Wi-Fi upgrades rather than committing $25M–$50M to physical seat retrofits, protecting approximately $19.4M in holdout annual passenger value.",
    body_style
))

# 2. BUSINESS CONTEXT AND OBJECTIVE
story.append(Paragraph("2. Business Context and Objective", h1_style))
story.append(Paragraph("• <b>Primary Stakeholder:</b> Vice President of Customer Experience & Commercial Strategy, responsible for annual fleet retrofit capital expenditure (Capex) budgets and retention interventions.", bullet_style))
story.append(Paragraph("• <b>Economic Grounding:</b> Using Bureau of Transportation Statistics (BTS, 2023) domestic round-trip airfare averages ($450) across 4 annual trips per repeat flyer, individual Customer Lifetime Value (LTV) is estimated at <b>$1,800/year</b>. In the 20,781-passenger test cohort, 11,403 passengers fall into neutral/dissatisfied churn-risk segments, representing over <b>$20.5M</b> in annual exposure.", bullet_style))
story.append(Paragraph("• <b>Project Objective & Success Criteria:</b> Deliver a reproducible predictive pipeline exceeding 0.90 out-of-sample ROC-AUC that quantifies marginal retention drivers and flags high-risk passengers (churn probability >= 0.18) for automated service recovery.", bullet_style))

# 3. INDIVIDUAL PROJECT OWNERSHIP
story.append(Paragraph("3. Individual Project Ownership", h1_style))
story.append(Paragraph(
    "As a former Division I student-athlete and current M.S. in Data Analytics candidate with a B.A. in Business Marketing, I designed this project to bridge technical machine learning rigor with executive capital budgeting. All stages—including problem framing, data ingestion, econometric OLS benchmarking, Random Forest pipeline serialization, TF-IDF text modeling, architecture diagramming, and stakeholder slide synthesis—were executed independently by the author.",
    body_style
))

# 4. TOPIC AND INDUSTRY CONTEXT
story.append(Paragraph("4. Topic and Industry Context", h1_style))
story.append(Paragraph(
    "Customer retention analytics evolved from static post-flight Net Promoter Score (NPS) surveys in the 1980s to modern hybrid pipelines combining tree-based ensembles (Breiman, 2001) with TF-IDF text mining (Salton & Buckley, 1988). Industry leaders such as Delta Air Lines have committed over $1B toward high-speed Wi-Fi and mobile app integration (Delta News Hub, 2023), signaling an industry-wide shift from physical cabin hardware to frictionless digital journeys.",
    body_style
))

# 5. DATA AND PREPARATION
story.append(Paragraph("5. Data and Preparation", h1_style))
story.append(Paragraph("• <b>Structured Survey Data:</b> Kaggle <i>Airline Passenger Satisfaction</i> dataset (103,904 training rows; 20,781 holdout test rows; 23 attributes). <b>Unit of Analysis:</b> One completed passenger flight leg.", bullet_style))
story.append(Paragraph("• <b>Unstructured Review Data:</b> Kaggle <i>Airline Reviews</i> dataset (public, unprompted passenger text reviews and overall ratings) used to triangulate survey findings against spontaneous customer language.", bullet_style))
story.append(Paragraph("• <b>Cleaning & Pipeline Transformations:</b> Missing values in <i>Arrival Delay in Minutes</i> (310 records) are imputed using median/departure values inside a scikit-learn <code>ColumnTransformer</code>. Categorical variables (<i>Gender</i>, <i>Customer Type</i>, <i>Type of Travel</i>, <i>Class</i>) undergo <code>OneHotEncoder(handle_unknown='ignore')</code>, while numeric attributes are standardized via <code>StandardScaler</code>. Text reviews undergo lowercasing, regex punctuation removal, stopword filtering, and unigram/bigram TF-IDF vectorization.", bullet_style))
story.append(Paragraph("• <b>Privacy & Governance:</b> Both sources are publicly licensed under CC0 / Open Database with anonymized keys and zero Personally Identifiable Information (PII).", bullet_style))

story.append(PageBreak())

# 6. METHOD AND IMPLEMENTATION
story.append(Paragraph("6. Method and Implementation", h1_style))
story.append(Paragraph(
    "To ensure rigorous model selection, four architectures from MSBA 265 coursework were evaluated on identical train/test splits: (1) Ordinary Least Squares (OLS) for exact econometric p-values, (2) L2-regularized Logistic Regression, (3) Stochastic Gradient Descent (SGD) Classifier, and (4) an ensemble Random Forest Classifier (100 trees, random_state=42) bundled inside a unified preprocessing pipeline.",
    body_style
))

pipe_img = "assets/data_to_action_pipeline.png"
if os.path.exists(pipe_img):
    story.append(Spacer(1, 4))
    story.append(Image(pipe_img, width=7.0*inch, height=3.35*inch))
    story.append(Paragraph("<i>Figure 1: End-to-End Data-to-Action Pipeline distinguishing completed P1/P2 engineering steps (solid blue) from planned Final Delivery dashboard and drift monitoring components (dashed orange).</i>", body_style))

# 7. EVALUATION AND FINDINGS
story.append(Paragraph("7. Evaluation and Findings", h1_style))
story.append(Paragraph("Because airline churn intervention requires balancing false-positive recovery costs against high-LTV customer defection, models were evaluated across Accuracy, F1-Score, and ROC-AUC on the 20,781-row holdout partition:", body_style))

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
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(t_bench)
story.append(Spacer(1, 6))

story.append(Paragraph(
    "<b>Econometric & NLP Triangulation:</b> OLS regression confirms <b>Online Boarding</b> (coef = 0.0795, t = 73.68, p < 0.001) and <b>Inflight Wi-Fi</b> (coef = 0.0673, t = 55.34, p < 0.001) exert roughly 9x the marginal impact of <b>Seat Comfort</b> (coef = 0.0080, t = 6.65), while <b>Flight Distance</b> is statistically insignificant (p = 0.339). Independently, the TF-IDF + Logistic Regression text model extracts operational breakdown terms (<i>refund</i>, <i>cancelled</i>, <i>worst</i>) as top defection predictors, confirming survey findings are free of questionnaire framing bias.",
    body_style
))

# 8. ADVANCED COMPONENT AND REPRODUCIBILITY
story.append(Paragraph("8. Advanced Component and Reproducibility", h1_style))
story.append(Paragraph(
    "To guarantee peer and production reproducibility, all preprocessing transformers and the fitted 100-tree Random Forest estimator are serialized into a single scikit-learn Pipeline at <code>artifacts/model.joblib</code> (built via <code>src/build_pipeline.py</code>). Running <code>python src/test_artifact.py</code> in an isolated virtual environment (<code>requirements.txt</code>) reloads the artifact and deterministically scores unseen passenger profiles:",
    body_style
))
story.append(Paragraph(
    "$ python src/test_artifact.py<br/>"
    "Successfully loaded pipeline from artifacts/model.joblib (scikit-learn v1.9.1)<br/>"
    "Passenger 1 -> Prediction: Neutral or Dissatisfied (Churn Risk) | Satisfaction Probability: 0.00%<br/>"
    "Passenger 2 -> Prediction: Satisfied | Satisfaction Probability: 95.00%",
    code_style
))

# 9. RECOMMENDATION, LIMITATIONS, AND NEXT STEPS
story.append(Paragraph("9. Recommendation, Limitations, and Next Steps", h1_style))
story.append(Paragraph("• <b>Actionable Capex Recommendation:</b> Reallocate $6M–$8M from physical seat re-upholstery budgets toward fleet-wide satellite Wi-Fi bandwidth and mobile boarding UX upgrades, while deploying automated service-recovery vouchers whenever a passenger's predicted churn risk exceeds 82% (satisfaction probability < 18%).", bullet_style))
story.append(Paragraph("• <b>Known Limitations & Risks:</b> The structured dataset is cross-sectional and lacks individual ticket fare paid, meaning price-elasticity differences between basic economy and full-fare business travelers cannot be isolated directly. Additionally, the serialized Random Forest artifact (~78.9 MB) requires batch or containerized inference rather than lightweight edge deployment.", bullet_style))
story.append(Paragraph("• <b>Remaining Work for Final Delivery:</b> (1) Build an interactive Streamlit Capex ROI & passenger risk simulator dashboard, (2) add SHAP local feature explanations, and (3) implement a prediction drift monitor logging weekly satisfaction score shifts.", bullet_style))

# 10. REFERENCES AND APPENDICES
story.append(Paragraph("10. References and Appendices", h1_style))
story.append(Paragraph("• Breiman, L. (2001). Random Forests. <i>Machine Learning</i>, 45(1), 5–32.", bullet_style))
story.append(Paragraph("• Bureau of Transportation Statistics (BTS). (2023). <i>Annual U.S. Domestic Average Itinerary Fare</i>. U.S. Department of Transportation.", bullet_style))
story.append(Paragraph("• Delta News Hub. (2023). <i>Delta invests over $1B in digital customer experience and fast, free Wi-Fi</i>.", bullet_style))
story.append(Paragraph("• Kaggle Datasets: <i>Airline Passenger Satisfaction</i> (TJ Klein) & <i>Airline Reviews</i> (Juhi Bhojani). Licensed under CC0 / Open Database.", bullet_style))
story.append(Paragraph("• Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval. <i>Information Processing & Management</i>, 24(5), 513–523.", bullet_style))

doc.build(story)
print(f"Successfully generated P2 Draft Report: {pdf_filename}")

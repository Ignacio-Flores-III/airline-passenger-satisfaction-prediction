import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

os.makedirs("reports", exist_ok=True)

SLIDES = [
    ("1. The Capital Allocation Dilemma", "Where should we test fleet upgrade dollars to reduce dissatisfaction risk?", [
        ("The Budget Choice", "Physical cabin seat overhauls cost $25M–$50M fleet-wide, while high-speed Wi-Fi and mobile boarding upgrades cost $6M–$8M."),
        ("Scenario Revenue Benchmark", "Using BTS industry averages ($450 round-trip fare across 4 annual trips), illustrative repeat flyer value is modeled at ~$1,800/year."),
        ("Dissatisfaction Segment", "In our 20,781-passenger holdout cohort, 11,403 flyers fall into neutral/dissatisfied segments (~$20.5M modeled annual exposure)."),
        ("The Core Question", "Is stated passenger dissatisfaction most strongly associated with seat padding, or with digital and operational friction?")
    ], None),
    ("2. What Customer Information We Examined", "Combining structured post-flight survey ratings with unprompted passenger reviews", [
        ("124,685 Flight Surveys", "Analyzed stated passenger satisfaction across 23 journey touchpoints—from online booking and gate boarding to Wi-Fi, seat comfort, and arrival delays."),
        ("Unprompted Customer Reviews", "Examined written public airline reviews via TF-IDF NLP to verify what flyers complain about outside structured survey scales."),
        ("Observed vs. Modeled Split", "Separated directly observed survey satisfaction and model accuracy from external economic retention assumptions.")
    ], "assets/target_distribution_by_class.png"),
    ("3. Model Selection & Out-of-Sample Benchmark", "Unified Random Forest outperforms linear baselines by +8.8% holdout accuracy", [
        ("96.34% Holdout Accuracy", "Unified ColumnTransformer + Random Forest achieves 0.9939 ROC-AUC and 0.9576 F1 on 20,781 unseen records."),
        ("Non-Linear Interactions", "Captures conditional thresholds where combined arrival delays and low Wi-Fi scores sharply elevate dissatisfaction risk."),
        ("Verified Confusion Matrix", "Balanced precision and recall minimize false-positive recovery offers while catching high-risk flyers.")
    ], "assets/course_models_benchmark.png"),
    ("4. Diagnostic Error & Delay Threshold Analysis", "Confusion matrix precision and arrival delay tipping points", [
        ("High Holdout Precision", "Confusion matrix confirms balanced classification performance across both satisfied and dissatisfied cohorts."),
        ("Operational Delay Friction", "Satisfaction drops sharply once arrival delays exceed 15–20 minutes, compounding digital friction."),
        ("Actionable Trigger", "Combining operational delay logs with digital touchpoint scores enables automated, real-time recovery.")
    ], "assets/confusion_matrix_heatmap.png"),
    ("5. Key Finding: Digital Friction Dominates Predictions", "Digital touchpoints show >6x stronger predictive association with satisfaction than seat comfort", [
        ("Digital Touchpoints Lead", "Online Boarding and Inflight Wi-Fi account for over 32% of Random Forest predictive importance."),
        ("Low Predictive Weight on Seats", "Physical seat comfort contributes less than 5% of predictive power—suggesting a $35M seat overhaul is unlikely to lift satisfaction scores."),
        ("Consistent Across Segments", "Digital friction dominates across both business and personal travel cohorts.")
    ], "assets/satisfaction_feature_importance.png"),
    ("6. Explainable AI: SHAP Marginal Feature Attribution", "TreeExplainer confirms directional downward pull of digital upgrades on risk", [
        ("Individual-Level Transparency", "SHAP values quantify exactly how much each touchpoint pushes an individual passenger toward or away from dissatisfaction."),
        ("Top Marginal Drivers", "High Online Boarding (4–5) and Inflight Wi-Fi ratings exert the strongest downward pull on predicted dissatisfaction probability."),
        ("Executive Auditability", "Replaces black-box scoring with transparent feature attributions in our live Streamlit simulator.")
    ], "assets/shap_summary.png"),
    ("7. NLP Triangulation: Unprompted Passenger Reviews", "Spontaneous customer language independently confirms operational & digital pain points", [
        ("Zero Survey Framing Bias", "TF-IDF + Logistic Regression trained on unprompted public airline reviews validates structured survey findings."),
        ("Top Dissatisfaction Terms", "Operational breakdown terms ('refund', 'cancelled', 'worst', 'delay') dominate negative review predictions."),
        ("Unified Evidence Base", "Both structured ratings and free-text complaints point away from seat padding toward journey reliability.")
    ], "assets/nlp_sentiment_drivers.png"),
    ("8. End-to-End MLOps Architecture & Drift Governance", "Production-ready artifact with automated pytest validation and PSI monitoring", [
        ("Serialized Pipeline Artifact", "Unified preprocessing and Random Forest model packaged in artifacts/model.joblib with automated pytest verification."),
        ("PSI Drift Thresholds", "Population Stability Index tracks feature drift: PSI < 0.10 (stable), 0.10–0.25 (monitor), > 0.25 (retrain)."),
        ("Live Interactive Simulator", "Deployed Streamlit Capex & Satisfaction Simulator lets executives test passenger profiles and ROI scenarios.")
    ], "assets/data_to_action_pipeline.png"),
    ("9. Monte Carlo Risk & Phased Pilot Recommendation", "Validate digital ROI via a 6-month hub-route A/B pilot before fleet-wide Capex rollout", [
        ("1,000-Trial Monte Carlo CI", "Varying fare, repeat frequency, recovery save rate, and $6M–$8M Capex yields a modeled Year-1 net value 95% CI of [$-1.75M, $9.30M]."),
        ("6-Month Hub-Route A/B Pilot", "Upgrade Wi-Fi and mobile boarding on treatment routes first, tracking actual repeat bookings via loyalty IDs."),
        ("Automated Service Recovery", "Deploy targeted recovery vouchers when predicted dissatisfaction risk exceeds 82%.")
    ], "assets/monte_carlo_roi.png"),
    ("10. Observational Boundaries & Revision Governance", "Transparent distinction between survey correlations and longitudinal booking proof", [
        ("Boundary — Cross-Sectional Data", "Survey records measure single-flight stated satisfaction rather than multi-year repeat ticket purchases or exact fare paid."),
        ("Mitigation — Controlled Pilot", "The 6-month loyalty-ID A/B pilot directly measures causal retention lift prior to full fleet Capex commitment."),
        ("Complete Revision Governance", "P1/P2 checkpoints, HTML/PDF reports, live simulator, and signed peer validation logs are archived on GitHub.")
    ], "assets/economic_value_created.png"),
]

# 1. BUILD POWERPOINT (.pptx)
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

NAVY_RGB = RGBColor(26, 54, 93)
BLUE_RGB = RGBColor(43, 108, 176)
DARK_RGB = RGBColor(45, 55, 72)

s1 = prs.slides.add_slide(prs.slide_layouts[6])
bg = s1.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg.fill.solid()
bg.fill.fore_color.rgb = NAVY_RGB
bg.line.fill.background()

tbox = s1.shapes.add_textbox(Inches(0.9), Inches(2.2), Inches(11.5), Inches(3.2))
ttf = tbox.text_frame
ttf.word_wrap = True
p = ttf.paragraphs[0]
p.text = "Passenger Satisfaction Prediction & Fleet Capex Allocation"
p.font.size = Pt(38)
p.font.bold = True
p.font.color.rgb = RGBColor(255, 255, 255)

sub = ttf.add_paragraph()
sub.space_before = Pt(14)
sub.text = "Data-Driven Investment Strategy: Digital Experience vs. Physical Cabin Seating\nPrepared for: VP of Customer Experience & Commercial Strategy | Ignacio Flores III (Final Project Delivery)"
sub.font.size = Pt(18)
sub.font.color.rgb = RGBColor(190, 227, 248)

for title_text, subtitle_text, bullets, image_path in SLIDES:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    header = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(1.25))
    header.fill.solid()
    header.fill.fore_color.rgb = NAVY_RGB
    header.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.22), Inches(12.1), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(25)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(190, 227, 248)

    has_img = image_path and os.path.exists(image_path)
    body_width = Inches(5.9) if has_img else Inches(12.0)
    btb = slide.shapes.add_textbox(Inches(0.6), Inches(1.55), body_width, Inches(5.4))
    btf = btb.text_frame
    btf.word_wrap = True

    for i, (head, desc) in enumerate(bullets):
        bp = btf.paragraphs[0] if i == 0 else btf.add_paragraph()
        bp.space_after = Pt(14)
        r1 = bp.add_run()
        r1.text = f"▪ {head}: "
        r1.font.bold = True
        r1.font.size = Pt(16)
        r1.font.color.rgb = BLUE_RGB

        r2 = bp.add_run()
        r2.text = desc
        r2.font.size = Pt(15)
        r2.font.color.rgb = DARK_RGB

    if has_img:
        slide.shapes.add_picture(image_path, Inches(6.75), Inches(1.6), width=Inches(6.0))

out_pptx = "reports/Stakeholder_Presentation.pptx"
prs.save(out_pptx)

# 2. BUILD MATCHING PDF (.pdf)
PAGE_W, PAGE_H = landscape(letter)
out_pdf = "reports/Stakeholder_Presentation.pdf"
doc = SimpleDocTemplate(out_pdf, pagesize=landscape(letter), leftMargin=36, rightMargin=36, topMargin=30, bottomMargin=28)
styles = getSampleStyleSheet()

NAVY_HEX = colors.HexColor("#1a365d")
DARK_HEX = colors.HexColor("#2d3748")

title_s = ParagraphStyle("T", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=21, leading=25, textColor=colors.white)
b_s = ParagraphStyle("B", parent=styles["Normal"], fontName="Helvetica", fontSize=12.5, leading=17, textColor=DARK_HEX, spaceAfter=12)
hero_t = ParagraphStyle("HT", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=30, leading=36, textColor=colors.white)

story = []
t1 = Table([[Paragraph("Passenger Satisfaction Prediction &amp; Fleet Capex Allocation<br/><br/><font size=14 color=#bee3f8>Data-Driven Investment Strategy: Digital Experience vs. Physical Cabin Seating<br/>Prepared for: VP of Customer Experience &amp; Commercial Strategy | Ignacio Flores III (Final Project Delivery)</font>", hero_t)]], colWidths=[PAGE_W - 84], rowHeights=[PAGE_H - 84])
t1.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), NAVY_HEX), ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (0,0), (-1,-1), 32), ("RIGHTPADDING", (0,0), (-1,-1), 32)]))
story.append(t1)
story.append(PageBreak())

for idx, (stitle, ssub, bullets, img_path) in enumerate(SLIDES):
    hdr = Table([[Paragraph(f"{stitle}<br/><font size=11 color=#bee3f8>{ssub}</font>", title_s)]], colWidths=[PAGE_W - 84])
    hdr.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), NAVY_HEX), ("TOPPADDING", (0,0), (-1,-1), 12), ("BOTTOMPADDING", (0,0), (-1,-1), 12), ("LEFTPADDING", (0,0), (-1,-1), 18)]))
    story.append(hdr)
    story.append(Spacer(1, 18))
    b_flow = [Paragraph(f"<b><font color=#2b6cb0>▪ {h}:</font></b> {d}", b_s) for h, d in bullets]
    if img_path and os.path.exists(img_path):
        body_tbl = Table([[b_flow, Image(img_path, width=4.7*inch, height=3.2*inch)]], colWidths=[5.0*inch, 4.7*inch])
        body_tbl.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP")]))
        story.append(body_tbl)
    else:
        for p in b_flow:
            story.append(p)
    if idx < len(SLIDES) - 1:
        story.append(PageBreak())

doc.build(story)
print(f"Successfully generated {out_pptx} and {out_pdf} with all diagnostic, SHAP, NLP, and Monte Carlo charts!")
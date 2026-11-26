import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

NAVY = RGBColor(26, 54, 93)
BLUE = RGBColor(43, 108, 176)
ORANGE = RGBColor(221, 107, 32)
DARK = RGBColor(45, 55, 72)
LIGHT_BG = RGBColor(247, 250, 252)

def add_slide(title_text, subtitle_text, bullets, image_path=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Top header bar
    header = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(1.25))
    header.fill.solid()
    header.fill.fore_color.rgb = NAVY
    header.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.22), Inches(12.1), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(190, 227, 248)

    # Content area
    body_width = Inches(6.0) if image_path else Inches(12.0)
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
        r1.font.color.rgb = BLUE

        r2 = bp.add_run()
        r2.text = desc
        r2.font.size = Pt(15)
        r2.font.color.rgb = DARK

    if image_path and os.path.exists(image_path):
        slide.shapes.add_picture(image_path, Inches(6.8), Inches(1.65), width=Inches(5.9))

# SLIDE 1: TITLE SLIDE
s1 = prs.slides.add_slide(prs.slide_layouts[6])
bg = s1.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg.fill.solid()
bg.fill.fore_color.rgb = NAVY
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

# SLIDE 2: THE STAKEHOLDER PROBLEM
add_slide(
    "1. The Capital Allocation Dilemma",
    "Where should we test fleet upgrade dollars to reduce dissatisfaction risk?",
    [
        ("The Budget Choice", "Physical cabin seat overhauls cost $25M–$50M fleet-wide, while high-speed Wi-Fi and mobile boarding upgrades cost $6M–$8M."),
        ("Scenario Revenue Benchmark", "Using BTS industry averages ($450 round-trip fare across 4 annual trips), illustrative repeat flyer value is modeled at ~$1,800/year."),
        ("Dissatisfaction Segment", "In our 20,781-passenger holdout cohort, 11,403 flyers fall into neutral/dissatisfied segments—representing ~$20.5M in modeled annual exposure."),
        ("The Core Question", "Is stated passenger dissatisfaction most strongly associated with seat padding, or with digital and operational friction?")
    ]
)

# SLIDE 3: INFORMATION EXAMINED
add_slide(
    "2. What Customer Information We Examined",
    "Combining structured post-flight survey ratings with unprompted passenger reviews",
    [
        ("124,685 Flight Surveys", "Analyzed stated passenger satisfaction across 23 journey touchpoints—from online booking and gate boarding to Wi-Fi, seat comfort, and arrival delays."),
        ("Unprompted Customer Reviews", "Examined written public airline reviews via TF-IDF NLP to verify what flyers complain about outside structured survey scales."),
        ("Observed vs. Modeled Split", "Separated directly observed survey satisfaction and model accuracy from external economic retention assumptions.")
    ]
)

# SLIDE 4: KEY FINDING
add_slide(
    "3. Key Finding: Digital Friction Dominates Predictions",
    "Digital touchpoints show >6x stronger predictive association with satisfaction than seat comfort",
    [
        ("Digital Touchpoints Lead", "Online Boarding and Inflight Wi-Fi account for over 32% of Random Forest predictive importance and top SHAP attribution."),
        ("Low Predictive Weight on Seats", "Physical seat comfort contributes less than 5% of predictive power—suggesting a $35M seat overhaul is unlikely to lift satisfaction scores."),
        ("Confirmed by Written Reviews", "Customer review text independently highlights operational and digital failures ('cancelled', 'refund', 'worst') rather than seat dimensions.")
    ],
    image_path="assets/satisfaction_feature_importance.png"
)

# SLIDE 5: HOW THE SOLUTION WORKS
add_slide(
    "4. How Our Early-Warning & MLOps System Works",
    "Automated risk scoring and PSI drift governance flag dissatisfied flyers in real time",
    [
        ("96.34% Holdout Accuracy", "Our unified Random Forest pipeline achieves 0.9939 ROC-AUC on unseen holdout records using routine operational touchpoint logs."),
        ("SHAP & Live Simulator", "Interactive Streamlit simulator pairs individual SHAP explanations with a 1,000-trial Monte Carlo Capex scenario optimizer."),
        ("MLOps Drift Governance", "Automated pytest suite and PSI monitoring (stable < 0.10, monitor 0.10–0.25, retrain > 0.25) ensure reliable production scoring.")
    ],
    image_path="assets/data_to_action_pipeline.png"
)

# SLIDE 6: STRATEGIC RECOMMENDATION
add_slide(
    "5. Recommended Phased Executive Action",
    "Validate digital ROI via a controlled hub-route pilot before fleet-wide Capex rollout",
    [
        ("1. Launch 6-Month Hub-Route A/B Pilot", "Upgrade satellite Wi-Fi and mobile boarding UX on treatment routes ($6M–$8M scope) and measure actual repeat bookings via loyalty IDs."),
        ("2. Deploy Automated Service Recovery", "Trigger targeted recovery vouchers when predicted dissatisfaction probability exceeds 82% after combined Wi-Fi and delay friction."),
        ("3. Modeled Scenario Upside", "Across 1,000 Monte Carlo trials, modeled Year-1 net value spans [$-1.75M, $9.30M] before recurring Year-2+ cash flows.")
    ]
)

# SLIDE 7: LIMITATIONS & GOVERNANCE
add_slide(
    "6. Observational Boundaries & Governance",
    "Transparent distinction between survey correlations and longitudinal booking proof",
    [
        ("Boundary — Cross-Sectional Data", "Public survey records measure single-flight stated satisfaction rather than multi-year repeat ticket purchases or exact fare paid."),
        ("Mitigation — Controlled Pilot", "The 6-month loyalty-ID A/B pilot directly measures causal retention lift prior to full fleet Capex commitment."),
        ("Completed Deliverables", "Full code, HTML report, PDF/PPTX deliverables, SHAP/Monte Carlo diagnostics, and peer validation logs are archived on GitHub.")
    ]
)

os.makedirs("reports", exist_ok=True)
out_pptx = "reports/Stakeholder_Presentation.pptx"
prs.save(out_pptx)
print(f"Successfully generated Final Stakeholder PowerPoint: {out_pptx}")
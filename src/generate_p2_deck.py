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
p.text = "Protecting Repeat Flyers & Optimizing Fleet Capex"
p.font.size = Pt(38)
p.font.bold = True
p.font.color.rgb = RGBColor(255, 255, 255)

sub = ttf.add_paragraph()
sub.space_before = Pt(14)
sub.text = "Data-Driven Investment Strategy: Digital Experience vs. Physical Cabin Seating\nPrepared for: VP of Customer Experience & Commercial Strategy | Ignacio Flores III (Draft P2)"
sub.font.size = Pt(18)
sub.font.color.rgb = RGBColor(190, 227, 248)

# SLIDE 2: THE STAKEHOLDER PROBLEM
add_slide(
    "1. The Capital Allocation Dilemma",
    "Where should we invest fleet upgrade dollars to prevent customer defection?",
    [
        ("The Budget Choice", "Physical cabin seat overhauls cost $25M–$50M fleet-wide, while high-speed Wi-Fi and mobile boarding upgrades cost $6M–$8M."),
        ("The Revenue at Stake", "Each repeat flyer generates ~$1,800 in annual ticket revenue ($450 average fare across 4 trips/year)."),
        ("Exposure Identified", "Across our 20,781-passenger validation cohort, over $19.4M in annual repeat revenue is at risk of defection."),
        ("The Core Question", "Do flyers leave because of seat padding, or because of digital and operational friction?")
    ]
)

# SLIDE 3: INFORMATION EXAMINED
add_slide(
    "2. What Customer Information We Examined",
    "Combining structured post-flight ratings with unprompted passenger reviews",
    [
        ("124,685 Flight Journeys", "Analyzed passenger satisfaction across 23 journey touchpoints—from online booking and gate boarding to Wi-Fi, seat comfort, and arrival delays."),
        ("Unprompted Customer Reviews", "Examined thousands of written public airline reviews to verify what flyers complain about when not prompted by a survey scale."),
        ("Business vs. Personal Flyers", "Separated loyalty segments and trip purposes to pinpoint where repeat revenue is most vulnerable.")
    ]
)

# SLIDE 4: KEY FINDING
add_slide(
    "3. Key Finding: Digital Friction Drives Defection",
    "Passengers forgive average seat comfort, but defect over broken digital touchpoints",
    [
        ("Digital Touchpoints Dominate", "Online Boarding and Inflight Wi-Fi account for over 32% of customer retention power."),
        ("Low Return on Seat Retrofits", "Physical seat comfort accounts for less than 5% of retention—meaning a $35M seat overhaul yields minimal loyalty lift."),
        ("Confirmed by Written Reviews", "Customer review text independently highlights operational and digital failures ('cancelled', 'refund', 'worst') rather than seat dimensions.")
    ],
    image_path="assets/satisfaction_feature_importance.png"
)

# SLIDE 5: HOW THE SOLUTION WORKS
add_slide(
    "4. How Our Early-Warning System Works",
    "Automated risk scoring flags dissatisfied flyers before they switch airlines",
    [
        ("96% Prediction Accuracy", "Our automated decision tool accurately identifies 96 out of 100 at-risk flyers using routine post-flight operational logs."),
        ("Proactive Recovery Trigger", "When a flyer experiences combined delay and Wi-Fi friction, the system flags them immediately for targeted recovery."),
        ("Built for Daily Operations", "The entire scoring tool is packaged and verified for seamless integration into customer experience workflows.")
    ],
    image_path="assets/data_to_action_pipeline.png"
)

# SLIDE 6: STRATEGIC RECOMMENDATION
add_slide(
    "5. Recommended Executive Action",
    "Shift capital from physical seat retrofits to digital reliability and proactive recovery",
    [
        ("1. Prioritize Digital Capex ($6M–$8M)", "Fund fleet-wide satellite Wi-Fi reliability and streamlined mobile boarding before approving physical seat re-upholstery."),
        ("2. Deploy Automated Service Recovery", "Automatically issue bonus miles or lounge passes to high-value flyers flagged after Wi-Fi outages or delays."),
        ("3. Expected Financial Impact", "Avoids $25M+ in low-yield physical capex while protecting over $19M in annual repeat passenger revenue.")
    ]
)

# SLIDE 7: LIMITATIONS & NEXT STEPS
add_slide(
    "6. Limitations & Next Steps to Final Rollout",
    "Transparent constraints and immediate milestones before full deployment",
    [
        ("Limitation — Fare Elasticity", "Current flight records do not capture exact ticket price paid; future integration with fare buckets will refine recovery offer sizing."),
        ("Limitation — Snapshot Timing", "Data reflects single flight legs rather than multi-year flyer histories."),
        ("Next Step — Executive Simulator", "Delivering an interactive Capex & Recovery Simulator dashboard for final stakeholder review.")
    ]
)

out_pptx = "P2_Stakeholder_Deck.pptx"
prs.save(out_pptx)
print(f"Successfully generated Stakeholder PowerPoint: {out_pptx}")

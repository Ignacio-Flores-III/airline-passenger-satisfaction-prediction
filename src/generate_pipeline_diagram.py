import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(13, 6.2), dpi=300)
ax.set_xlim(0, 13)
ax.set_ylim(0, 6.2)
ax.axis("off")

# Title & Legend Header
ax.text(0.4, 5.75, "END-TO-END DATA-TO-ACTION PIPELINE: AIRLINE CHURN & CAPEX ALLOCATION",
        fontsize=12.5, fontweight="bold", color="#1a365d", family="sans-serif")

comp_badge = patches.FancyBboxPatch((8.8, 5.65), 1.7, 0.32, boxstyle="round,pad=0.05",
                                    facecolor="#ebf8ff", edgecolor="#2b6cb0", linewidth=1.5)
ax.add_patch(comp_badge)
ax.text(9.65, 5.81, "COMPLETED (P1/P2)", fontsize=7.5, fontweight="bold", color="#2b6cb0", ha="center", va="center")

plan_badge = patches.FancyBboxPatch((10.8, 5.65), 1.8, 0.32, boxstyle="round,pad=0.05",
                                    facecolor="#fffaf0", edgecolor="#dd6b20", linewidth=1.5, linestyle="--")
ax.add_patch(plan_badge)
ax.text(11.7, 5.81, "PLANNED (FINAL)", fontsize=7.5, fontweight="bold", color="#dd6b20", ha="center", va="center")

def draw_node(x, y, w, h, icon_txt, title, subtitle, status="completed"):
    if status == "completed":
        bg, edge, lstyle, badge_col = "#f7fafc", "#2b6cb0", "-", "#2b6cb0"
    else:
        bg, edge, lstyle, badge_col = "#fffaf0", "#dd6b20", "--", "#dd6b20"

    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                                 facecolor=bg, edgecolor=edge, linewidth=1.8, linestyle=lstyle)
    ax.add_patch(box)

    circ = patches.Circle((x + w/2, y + h - 0.35), 0.22, facecolor=badge_col, edgecolor="none")
    ax.add_patch(circ)
    ax.text(x + w/2, y + h - 0.35, icon_txt, fontsize=8, fontweight="bold", color="white", ha="center", va="center")

    ax.text(x + w/2, y + 0.52, title, fontsize=8.5, fontweight="bold", color="#1a202c", ha="center", va="center")
    ax.text(x + w/2, y + 0.22, subtitle, fontsize=7.2, color="#4a5568", ha="center", va="center")

# TOP ROW (Left to Right): Ingestion -> Prep -> Modeling -> Artifact
draw_node(0.4, 3.6, 2.3, 1.45, "DB", "DATA SOURCES", "Kaggle CSVs (103k rows)\n& Airline Text Reviews", "completed")
draw_node(3.5, 3.6, 2.3, 1.45, "PY", "PYTHON ETL & NLP", "pandas Impute/IQR Cap\n& TF-IDF Vectorizer", "completed")
draw_node(6.6, 3.6, 2.3, 1.45, "ML", "MODEL TRAINING", "Random Forest (96.3%)\n+ Logit NLP Benchmark", "completed")
draw_node(9.7, 3.6, 2.5, 1.45, "PKL", "SAVED ARTIFACT", "artifacts/model.joblib\nVerified Pipeline Handoff", "completed")

# BOTTOM ROW (Right to Left): Inference -> Dashboard -> Executive Action -> Drift
draw_node(9.7, 1.1, 2.5, 1.45, "API", "BATCH / LIVE SCORING", "Score Unseen Flights\nFlag Churn Prob >= 0.18", "completed")
draw_node(6.6, 1.1, 2.3, 1.45, "UI", "DECISION DASHBOARD", "Streamlit Capex ROI\n& Friction Simulator", "planned")
draw_node(3.5, 1.1, 2.3, 1.45, "VP", "STAKEHOLDER ACTION", "VP Customer Experience\nAllocates Wi-Fi Capex", "planned")
draw_node(0.4, 1.1, 2.3, 1.45, "OPS", "OUTCOME & DRIFT", "Track Retention Lift\n& Feature Drift Alerts", "planned")

# Arrows connecting Top Row (Left -> Right)
arrow_kw = dict(arrowstyle="-|>,head_width=0.25,head_length=0.35", lw=1.8, color="#2b6cb0")
ax.annotate("", xy=(3.42, 4.32), xytext=(2.78, 4.32), arrowprops=arrow_kw)
ax.annotate("", xy=(6.52, 4.32), xytext=(5.88, 4.32), arrowprops=arrow_kw)
ax.annotate("", xy=(9.62, 4.32), xytext=(8.98, 4.32), arrowprops=arrow_kw)

# Downward arrow (Saved Artifact -> Scoring)
ax.annotate("", xy=(10.95, 2.65), xytext=(10.95, 3.52), arrowprops=arrow_kw)

# Arrows connecting Bottom Row (Right -> Left)
plan_arrow_kw = dict(arrowstyle="-|>,head_width=0.25,head_length=0.35", lw=1.8, color="#dd6b20", linestyle="--")
ax.annotate("", xy=(8.98, 1.82), xytext=(9.62, 1.82), arrowprops=plan_arrow_kw)
ax.annotate("", xy=(5.88, 1.82), xytext=(6.52, 1.82), arrowprops=plan_arrow_kw)
ax.annotate("", xy=(2.78, 1.82), xytext=(3.42, 1.82), arrowprops=plan_arrow_kw)

# Feedback Loop Arrow (Outcome & Drift -> Data Sources)
ax.annotate("", xy=(1.55, 3.52), xytext=(1.55, 2.65),
            arrowprops=dict(arrowstyle="-|>,head_width=0.25,head_length=0.35", lw=1.8, color="#dd6b20", linestyle=":"))
ax.text(1.65, 3.08, "Feedback &\nDrift Refresh", fontsize=7, fontweight="bold", color="#dd6b20", va="center")

# Footer citation note
ax.text(0.4, 0.45, "Source: Author-generated architecture diagram (matplotlib). Solid blue = Completed in P1/P2; Dashed orange = Planned for Final Delivery.",
        fontsize=7, style="italic", color="#718096")

os.makedirs("assets", exist_ok=True)
out_path = "assets/data_to_action_pipeline.png"
plt.tight_layout()
plt.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"Successfully generated pipeline diagram: {out_path}")

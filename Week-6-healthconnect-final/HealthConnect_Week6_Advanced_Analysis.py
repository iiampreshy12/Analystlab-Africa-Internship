"""
HealthConnect Clinic - Week 6 Advanced Analytics & Decision Support
AnalystLab Africa Experience Lab
Author: Osagie Osagieduwa Precious

Builds directly on the Week 5 EDA and KPI calculations (see
HealthConnect_Week5_Data_Analysis.py). This script does NOT repeat
the full Week 5 EDA — it deepens the strongest Week 5 finding
(prior no-show history), validates it against other factors, builds
a combined patient risk segmentation, refreshes the dashboard with
that new view, and exports a handoff file for the Data Science track.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch

df = pd.read_csv(r"G:\My Drive\Analystlab Projects\Week-6-healthconnect-project-final\HealthConnect_Appointment_Data_Cleaned.csv")


def no_show_rate(series):
    """Return the % of records with outcome 'No-Show', rounded to 1dp."""
    return round((series == "No-Show").mean() * 100, 1)


# ---------------------------------------------------------------
# Recreate the Week 5 bands (inputs needed for Week 6 analysis)
# ---------------------------------------------------------------
df["lead_band"] = pd.cut(df["booking_lead_days"], bins=[-1, 0, 7, 999],
                          labels=["Same-day", "1-7 days", "8+ days"])
df["prior_band"] = pd.cut(df["previous_no_shows"], bins=[-1, 0, 1, 2, 100],
                           labels=["0 prior", "1 prior", "2 prior", "3+ prior"])
df["distance_band"] = pd.cut(df["distance_to_clinic_km"], bins=[0, 5, 10, 20, 100],
                              labels=["0-5km", "5-10km", "10-20km", "20+km"])

# =================================================================
# PART A: Deepening & validating the strongest Week 5 finding
# (prior no-show history: 43.5% -> 68.8%). Does it hold once
# checked against other factors, or mask something more specific?
# =================================================================
print("=" * 70)
print("PART A: Validating & deepening the prior no-show history finding")
print("=" * 70)

interaction_lead = df.groupby(["prior_band", "lead_band"], observed=True)["appointment_outcome"].apply(no_show_rate)
print("\nA1 - No-Show Rate by Prior History x Lead Time (interaction check):")
print(interaction_lead.unstack())

interaction_dist = df.groupby(["prior_band", "distance_band"], observed=True)["appointment_outcome"].apply(no_show_rate)
print("\nA2 - No-Show Rate by Prior History x Distance to Clinic:")
print(interaction_dist.unstack())

sample_sizes = df["prior_band"].value_counts()
print("\nA3 - Sample sizes behind the prior-history finding (reliability check):")
print(sample_sizes)

# =================================================================
# PART B: Combined patient risk segmentation (refined KPI)
# =================================================================
print("\n" + "=" * 70)
print("PART B: Combined patient no-show risk segmentation")
print("=" * 70)


def risk_score(row):
    """Additive risk score from the strongest Week 5/6 predictors."""
    score = 0
    if row["previous_no_shows"] >= 2:
        score += 1
    if row["booking_lead_days"] >= 8:
        score += 1
    if row["distance_to_clinic_km"] >= 20:
        score += 1
    if row["reminder_sent"] == "No":
        score += 1
    return score


df["risk_score"] = df.apply(risk_score, axis=1)
df["risk_segment"] = pd.cut(df["risk_score"], bins=[-1, 0, 1, 4],
                             labels=["Low", "Medium", "High"])

risk_rate = df.groupby("risk_segment", observed=True)["appointment_outcome"].apply(no_show_rate)
print("\nB1 - No-Show Rate by Combined Risk Segment:")
print(risk_rate)

risk_counts = df["risk_segment"].value_counts()
print("\nB2 - Patients per Risk Segment:")
print(risk_counts)

total_no_shows = (df["appointment_outcome"] == "No-Show").sum()
high_risk_no_shows = ((df["appointment_outcome"] == "No-Show") & (df["risk_segment"] == "High")).sum()
pct_no_shows_from_high_risk = round(high_risk_no_shows / total_no_shows * 100, 1)
print(f"\nB3 - Refined KPI: {pct_no_shows_from_high_risk}% of all no-shows come from "
      f"the High-risk segment ({high_risk_no_shows} of {total_no_shows} no-shows)")

# =================================================================
# PART C: Updated dashboard — adds the risk segmentation view,
# does not recreate the full Week 5 dashboard from scratch
# =================================================================
DARK_GREEN = "#1B5E20"
GREEN = "#4CAF50"
GOLD = "#FFD54F"
RED = "#C62828"
LIGHT_GREEN_BG = "#F1F8E9"

fig = plt.figure(figsize=(14, 12))
gs = gridspec.GridSpec(3, 2, height_ratios=[0.4, 0.9, 2], hspace=0.6, wspace=0.25)

ax_header = fig.add_subplot(gs[0, :])
ax_header.axis("off")
ax_header.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax_header.transAxes,
                                   facecolor=DARK_GREEN, edgecolor="none"))
ax_header.text(0.02, 0.5, "HEALTHCONNECT — WEEK 6 RISK SEGMENTATION UPDATE",
               transform=ax_header.transAxes, fontsize=13, fontweight="bold",
               color="white", va="center")
ax_header.text(0.98, 0.5, "AnalystLab Africa | Week 6",
               transform=ax_header.transAxes, fontsize=9, color=GOLD,
               va="center", ha="right")

kpi_data = [
    (f"{pct_no_shows_from_high_risk}%", "of No-Shows Come\nfrom High-Risk Segment"),
    (f"{int(risk_counts.get('High', 0)):,}", "Patients in\nHigh-Risk Segment"),
    (f"{risk_rate.get('High', 0)}%", "No-Show Rate\n(High Risk)"),
    (f"{risk_rate.get('Low', 0)}%", "No-Show Rate\n(Low Risk)"),
]
ax_kpi = fig.add_subplot(gs[1, :])
ax_kpi.axis("off")
for i, (value, label) in enumerate(kpi_data):
    x = i * 0.25
    box = FancyBboxPatch((x + 0.01, 0.05), 0.22, 0.9,
                          boxstyle="round,pad=0.02",
                          transform=ax_kpi.transAxes,
                          facecolor=LIGHT_GREEN_BG, edgecolor=DARK_GREEN, linewidth=1.2)
    ax_kpi.add_patch(box)
    ax_kpi.text(x + 0.12, 0.68, value, transform=ax_kpi.transAxes,
                fontsize=17, fontweight="bold", color=DARK_GREEN, ha="center")
    ax_kpi.text(x + 0.12, 0.22, label, transform=ax_kpi.transAxes,
                fontsize=8.5, color="#333333", ha="center")

ax1 = fig.add_subplot(gs[2, 0])
seg_order = ["Low", "Medium", "High"]
seg_vals = [risk_rate.get(s, 0) for s in seg_order]
bars = ax1.bar(seg_order, seg_vals, color=[GREEN, GOLD, RED], width=0.55)
ax1.set_title("No-Show Rate by Combined Risk Segment", fontweight="bold", color=DARK_GREEN)
for b, v in zip(bars, seg_vals):
    ax1.text(b.get_x() + b.get_width() / 2, v + 1, f"{v}%", ha="center",
              fontweight="bold", color=DARK_GREEN)
ax1.set_ylim(0, max(seg_vals) + 15)
ax1.spines[["top", "right"]].set_visible(False)

ax2 = fig.add_subplot(gs[2, 1])
seg_counts = [risk_counts.get(s, 0) for s in seg_order]
bars2 = ax2.bar(seg_order, seg_counts, color=[GREEN, GOLD, RED], width=0.55)
ax2.set_title("Patients per Risk Segment", fontweight="bold", color=DARK_GREEN)
for b, v in zip(bars2, seg_counts):
    ax2.text(b.get_x() + b.get_width() / 2, v + max(seg_counts) * 0.02, f"{v:,}",
              ha="center", fontweight="bold", color=DARK_GREEN)
ax2.spines[["top", "right"]].set_visible(False)

plt.savefig("HealthConnect_Week6_Dashboard.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
print("\nWeek 6 dashboard saved as HealthConnect_Week6_Dashboard.png")

# =================================================================
# PART D: Data Science handoff extract — evidence for the
# mandatory cross-track integration requirement
# =================================================================
handoff_cols = [
    "previous_no_shows", "booking_lead_days", "distance_to_clinic_km",
    "reminder_sent", "reminder_channel", "age_group", "gender",
    "appointment_type", "risk_score", "risk_segment", "appointment_outcome"
]
df[handoff_cols].to_csv("HealthConnect_Week6_DataScience_Handoff.csv", index=False)
print("\nData Science handoff file saved: HealthConnect_Week6_DataScience_Handoff.csv")
print("Columns included:", handoff_cols)

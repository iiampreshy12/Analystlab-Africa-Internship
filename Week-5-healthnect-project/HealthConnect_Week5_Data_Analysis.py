"""
HealthConnect Clinic - Week 5 Data Analytics
AnalystLab Africa Experience Lab
Author: Osagie Osagieduwa Precious

Expanded exploratory analysis + KPI calculation, building on the
Week 4 data quality assessment and cleaned dataset.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch

df = pd.read_csv("HealthConnect_Appointment_Data_Cleaned.csv")


def no_show_rate(series):
    """Return the % of records with outcome 'No-Show', rounded to 1dp."""
    return round((series == "No-Show").mean() * 100, 1)


# ---------------------------------------------------------------
# KPI 1: Overall No-Show Rate
# ---------------------------------------------------------------
overall_rate = no_show_rate(df["appointment_outcome"])
print("KPI 1 - Overall No-Show Rate:", overall_rate, "%")

# ---------------------------------------------------------------
# KPI 2: No-Show Rate by Booking Lead Time
# ---------------------------------------------------------------
bins = [-1, 0, 7, 999]
labels = ["Same-day", "1-7 days", "8+ days"]
df["lead_band"] = pd.cut(df["booking_lead_days"], bins=bins, labels=labels)
lead_time_rate = df.groupby("lead_band", observed=True)["appointment_outcome"].apply(no_show_rate)
print("\nKPI 2 - No-Show Rate by Lead Time:")
print(lead_time_rate)

# ---------------------------------------------------------------
# KPI 3: No-Show Rate by Prior No-Show History (strongest finding)
# ---------------------------------------------------------------
bins = [-1, 0, 1, 2, 100]
labels = ["0 prior", "1 prior", "2 prior", "3+ prior"]
df["prior_band"] = pd.cut(df["previous_no_shows"], bins=bins, labels=labels)
prior_rate = df.groupby("prior_band", observed=True)["appointment_outcome"].apply(no_show_rate)
print("\nKPI 3 - No-Show Rate by Prior No-Show History:")
print(prior_rate)

# ---------------------------------------------------------------
# KPI 4: Reminder Effectiveness Rate
# ---------------------------------------------------------------
reminder_rate = df.groupby("reminder_sent")["appointment_outcome"].apply(no_show_rate)
print("\nKPI 4 - No-Show Rate by Reminder Sent:")
print(reminder_rate)

channel_rate = df.groupby("reminder_channel")["appointment_outcome"].apply(no_show_rate)
print("\nNo-Show Rate by Reminder Channel:")
print(channel_rate)

# ---------------------------------------------------------------
# KPI 5: Lost Appointment Slots
# ---------------------------------------------------------------
lost_slots = (df["appointment_outcome"] == "No-Show").sum()
print("\nKPI 5 - Lost Appointment Slots:", lost_slots)

# For the "3+ prior no-shows" and "8+ day bookings" KPI cards on the dashboard
rate_3plus_prior = prior_rate["3+ prior"]
rate_8plus_days = lead_time_rate["8+ days"]

# ---------------------------------------------------------------
# Additional EDA: distance, demographics, appointment type
# ---------------------------------------------------------------
bins = [0, 5, 10, 20, 100]
labels = ["0-5km", "5-10km", "10-20km", "20+km"]
df["distance_band"] = pd.cut(df["distance_to_clinic_km"], bins=bins, labels=labels)
distance_rate = df.groupby("distance_band", observed=True)["appointment_outcome"].apply(no_show_rate)
print("\nNo-Show Rate by Distance to Clinic:")
print(distance_rate)

age_rate = df.groupby("age_group")["appointment_outcome"].apply(no_show_rate)
print("\nNo-Show Rate by Age Group:")
print(age_rate)

gender_rate = df.groupby("gender")["appointment_outcome"].apply(no_show_rate)
print("\nNo-Show Rate by Gender:")
print(gender_rate)

appt_type_rate = df.groupby("appointment_type")["appointment_outcome"].apply(no_show_rate)
print("\nNo-Show Rate by Appointment Type:")
print(appt_type_rate)

# ---------------------------------------------------------------
# Data quality note: waiting_time_minutes 60+ min band
# has only 3 records - flagged as unreliable, not used as a finding
# ---------------------------------------------------------------
bins = [0, 15, 30, 60, 999]
labels = ["0-15min", "15-30min", "30-60min", "60+min"]
df["wait_band"] = pd.cut(df["waiting_time_minutes"], bins=bins, labels=labels)
print("\nWaiting time band sample sizes (checking reliability):")
print(df["wait_band"].value_counts())

# =================================================================
# DASHBOARD — HealthConnect Clinic No-Show Analytics
# =================================================================
DARK_GREEN = "#1B5E20"
GREEN = "#4CAF50"
GOLD = "#FFD54F"
ORANGE = "#FFA726"
GREY = "#B0B0B0"
LIGHT_GREEN_BG = "#F1F8E9"

fig = plt.figure(figsize=(14, 18))
gs = gridspec.GridSpec(4, 2, height_ratios=[0.4, 0.9, 2, 2], hspace=0.7, wspace=0.25)

# ---- HEADER BANNER ----
ax_header = fig.add_subplot(gs[0, :])
ax_header.axis("off")
ax_header.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax_header.transAxes,
                                   facecolor=DARK_GREEN, edgecolor="none"))
ax_header.text(0.02, 0.5, "HEALTHCONNECT CLINIC — APPOINTMENT NO-SHOW ANALYTICS",
               transform=ax_header.transAxes, fontsize=13, fontweight="bold",
               color="white", va="center")
ax_header.text(0.98, 0.5, "AnalystLab Africa | Week 5",
               transform=ax_header.transAxes, fontsize=9, color=GOLD,
               va="center", ha="right")

# ---- KPI CARDS ----
kpi_data = [
    (f"{overall_rate}%", "Overall\nNo-Show Rate"),
    (f"{lost_slots:,}", "Lost Appointment\nSlots"),
    (f"{rate_8plus_days}%", "No-Show Rate\n(8+ day bookings)"),
    (f"{rate_3plus_prior}%", "No-Show Rate\n(3+ prior no-shows)"),
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
                fontsize=18, fontweight="bold", color=DARK_GREEN, ha="center")
    ax_kpi.text(x + 0.12, 0.22, label, transform=ax_kpi.transAxes,
                fontsize=8.5, color="#333333", ha="center")


def add_bar_chart(ax, series, title, colors, ylim):
    """Helper: draw a bar chart from a pandas Series with value labels."""
    bars = ax.bar(series.index.astype(str), series.values, color=colors, width=0.55)
    ax.set_title(title, fontweight="bold", color=DARK_GREEN)
    for b, v in zip(bars, series.values):
        ax.text(b.get_x() + b.get_width() / 2, v + (ylim * 0.02), f"{v}%",
                ha="center", fontweight="bold", color=DARK_GREEN)
    ax.set_ylim(0, ylim)
    ax.spines[["top", "right"]].set_visible(False)


# ---- CHART 1: No-Show Rate by Lead Time ----
ax1 = fig.add_subplot(gs[2, 0])
add_bar_chart(ax1, lead_time_rate, "No-Show Rate by Booking Lead Time",
              [GREEN, GOLD, DARK_GREEN], 60)

# ---- CHART 2: No-Show Rate by Prior History ----
ax2 = fig.add_subplot(gs[2, 1])
add_bar_chart(ax2, prior_rate, "No-Show Rate by Prior No-Show History",
              [GREEN, GOLD, ORANGE, DARK_GREEN], 80)

# ---- CHART 3: Reminder Effect ----
ax3 = fig.add_subplot(gs[3, 0])
reminder_plot = reminder_rate.rename(index={"Yes": "Reminder Sent", "No": "No Reminder"})
# Reorder so "Reminder Sent" appears first, matching the reference layout
reminder_plot = reminder_plot.reindex(["Reminder Sent", "No Reminder"])
add_bar_chart(ax3, reminder_plot, "Reminder Effect on No-Shows", [GREEN, DARK_GREEN], 60)

# ---- CHART 4: Overall Appointment Outcomes (pie) ----
ax4 = fig.add_subplot(gs[3, 1])
outcome_counts = df["appointment_outcome"].value_counts(normalize=True) * 100
colors_map = {"No-Show": DARK_GREEN, "Attended": GREEN, "Cancelled": GREY}
pie_colors = [colors_map.get(label, GREY) for label in outcome_counts.index]
ax4.pie(outcome_counts.values, labels=outcome_counts.index,
        autopct="%1.1f%%", colors=pie_colors, startangle=90,
        textprops={"fontweight": "bold"})
ax4.set_title("Overall Appointment Outcomes", fontweight="bold", color=DARK_GREEN)

plt.savefig("HealthConnect_Week5_Dashboard.png", dpi=200, bbox_inches="tight", facecolor="white")
plt.show()
print("\nDashboard saved as HealthConnect_Week5_Dashboard.png")
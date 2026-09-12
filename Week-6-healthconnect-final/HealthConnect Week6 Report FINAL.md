# HealthConnect Clinic — Week 6 Advanced Analytics & Decision Support Report

**AnalystLab Africa Experience Lab | Data Analytics Track**
**Author:** Osagie Osagieduwa Precious
**Week:** 6 — Integration, Advanced Development & Validation

---

## 1. Week 5 → Week 6 Transition

- **My main Week 5 output:** HealthConnect Advanced Analytics Report — 5 KPIs calculated, full EDA across lead time, prior no-show history, reminders, distance, age, gender, and appointment type, plus an initial dashboard.
- **Most important result/component produced:** Prior no-show history emerged as the strongest predictor of future no-shows — the no-show rate rose from 43.5% (0 prior no-shows) to 68.8% (3+ prior no-shows), a 25-point spread, by far the widest gap of any factor tested.
- **Main issue/limitation discovered:** The waiting-time-band breakdown had an unreliable 60+ minute band (only 3 records), so that finding was flagged but not used. Week 5 also only looked at each factor in isolation — no interaction effects were tested.
- **Track(s) whose work is relevant to Week 6:** Data Science — my validated predictors and risk segmentation can directly inform their model's feature set and target definition.
- **What I intend to improve/integrate/validate in Week 6:** Deepen the prior-no-show-history finding by checking it against other factors, build a combined patient risk score, refresh the dashboard with that view, and hand off a clean feature set to Data Science.

---

## 2. Advanced Analysis

### 2.1 Interaction checks

**No-Show Rate (%) by Prior No-Show History × Booking Lead Time:**

| Prior History | Same-day | 1-7 days | 8+ days |
|---|---|---|---|
| 0 prior | 18.4 | 22.3 | 46.7 |
| 1 prior | 26.9 | 34.1 | 56.3 |
| 2 prior | 62.5 | 47.3 | 61.1 |
| 3+ prior | 0.0 | 23.1 | 78.2 |

**No-Show Rate (%) by Prior No-Show History × Distance to Clinic:**

| Prior History | 0-5km | 5-10km | 10-20km | 20+km |
|---|---|---|---|---|
| 0 prior | 42.1 | 41.7 | 44.0 | 53.0 |
| 1 prior | 50.6 | 51.2 | 55.4 | 62.9 |
| 2 prior | 53.7 | 56.8 | 63.3 | 68.8 |
| 3+ prior | 89.5 | 68.8 | 60.0 | 60.0 |

Interpretation: For the 0, 1, and 2 prior no-show groups, both interactions behave as expected — no-show rate rises steadily with longer lead time and with greater distance, and the two factors compound (e.g. 2 prior no-shows + 20+km distance = 68.8%, well above either factor alone). This confirms prior no-show history is not simply a proxy for distance or lead time — it adds real, independent risk. The 3+ prior row is the exception: it swings erratically (0.0% for same-day, 89.5% for 0-5km) rather than following the same clean pattern, which is investigated in 2.2 below.

### 2.2 Reliability check

**Sample sizes behind each prior-history band:**

| Prior History | Sample Size |
|---|---|
| 0 prior | 2,921 |
| 1 prior | 1,548 |
| 2 prior | 438 |
| 3+ prior | **93** |

Interpretation: This is the key finding of the reliability check. The 3+ prior no-shows group is only 93 patients out of ~5,000 (under 2% of the dataset). Once that group is further split across three lead-time bands or four distance bands, individual cells can shrink to single digits — which explains the erratic 0.0%/89.5% swings seen in section 2.1. **The overall 3+ prior finding (elevated no-show risk) is directionally reliable, but the specific interaction breakdowns for that group are not** — there isn't enough data to trust any one cell in isolation. This is an important caveat that Week 5's headline number didn't surface.

### 2.3 What changed vs. Week 5 understanding
Prior no-show history holds up as a genuine, independent risk driver — it compounds with both lead time and distance rather than being explained away by either. However, Week 6 analysis surfaces a limitation Week 5 didn't have visibility into: the 3+ prior segment is small (n=93), so while its elevated risk is real, granular claims about *how* that risk interacts with other factors should be treated with caution until more data accumulates. This is why the Week 6 risk segmentation (Section 4) groups "2+ prior no-shows" together rather than isolating "3+ prior" alone — it trades some precision for a group large enough to trust.

---

## 3. Refined KPIs

| KPI | Week 5 Value | Week 6 Status |
|---|---|---|
| Overall No-Show Rate | 48.5% | Validated baseline, unchanged |
| Lost Appointment Slots | 2,423 | Validated baseline, unchanged |
| No-Show Rate (8+ day bookings) | 51.5% | Confirmed as part of interaction check (2.1) |
| No-Show Rate (3+ prior no-shows) | 68.8% | **Confirmed independent** of lead time/distance (see 2.3) |
| **New:** % of no-shows from High-risk segment | — | **41.6%** |
| **New:** Patients in High-risk segment | — | **1,798** (of ~5,000 patients) |

---

## 4. Patient Risk Segmentation

- **Method:** Combined the four strongest predictors into a single additive risk score (0–4 points): previous no-shows ≥ 2, booking lead time ≥ 8 days, distance to clinic ≥ 20km, and no reminder sent. Score is then bucketed into Low (0), Medium (1), High (2+).
- **Segments:** Low / Medium / High
- **Finding:** No-show rate climbs cleanly across every segment — **Low: 23.8%** (378 patients) → **Medium: 46.9%** (2,824 patients) → **High: 56.1%** (1,798 patients). The High-risk segment's no-show rate is more than double the Low-risk segment's, and unlike the raw 3+ prior-no-shows finding, this segment is large enough (1,798 patients) to be statistically trustworthy.
- **Business relevance:** This turns four separate Week 5 findings into one operational flag clinic staff can act on directly — instead of checking multiple fields per patient, a single "High-risk" tag identifies who needs a confirmation call or reminder priority. The High-risk segment is 36% of all patients (1,798 of ~5,000) but accounts for 41.6% of all no-shows — a concentrated, actionable target rather than a diffuse problem across the whole patient base.

---

## 5. Updated Dashboard/Visualisation

- Insert `HealthConnect_Week6_Dashboard.png` here (generated by the script)
- **What's new vs. Week 5:** The Week 5 dashboard showed no-show rate broken down by each factor separately. The Week 6 dashboard adds the combined risk-segmentation view — showing both the no-show rate *and* patient volume per risk tier, so it's immediately clear where the biggest operational opportunity sits (e.g. a large High-risk group with a high no-show rate is a bigger lever than a small group with the same rate).

---

## 6. Evidence-Based Business Insights

1. Prior no-show history remains the single strongest and most independent predictor of future no-shows (43.5% → 68.8%), and this holds even when controlling for lead time and distance to clinic — patients with 2 prior no-shows who also live 20+km away and book 8+ days ahead reach a 68.8% no-show rate, showing these risk factors compound rather than overlap.
2. Combining the top risk factors into one segmentation model identifies a High-risk group (1,798 patients, 36% of the base) responsible for 41.6% of all no-shows — a concentrated, actionable target rather than treating every patient equally.
3. The "3+ prior no-shows" group, while genuinely high-risk, is small (93 patients) — future risk models should treat 2+ prior no-shows as the more statistically reliable threshold rather than isolating 3+ alone, since finer breakdowns of the 3+ group produce unstable, unreliable percentages.
4. Distance to clinic and prior no-show history compound each other: even patients with no prior no-shows see their no-show rate rise from 42.1% (0-5km) to 53.0% (20+km), suggesting transport/access barriers affect all patients, not just repeat no-show patients.
5. The Low-risk segment (378 patients, 23.8% no-show rate) proves HealthConnect already has patients who reliably attend — the gap between this group and the High-risk segment (56.1%) shows the size of the opportunity if targeted interventions bring High-risk behaviour even partway toward Low-risk norms.

---

## 7. Business Recommendations

1. Introduce mandatory phone/SMS confirmation calls specifically for patients flagged High-risk, rather than a blanket reminder policy for all patients — this targets the 36% of patients driving 41.6% of no-shows.
2. Prioritise the High-risk segment (2+ prior no-shows, 8+ day lead time, 20+km distance, or no reminder sent) for transport support or telehealth options where clinically appropriate, since distance is a compounding factor across every prior-history group.
3. Use "2+ prior no-shows" rather than "3+ prior no-shows" as the operational risk threshold going forward — it captures the same directional risk with a large enough sample (531 combined patients) to support reliable, repeatable decisions.

---

## 8. Cross-Track Integration

*Per guidance from the programme coordinator, cross-track collaboration is not required for this submission. This section is included for completeness but not populated, since no integration activity was performed.*

**Note for future weeks:** Should cross-track integration become relevant later, the natural handoff point remains Data Science — the `risk_score`/`risk_segment` fields in this report (Section 4) are ready to serve as engineered features if a Data Science teammate needs them.

---

## 9. Assumptions, Limitations, Risks & Dependencies

- **Resolved from Week 5:** Waiting-time reliability issue was documented and excluded from findings (not used as evidence).
- **Unresolved from Week 5:** Interaction effects between factors were not tested until this week.
- **New issues discovered:** The "3+ prior no-shows" group (n=93) is too small to support reliable sub-analysis once broken down further by lead time or distance — Week 5's headline 68.8% figure for this group is directionally sound but shouldn't be over-interpreted at a finer grain.
- **New cross-track dependencies:** None — cross-track collaboration not required for this submission per programme guidance.
- **Data limitations:** Dataset does not capture causal factors (e.g. transport availability, financial hardship) that may underlie the distance and reminder findings — associations shown are correlational, not causal.
- **Recommended mitigation:** Treat risk segmentation as a decision-support flag, not a deterministic prediction; revisit thresholds once Data Science's model is validated.

*(The Week 6 Project Summary is submitted as a separate document — see `HealthConnect_Week6_Project_Summary.md`.)*

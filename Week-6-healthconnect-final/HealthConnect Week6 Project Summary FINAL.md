# HealthConnect Clinic — Week 6 Project Summary

**AnalystLab Africa Experience Lab | Data Analytics Track**
**Author:** Osagie Osagieduwa Precious
**Week:** 6

*This summary complements the main Week 6 Advanced Analytics & Decision Support Report — it does not repeat it.*

---

**1. What I planned to accomplish**
Deepen and validate the strongest Week 5 finding (prior no-show history), build a combined patient risk segmentation, and refresh the dashboard with that view.

**2. What I completed**
Ran interaction checks on prior no-show history against booking lead time and distance to clinic, confirmed the reliability of the finding via sample-size review, built a four-factor patient risk score (Low/Medium/High), and updated the dashboard to show the risk segmentation.

**3. What I improved from Week 5**
Week 5 looked at each predictor in isolation. Week 6 tested whether prior no-show history holds up when checked against other factors, and combined multiple predictors into one actionable risk score instead of several separate findings. Week 6 also surfaced a reliability limitation Week 5 didn't catch — the "3+ prior no-shows" group is small (93 patients), so the headline 68.8% figure is directionally sound but shouldn't be over-interpreted at a finer grain.

**4. What I integrated**
Not applicable this week — cross-track collaboration was confirmed as not required for this submission.

**5. Which track(s) I collaborated with**
None — not required for this submission per programme guidance.

**6. What was exchanged**
Not applicable.

**7. What changed as a result**
Not applicable.

**8. Key findings or development outcomes**
Prior no-show history is confirmed as an independent predictor of no-shows, not explained away by lead time or distance to clinic — the two factors compound rather than overlap (e.g. 2 prior no-shows + 20+km distance = 68.8% no-show rate). The combined risk segmentation shows 41.6% of all no-shows are concentrated in the High-risk group (1,798 of ~5,000 patients), giving HealthConnect a targeted, statistically reliable intervention point.

**9. Major challenges**
Balancing depth of analysis (interaction checks, reliability review) against the instruction not to repeat the full Week 5 EDA — had to be selective about which findings warranted deeper investigation. Also identifying that the 3+ prior no-shows group was too small for granular sub-analysis, which required stepping back from the original Week 5 framing rather than just extending it.

**10. Important decisions**
Chose an additive risk score (rather than a weighted/statistical model) for interpretability, since the Week 6 goal was decision support, not a production ML model. Also decided to recommend "2+ prior no-shows" as the operational risk threshold going forward instead of "3+ prior no-shows," since the larger combined sample size makes it more statistically trustworthy for real decisions.

**11. Remaining issues**
Risk score thresholds are provisional and were chosen for interpretability rather than statistically optimised — worth revisiting if any future track builds a more formal predictive model.

**12. My contribution to the overall HealthConnect project**
Provided the analytical foundation HealthConnect needs to prioritise intervention — moving from "many patients no-show" to "which specific patients are highest-risk and why" — while also flagging a data-reliability limitation in the original Week 5 finding before it could mislead later decisions.

**13. Proposed focus for Week 7**
Test the risk segmentation against a holdout period of appointment data to see if the Low/Medium/High no-show rates hold consistent over time, and refine the risk score thresholds based on that validation.

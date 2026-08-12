# Phase 6 — Model Interpretation & Explainability

## 1. Objective

Phase 6 focused on understanding how the final FactoryGuard AI model behaves, identifying important features, analyzing individual predictions, investigating errors, and translating model results into practical business interpretations.

---

## 2. Final Model

**Model:** Random Forest Classifier

**Decision Threshold:** 0.50

**Minority Class:** Class 0

**Majority Class:** Class 1

**Training Records:** 8000

**Test Records:** 2000

---

## 3. Final Model Performance

| Metric | Value |
|---|---:|
| Accuracy | 85.35% |
| Minority Precision | 39.82% |
| Minority Recall | 35.48% |
| Minority F1-score | 37.53% |
| ROC-AUC | 70.09% |
| PR-AUC | 42.44% |
| False Positive Rate | 7.59% |
| False Negative Rate | 64.52% |

---

## 4. Prediction Error Analysis

| Prediction Type | Count |
|---|---:|
| True Positive | 88 |
| True Negative | 1619 |
| False Positive | 133 |
| False Negative | 160 |

The minority-class error analysis shows that the model correctly detects 88 of the 248 actual minority-class observations and misses 160.

The high False Negative Rate is therefore the primary limitation of the final model.

---

## 5. Top Important Features

1. numerical__cost_usd (importance = 0.1493)
2. numerical__defect_severity_0to3 (importance = 0.1078)
3. numerical__energy_kwh (importance = 0.0733)
4. numerical__total_cycle_time_min (importance = 0.0729)
5. categorical__defect_type_none (importance = 0.0610)
6. numerical__machine_age_yrs (importance = 0.0528)
7. numerical__process_speed_units_hr (importance = 0.0408)
8. numerical__humidity_pct (importance = 0.0397)
9. numerical__temp_c (importance = 0.0382)
10. numerical__event_hour (importance = 0.0289)

These features are identified as important by the Random Forest feature-importance analysis.

Feature importance should be interpreted as a measure of predictive contribution within the trained model rather than as evidence of causation.

---

## 6. Individual Prediction Analysis

Representative True Positive, True Negative, False Positive, and False Negative observations were examined.

The analysis showed that predictions close to the 0.50 threshold can be difficult to classify.

The representative False Negative case had a minority-class probability just below the threshold, demonstrating how the decision threshold affects final classification.

---

## 7. Error Analysis

True Positive cases generally received higher minority-class probabilities than False Negative cases.

The comparison between True Positives and False Negatives showed noticeable differences in several important processed features, including:

- Cost
- Defect severity
- Total cycle time
- Energy consumption
- Defect-type related features

These differences describe patterns associated with successful and unsuccessful predictions but do not establish causal relationships.

---

## 8. Business Interpretation

FactoryGuard AI can be used as a screening and decision-support system for identifying potentially problematic manufacturing cases.

A predicted minority-class case can be flagged for further investigation.

The system should not be treated as a fully automated quality-control replacement because a substantial proportion of minority-class cases are still missed.

---

## 9. Model Limitations

The main limitations identified during Phase 6 are:

1. Minority-class recall is only 35.48%.
2. The False Negative Rate is 64.52%.
3. The dataset contains an imbalanced target distribution.
4. Model performance depends on the quality and representativeness of the available data.
5. Processed feature values may not directly correspond to original business units.
6. Feature importance does not establish causality.
7. Future manufacturing conditions may differ from the training distribution.

---

## 10. Recommended Future Improvements

Potential improvements include:

- Collecting more representative minority-class observations.
- Evaluating additional class-imbalance handling methods.
- Optimizing the decision threshold according to real business costs.
- Evaluating additional classification models.
- Improving local prediction explanations where necessary.
- Monitoring model performance and data distribution after deployment.

---

## 11. Final Conclusion

Phase 6 established that FactoryGuard AI provides meaningful predictive capability and that its predictions can be interpreted at both global and individual levels.

The analysis also identified an important limitation: the model misses a substantial proportion of minority-class cases.

Therefore, the appropriate positioning of FactoryGuard AI is:

**Manufacturing Data → Prediction → Risk Flag → Human Investigation → Decision**

rather than fully automated decision-making.

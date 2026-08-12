# FactoryGuard AI — Business Interpretation & Model Limitations

## Final Model

- Model: Random Forest Classifier
- Decision Threshold: 0.50
- Training Records: 8,000
- Test Records: 2,000

## Final Test Performance

- Accuracy: 85.35%
- Minority Precision: 39.82%
- Minority Recall: 35.48%
- Minority F1-score: 37.53%
- ROC-AUC: 70.09%
- PR-AUC: 42.44%
- False Positive Rate: 7.59%
- False Negative Rate: 64.52%

## Business Interpretation

FactoryGuard AI is designed as a decision-support system for identifying potentially problematic manufacturing outcomes.

The model demonstrates meaningful predictive capability, with a ROC-AUC of approximately 0.70 and an overall accuracy of approximately 85%.

However, minority-class recall is only 35.48%. This means that a substantial proportion of minority-class cases are not detected.

Therefore, the model should be used as a screening and decision-support tool rather than as a fully automated quality-control system.

## False Positive

A False Positive occurs when a majority-class case is incorrectly flagged as a minority-class case.

Business implication:

The case may receive unnecessary investigation or additional quality-control attention.

## False Negative

A False Negative occurs when an actual minority-class case is incorrectly classified as the majority class.

Business implication:

A potentially problematic case may be missed by the system.

Because False Negatives are more important for the project's detection objective, they should receive particular attention when evaluating future model improvements.

## Model Strengths

- Meaningful class-separation capability.
- Good overall accuracy.
- Relatively low false-positive rate.
- Ability to capture nonlinear relationships in structured manufacturing data.
- Global feature importance provides model interpretability.

## Model Limitations

- Minority-class recall is limited.
- False-negative rate is high.
- The target variable is imbalanced.
- Model performance depends on the quality and representativeness of the training data.
- Real-world manufacturing conditions may differ from the training data.
- Predictions depend on the features available during inference.
- Feature relationships should not be interpreted as causal relationships.

## Recommended Operational Role

FactoryGuard AI should operate as:

Manufacturing Data
→ Preprocessing
→ Random Forest Prediction
→ Minority-Class Probability
→ Threshold-Based Flag
→ Human Review
→ Appropriate Manufacturing Action

The model should support human decision-making rather than replace human quality-control judgment.

## Potential Future Improvements

- Collect more representative minority-class data.
- Evaluate additional imbalance-handling strategies.
- Optimize the threshold according to business costs.
- Evaluate additional classification models.
- Improve local prediction explanations.
- Monitor model performance and data drift after deployment.

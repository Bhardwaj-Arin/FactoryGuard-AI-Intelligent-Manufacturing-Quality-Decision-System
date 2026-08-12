
# Phase 5 — Model Development & Evaluation

## 1. Objective

The objective of Phase 5 was to build, evaluate, compare, tune, and select a classification model for FactoryGuard AI.

The project uses a binary target:

- Majority class: 1
- Minority class: 0
- Minority-class proportion: approximately 12.39%

Because of the class imbalance, model selection focused primarily on minority-class detection rather than accuracy alone.

---

## 2. Modeling Workflow

The Phase 5 workflow was:

1. Modeling setup
2. Baseline classification
3. Initial model training
4. Initial model evaluation
5. Class-imbalance analysis
6. Confusion-matrix analysis
7. Model comparison
8. Cross-validation
9. Hyperparameter tuning using RandomizedSearchCV
10. Tuned model evaluation
11. Final model selection and training
12. Decision-threshold optimization
13. Final test-set validation and inference
14. Phase 5 documentation

---

## 3. Candidate Models

Two tree-based ensemble models were evaluated:

- Random Forest
- XGBoost

These models were selected because they are suitable for tabular manufacturing data and can capture nonlinear relationships between manufacturing features and the target variable.

---

## 4. Cross-Validation and Hyperparameter Tuning

Five-fold stratified cross-validation was used to evaluate model stability.

RandomizedSearchCV was used to search for improved hyperparameters for Random Forest and XGBoost.

### Best Cross-Validated Minority F1

| Model | CV Minority F1 |
|---|---:|
| Random Forest | 0.3827 |
| XGBoost | 0.3551 |

Random Forest achieved the stronger cross-validated minority-class F1-score.

---

## 5. Tuned Model Test Performance

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Random Forest | 0.8535 | 0.3982 | 0.3548 | 0.3753 | 0.7009 | 0.4244 |
| XGBoost | 0.8970 | 0.7917 | 0.2298 | 0.3562 | 0.6839 | 0.4186 |

### Interpretation

XGBoost achieved higher overall accuracy and precision.

However, Random Forest achieved:

- Higher minority-class recall
- Higher minority-class F1-score
- Higher ROC-AUC
- Higher PR-AUC

Because FactoryGuard AI places importance on detecting minority-class observations, Random Forest provided the better overall balance.

---

## 6. Final Model Selection

The final model selected was:

**Random Forest Classifier**

### Final Hyperparameters

- `n_estimators = 188`
- `max_depth = 12`
- `max_features = sqrt`
- `min_samples_split = 5`
- `min_samples_leaf = 2`
- `class_weight = balanced`

The final model was saved as:

`models/final_factoryguard_model.pkl`

---

## 7. Threshold Optimization

The default threshold of 0.50 was compared with alternative thresholds using five-fold cross-validated training predictions.

The best candidate threshold was:

**0.55**

Cross-validation results:

| Threshold | F1 |
|---|---:|
| 0.50 | 0.3827 |
| 0.55 | 0.3858 |

The improvement was small.

When evaluated on the held-out test set:

| Metric | Threshold 0.50 | Threshold 0.55 |
|---|---:|---:|
| Accuracy | 0.8535 | 0.8735 |
| Minority Precision | 0.3982 | 0.4841 |
| Minority Recall | 0.3548 | 0.3065 |
| Minority F1 | 0.3753 | 0.3753 |
| False Positive Rate | 0.0759 | 0.0462 |
| False Negative Rate | 0.6452 | 0.6935 |

The optimized threshold did not improve test-set F1-score.

Since the project prioritizes minority-class detection and threshold 0.50 provides higher recall with the same test-set F1-score, the default threshold of **0.50** is retained as the final operating threshold.

---

## 8. Final Model Performance

### Final Operating Configuration

- Model: Random Forest
- Decision threshold: 0.50

### Final Test Metrics

- Accuracy: 0.8535
- Minority Precision: 0.3982
- Minority Recall: 0.3548
- Minority F1-score: 0.3753
- ROC-AUC: 0.7009
- PR-AUC: 0.4244
- False Positive Rate: 0.0759
- False Negative Rate: 0.6452

---

## 9. Interpretation

The model demonstrates useful predictive capability, particularly in distinguishing the two classes, as indicated by the ROC-AUC of approximately 0.70.

However, minority-class recall remains limited.

A recall of approximately 35.48% means that the model identifies only a portion of the minority-class observations.

Therefore, FactoryGuard AI should be considered a decision-support system rather than a perfect automated quality-control mechanism.

---

## 10. Important Limitation

The model still produces a relatively high false-negative rate.

This means some minority-class manufacturing observations may not be detected.

Future improvements may include:

- Additional manufacturing features
- More representative training data
- Improved class-imbalance strategies
- Decision-threshold optimization based on operational costs
- Alternative ensemble models
- Cost-sensitive learning
- Additional model validation

These improvements can be explored in future project phases.

---

## 11. Final Inference Pipeline

The final FactoryGuard AI prediction pipeline is:

Manufacturing Input
↓
Preprocessing Pipeline
↓
Processed Features
↓
Final Random Forest
↓
Minority-Class Probability
↓
Decision Threshold = 0.50
↓
Final Classification

---

## 12. Phase 5 Conclusion

Phase 5 successfully transformed the engineered manufacturing dataset into a trained and evaluated machine-learning solution.

Random Forest was selected as the final model based on its stronger minority-class performance across cross-validation and test evaluation.

The final model and supporting artifacts have been saved for use in the deployment stage.

Phase 5 is therefore complete.

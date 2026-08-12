## Final EDA Observations

The Exploratory Data Analysis established that the Manufacturing Quality Decisions dataset is suitable for developing FactoryGuard AI as a binary classification system for manufacturing quality prediction.

### Major Findings

1. **Target Imbalance**

   The `final_pass` target contains approximately 87.61% majority-class observations and 12.39% minority-class observations.

   This means model evaluation must consider metrics beyond accuracy, including precision, recall, F1-score, ROC-AUC, and the confusion matrix.

2. **Operational Variation**

   Manufacturing outcomes vary across plants, production lines, shifts, material grades, and other operational conditions.

3. **Strong Feature Relationships**

   Several numerical features are strongly correlated, particularly:

   - `rework_time_min` ↔ `total_cycle_time_min` = 0.92
   - `total_cycle_time_min` ↔ `energy_kwh` = 0.90

   These relationships will be investigated during Feature Engineering.

4. **Outliers and Skewness**

   Several continuous variables contain potential extreme observations and skewed distributions.

   These will be investigated rather than automatically removed or transformed.

5. **Potential Target Leakage**

   Features such as:

   - `decision_rework`
   - `rework_time_min`
   - `defect_severity_0to3`
   - `scrap`
   - `warranty_claim_90d`

   require a prediction-time availability assessment before they are included in the final model.

6. **Feature Engineering Requirements**

   The next phase will focus on:

   - Feature availability and leakage assessment
   - Identifier evaluation
   - Feature selection
   - Categorical encoding
   - Numerical preprocessing
   - Outlier treatment
   - Skewness treatment where appropriate
   - Meaningful feature creation
   - Class imbalance strategy
   - Creation of the final ML-ready dataset

## Final EDA Conclusion

EDA has transformed the raw dataset from a collection of manufacturing records into a structured understanding of the problem.

The analysis identified the major data-quality, statistical, operational, and modeling considerations that must be addressed before model development.

The project can now proceed to:

**Phase 4 — Feature Engineering**
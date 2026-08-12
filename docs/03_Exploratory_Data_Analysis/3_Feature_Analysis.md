## Feature Analysis — Key Observations

### Target Variable

The target variable `final_pass` is imbalanced:

- Majority class: 87.61%
- Minority class: 12.39%
- Majority/Minority ratio: approximately 7.07:1

Therefore, accuracy alone should not be used to evaluate the final classification model.

### Numerical Features

The numerical features show different ranges, distributions, and levels of variability.

Several variables, including `cost_usd`, `total_cycle_time_min`, and `energy_kwh`, contain potential extreme observations that require investigation rather than automatic removal.

### Categorical Features

Variables such as:

- `plant`
- `line`
- `shift`
- `material_grade`
- `inspection_method`

show different distributions across the manufacturing records and may contain useful predictive information.

### Bivariate and Multivariate Analysis

Quality outcomes vary across different operational groups and combinations of manufacturing conditions.

The Plant + Shift and Material Grade + Shift analyses indicate that combinations of operational factors may reveal patterns that are not visible when features are analyzed independently.

### Correlation

Several strong relationships were identified:

- `rework_time_min` and `total_cycle_time_min` → **0.92**
- `total_cycle_time_min` and `energy_kwh` → **0.90**
- `scrap` and `cost_usd` → **0.85**
- `defect_severity_0to3` and `rework_time_min` → **0.84**

These relationships indicate potential feature redundancy and will be investigated during Feature Engineering.

### Outliers

The IQR analysis identified potential extreme observations in several variables.

However, binary and zero-inflated variables such as `final_pass`, `decision_rework`, and `scrap` should not be interpreted as conventional continuous-feature outliers.

Outliers in continuous manufacturing variables will therefore be investigated based on their business meaning before deciding on treatment.

### Feature Distribution

Several features show noticeable skewness.

The most skewed feature was:

`warranty_claim_90d` → skewness approximately **8.78**

However, high skewness in binary or zero-inflated variables does not automatically justify a mathematical transformation.

Continuous numerical features will be evaluated separately during Feature Engineering.

### Feature Analysis Conclusion

The EDA indicates that multiple manufacturing and operational variables may contribute useful predictive information. However, feature selection must consider not only statistical relationships but also business meaning, prediction-time availability, redundancy, and target leakage.
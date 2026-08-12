## Key Observations from EDA

The Exploratory Data Analysis provided an overall understanding of the Manufacturing Quality Decisions dataset and established the foundation for Feature Engineering.

The main observations were:

- The dataset contains approximately 10,000 manufacturing records representing different production and operational conditions.
- The target variable is `final_pass`, which represents the final quality outcome.
- The target is imbalanced, with approximately 87.61% majority-class observations and 12.39% minority-class observations.
- The dataset contains numerical, categorical, operational, and quality-related variables that require different preprocessing strategies.
- Several manufacturing variables show noticeable variation, skewness, and potential extreme observations.
- Differences in quality outcomes were observed across operational groups such as plant, line, shift, and material grade.
- Several numerical variables show strong relationships with each other, indicating possible overlapping information.
- Some variables require further investigation for target leakage because they may represent information generated after or around the final quality decision.

### Overall EDA Conclusion

The dataset contains sufficient variation and operational information for developing a classification-based manufacturing quality prediction system. However, target imbalance, feature redundancy, outliers, skewness, and prediction-time feature availability must be carefully addressed before model development.
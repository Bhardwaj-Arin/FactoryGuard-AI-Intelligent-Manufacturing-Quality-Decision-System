# Dataset Profile

## Overview

Before performing preprocessing and exploratory data analysis, it is essential to understand the structure, characteristics, and composition of the dataset. A detailed dataset profile provides an overview of the available features, their data types, business significance, and overall quality.

The **Manufacturing Quality Decisions** dataset contains production, machine, operator, inspection, environmental, quality, and cost-related information collected from manufacturing operations. Each record represents a single manufacturing event and captures multiple factors that may influence production quality and operational decisions.

---

# Dataset Summary

| Attribute | Value |
|-----------|-------|
| **Dataset Name** | Manufacturing Quality Decisions |
| **Domain** | Manufacturing & Quality Management |
| **Problem Type** | Supervised Machine Learning |
| **Number of Records** | 10,000 |
| **Number of Features** | 23 |
| **Missing Values** | None |
| **Duplicate Records** | None |

---

# Dataset Composition

The dataset consists of multiple feature categories representing different stages of the manufacturing process.

| Feature Type | Count |
|--------------|------:|
| Identifier Features | 1 |
| Datetime Features | 1 |
| Categorical Features | 8 |
| Numerical Features | 13 |
| **Total Features** | **23** |

---

# Feature Categories

## Identifier Feature

| Feature | Description |
|---------|-------------|
| **event_id** | Unique identifier assigned to each manufacturing event. Used for record tracking and traceability rather than model training. |

---

## Datetime Feature

| Feature | Description |
|---------|-------------|
| **event_ts** | Timestamp indicating when the manufacturing event occurred. This feature can be used to derive additional temporal information during preprocessing. |

---

## Categorical Features

These variables describe different operational characteristics of the manufacturing environment.

| Feature | Description |
|---------|-------------|
| **plant** | Manufacturing plant where production occurred. |
| **line** | Production line responsible for manufacturing. |
| **shift** | Working shift during production. |
| **machine_id** | Machine used during manufacturing. |
| **operator_id** | Operator responsible for production. |
| **material_grade** | Grade of raw material used. |
| **inspection_method** | Inspection technique applied for quality assessment. |
| **defect_type** | Category of defect identified during inspection. |

---

## Numerical Features

These variables represent measurable production, environmental, operational, and cost-related information.

| Feature | Description |
|---------|-------------|
| **machine_age_yrs** | Age of the production machine in years. |
| **temp_c** | Operating temperature during manufacturing. |
| **humidity_pct** | Relative humidity during production. |
| **process_speed_units_hr** | Production speed measured in units per hour. |
| **defect_severity_0to3** | Severity level assigned to detected defects. |
| **decision_rework** | Indicates whether rework was required. |
| **rework_time_min** | Time spent performing rework. |
| **final_pass** | Indicates whether the product passed final quality inspection. |
| **scrap** | Indicates whether the product was scrapped. |
| **total_cycle_time_min** | Total production cycle time. |
| **energy_kwh** | Energy consumed during production. |
| **cost_usd** | Manufacturing cost of the product. |
| **warranty_claim_90d** | Indicates whether a warranty claim occurred within 90 days. |

---

# Quality Outcome Variables

Unlike many traditional machine learning datasets, this dataset contains multiple manufacturing quality outcome variables.

These include:

- Final inspection result
- Rework decision
- Scrap status
- Warranty claim information
- Defect severity

This provides flexibility for developing different predictive models depending on the selected business objective.

For the FactoryGuard AI project, the primary prediction target will be selected during the preprocessing phase after evaluating the business requirements and suitability of each outcome variable.

---

# Initial Data Characteristics

The initial exploration of the dataset revealed the following observations:

- The dataset contains **10,000 manufacturing records**.
- No missing values were identified.
- No duplicate records were found.
- Both categorical and numerical variables are available.
- Manufacturing events are distributed across multiple plants, production lines, and work shifts.
- The dataset includes production, quality, inspection, machine, operator, environmental, and cost-related information.
- Data is well structured and suitable for machine learning.

---

# Business Perspective

The richness of this dataset makes it possible to analyze manufacturing operations from multiple perspectives rather than focusing on a single prediction problem.

Using this information, FactoryGuard AI can help manufacturing organizations:

- Monitor production quality.
- Analyze machine performance.
- Evaluate inspection effectiveness.
- Understand operator-related trends.
- Identify production bottlenecks.
- Support quality-related business decisions.
- Build predictive models for manufacturing outcomes.

---

# Summary

The Manufacturing Quality Decisions dataset provides a comprehensive representation of modern manufacturing operations by combining production, operational, quality, inspection, and business-related information within a single dataset.

Its balanced combination of identifier, datetime, categorical, and numerical variables makes it well suited for exploratory data analysis, feature engineering, predictive modeling, and business intelligence applications. This strong data foundation supports the overall objective of FactoryGuard AI as an intelligent manufacturing quality decision system.
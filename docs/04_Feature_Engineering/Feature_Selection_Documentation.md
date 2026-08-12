
---

# 3. `Feature_Selection_Documentation.md`

```markdown
# Feature Selection Documentation

## Purpose

The objective of feature selection is to identify the most useful and reliable predictors while removing features that are irrelevant, redundant, or affected by target leakage.

---

## Selection Criteria

Features were evaluated using:

- Prediction-time availability
- Business relevance
- Correlation
- Redundancy
- Variance
- Feature usefulness
- Model-based importance

---

## Identifier Features

The following identifiers were evaluated:

- `event_id`
- `machine_id`
- `operator_id`

`event_id` was treated as a record identifier and excluded from the candidate ML features.

`machine_id` and `operator_id` require business and model-based evaluation before final inclusion.

---

## Highly Correlated Features

EDA identified:

```text
rework_time_min ↔ total_cycle_time_min = 0.92
total_cycle_time_min ↔ energy_kwh = 0.90
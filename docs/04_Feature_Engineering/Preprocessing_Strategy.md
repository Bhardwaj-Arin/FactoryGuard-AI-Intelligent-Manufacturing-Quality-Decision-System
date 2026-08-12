
---

# 4. `Preprocessing_Strategy.md`

```markdown
# Preprocessing Strategy

## Purpose

The preprocessing strategy prepares the final feature set for machine learning while ensuring that the same transformations are consistently applied to training, testing, and future prediction data.

---

## Preprocessing Workflow

```text
Input Features
      ↓
Separate Numerical / Categorical Features
      ↓
Numerical Pipeline
      ↓
Categorical Pipeline
      ↓
Combine Using ColumnTransformer
      ↓
ML-Ready Features
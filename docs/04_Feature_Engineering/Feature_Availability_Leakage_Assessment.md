# Feature Availability & Leakage Assessment

## Purpose

The objective of this assessment is to determine whether each feature would realistically be available when FactoryGuard AI makes the `final_pass` prediction.

Features generated after the prediction point can introduce target leakage and must not be used as model inputs.

---

## Prediction Point

FactoryGuard AI is designed to predict the final quality outcome using information available during or immediately after the manufacturing process and before post-decision outcomes.

Conceptual workflow:

```text
Manufacturing Process
        ↓
Process Information Available
        ↓
FactoryGuard Prediction
        ↓
Quality Decision
        ↓
Rework / Scrap
        ↓
Shipment
        ↓
Warranty Outcome
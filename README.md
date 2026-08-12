# 🏭 FactoryGuard AI — Intelligent Manufacturing Quality Decision System

An end-to-end machine learning decision-support system that screens manufacturing and process data to flag potentially problematic production units before they move further down the line.

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?logo=streamlit&logoColor=white)](https://factoryguard-ai-intelligent-manufacturing-quality-decision-sys.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-RandomForest-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)

**🚀 Live App:** https://factoryguard-ai-intelligent-manufacturing-quality-decision-sys.streamlit.app/
**📦 Repository:** https://github.com/Bhardwaj-Arin/FactoryGuard-AI-Intelligent-Manufacturing-Quality-Decision-System

---

## 📌 Overview

FactoryGuard AI takes structured manufacturing observations — plant, machine, material, environmental readings, process metrics, inspection results, and cost/energy data — and predicts whether a unit is likely to **pass final quality control** or is **potentially problematic**, along with a probability score.

It is built and positioned as a **screening / decision-support tool**, not an automated pass/fail gate — every prediction is a signal for human review, not a replacement for it.

```
User Input → Validation → Feature Engineering → Preprocessing → Random Forest → Prediction
```

---

## 🎯 Objective

Build a complete, reproducible ML pipeline — from raw data to a deployed application — that identifies potentially problematic manufacturing cases while being explicit about the trade-off between false positives (unnecessary inspections) and false negatives (missed defects).

**Target variable:** `final_pass` (1 = passed QC, 0 = potentially problematic)

---

## 🧠 Model Performance

| Metric | Value | What it means |
|---|---|---|
| Accuracy | 85.4% | Overall correct predictions across all test cases |
| ROC-AUC | 70.1% | Ability to distinguish pass vs. problematic cases |
| PR-AUC | 42.4% | Precision-recall trade-off on the rarer, harder class |
| Minority Precision | 39.8% | Of units flagged as problematic, ~40% actually are |
| Minority Recall | 35.5% | Of actually problematic units, the model catches ~35% |
| False Positive Rate | 7.6% | Passing units incorrectly flagged |
| False Negative Rate | 64.5% | Problematic units the model misses |

**Model:** Random Forest Classifier · **Decision threshold:** 0.50 · **Training data:** 10,000 manufacturing records (87.6% pass / 12.4% problematic)

> ⚠️ **Known limitation:** the model currently misses roughly two-thirds of true problem cases (high false negative rate). It is tuned to keep false alarms low, at the cost of recall on the minority class. See the in-app **Model Insights** page for the full breakdown, and `reports/06_Model_Interpretation/` for the detailed writeup.

---

## 🖥️ Application Walkthrough

The Streamlit app has five pages:

| Page | Purpose |
|---|---|
| **🏭 Home** | Project overview, model snapshot, dataset summary, architecture diagram |
| **🔍 Predict** | Score a single manufacturing observation via a guided input form, with one-click example scenarios |
| **🎛️ What-If Explorer** | Live, slider-driven exploration — watch the prediction update in real time as you change inputs, plus a sensitivity chart isolating the effect of one feature at a time |
| **📊 Model Insights** | Performance metrics, feature importance, and documented strengths/limitations |
| **📁 Batch Prediction** | Upload a CSV of many observations and score them all at once, with downloadable results |

---

## 📂 Project Structure

```
FactoryGuard-AI/
│
├── data/
│   ├── raw/                  # Original manufacturing dataset (10,000 records)
│   ├── interim/               # Cleaned working dataset
│   └── processed/             # Train/test splits + final feature list
│
├── notebooks/                 # Phase-by-phase development notebooks
│   ├── 02_Initial_Data_Exploration.ipynb
│   ├── 03_exploratory_data_analysis.ipynb
│   ├── 04_Feature_Engineering.ipynb
│   ├── 05_Model_Development.ipynb
│   ├── 06_Model_Interpretation.ipynb
│   └── 07_Deployment_Preparation.ipynb
│
├── docs/                      # Project documentation by phase
│   ├── 01_Project_Foundation/
│   ├── 02_Data_Collection_Understanding/
│   ├── 03_Exploratory_Data_Analysis/
│   ├── 04_Feature_Engineering/
│   └── 05_Model_Development/
│
├── reports/                   # Generated figures & tables per phase
│   ├── 03_EDA/
│   ├── 05_Model_Development/
│   ├── 06_Model_Interpretation/
│   └── 07_Deployment/
│
├── src/                       # Reusable pipeline logic
│   ├── validation.py          # Input schema & range validation
│   ├── feature_engineering.py # Raw input → model features
│   └── prediction.py          # Load artifacts & run inference
│
├── models/
│   ├── final_factoryguard_model.pkl
│   └── preprocessing_pipeline.pkl
│
├── streamlit_app/              # Deployed application
│   ├── app.py                  # Home page
│   ├── utils.py                 # Shared data/model loading & prediction helpers
│   ├── pages/
│   │   ├── 1_Predict.py
│   │   ├── 2_What_If_Explorer.py
│   │   ├── 3_Model_Insights.py
│   │   └── 4_Batch_Prediction.py
│   └── assets/                  # Images used in the app
│
├── references/                 # Business requirements & source notes
├── requirements.txt
├── main.py
└── README.md
```

---

## ⚙️ Tech Stack

- **Language:** Python 3.12
- **Data & ML:** pandas, numpy, scikit-learn, xgboost
- **Interpretability:** shap
- **Visualization:** matplotlib, seaborn
- **Application:** Streamlit (multipage app)
- **Model persistence:** joblib

---

## 🚀 Running Locally

```bash
# 1. Clone the repository
git clone https://github.com/Bhardwaj-Arin/FactoryGuard-AI-Intelligent-Manufacturing-Quality-Decision-System.git
cd FactoryGuard-AI-Intelligent-Manufacturing-Quality-Decision-System

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run streamlit_app/app.py
```

The app will open at `http://localhost:8501`.

---

## 🔍 How a Prediction Works

1. **Validation** (`src/validation.py`) — checks required fields are present, categorical values are known, and numeric values fall within observed training ranges
2. **Feature Engineering** (`src/feature_engineering.py`) — derives model-ready features (e.g., time-based features from the event timestamp) from raw input
3. **Preprocessing** — the saved `ColumnTransformer` pipeline encodes categoricals and scales numerics exactly as done during training
4. **Inference** (`src/prediction.py`) — the Random Forest model outputs class probabilities; the 0.50 decision threshold converts that into a Pass / Potentially Problematic label

The same three modules power both the notebooks and the live Streamlit app, so there is a single source of truth for the pipeline logic.

---

## ⚠️ Known Limitations

- **Recall on problematic cases is limited (~35%)** — the model is conservative and will miss a meaningful share of true defects; it should not be used as a sole gatekeeper
- **Class imbalance** — problematic cases make up only ~12% of training data, which caps how well any model can learn that class without further rebalancing or additional features
- **Synthetic dataset** — trained on a structured/simulated manufacturing dataset rather than live plant-floor data; performance on real production data has not been validated

See `reports/06_Model_Interpretation/business_interpretation_and_limitations.md` for the full discussion, and the in-app Model Insights page for a live view of strengths, limitations, and planned improvements.

---

## 📄 License

See [`LICENSE`](./LICENSE) for details.

---

## 🙋 About

Built as an end-to-end applied ML project covering data understanding, EDA, feature engineering, model development, interpretation, and deployment — documented at every phase in `docs/` and `reports/`.

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils import (
    METRICS_PATH,
    FEATURE_IMPORTANCE_PATH,
    BUSINESS_INTERP_PATH,
    STRENGTHS_PATH,
    LIMITATIONS_PATH,
    FUTURE_IMPROVEMENTS_PATH,
    FEATURE_IMPORTANCE_IMAGE_PATH,
)

st.set_page_config(page_title="Model Insights - FactoryGuard AI", page_icon="📊", layout="wide")

st.title("📊 Model Insights")
st.markdown(
    "Performance, key drivers, and known limitations of the final Random "
    "Forest model, as documented during model interpretation."
)

# ============================================================
# METRICS
# ============================================================

st.header("Performance Metrics")

metrics_df = pd.read_csv(METRICS_PATH)
metrics = dict(zip(metrics_df["Metric"], metrics_df["Percentage"]))

col1, col2, col3, col4 = st.columns(4)
col1.metric("Accuracy", f"{metrics['Accuracy']:.2f}%")
col2.metric("ROC-AUC", f"{metrics['ROC-AUC']:.2f}%")
col3.metric("PR-AUC", f"{metrics['PR-AUC']:.2f}%")
col4.metric("Minority F1-score", f"{metrics['Minority F1-score']:.2f}%")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Minority Precision", f"{metrics['Minority Precision']:.2f}%")
col2.metric("Minority Recall", f"{metrics['Minority Recall']:.2f}%")
col3.metric("False Positive Rate", f"{metrics['False Positive Rate']:.2f}%")
col4.metric("False Negative Rate", f"{metrics['False Negative Rate']:.2f}%")

st.caption(
    "'Minority class' = Class 0 (potentially problematic units), roughly 12% of observations."
)

# ============================================================
# FEATURE IMPORTANCE
# ============================================================

st.header("Top Feature Importance")

col1, col2 = st.columns([1.3, 1])

with col1:
    if FEATURE_IMPORTANCE_IMAGE_PATH.exists():
        st.image(str(FEATURE_IMPORTANCE_IMAGE_PATH), use_container_width=True)
    else:
        fi_df = pd.read_csv(FEATURE_IMPORTANCE_PATH)
        st.bar_chart(fi_df.set_index("feature")["importance"])

with col2:
    fi_df = pd.read_csv(FEATURE_IMPORTANCE_PATH)
    st.dataframe(fi_df, use_container_width=True, hide_index=True)

# ============================================================
# BUSINESS INTERPRETATION
# ============================================================

st.header("Business Interpretation")
business_df = pd.read_csv(BUSINESS_INTERP_PATH)
for _, row in business_df.iterrows():
    st.markdown(f"**{row['Aspect']}** — {row['Interpretation']}")

# ============================================================
# STRENGTHS / LIMITATIONS / FUTURE IMPROVEMENTS
# ============================================================

tab1, tab2, tab3 = st.tabs(["✅ Strengths", "⚠️ Limitations", "🚀 Future Improvements"])

with tab1:
    st.dataframe(pd.read_csv(STRENGTHS_PATH), use_container_width=True, hide_index=True)

with tab2:
    st.dataframe(pd.read_csv(LIMITATIONS_PATH), use_container_width=True, hide_index=True)

with tab3:
    st.dataframe(pd.read_csv(FUTURE_IMPROVEMENTS_PATH), use_container_width=True, hide_index=True)

st.info(
    "Recommended system role: use FactoryGuard AI as a decision-support and "
    "screening system rather than a fully automated quality-control system."
)

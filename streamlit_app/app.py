import pandas as pd
import streamlit as st

from utils import (
    load_reference_data,
    load_artifacts,
    METRICS_PATH,
    ARCHITECTURE_IMAGE_PATH,
)

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FactoryGuard AI",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# HEADER
# ============================================================

st.title("🏭 FactoryGuard AI")
st.subheader("Manufacturing Quality Decision-Support System")

st.markdown(
    """
    FactoryGuard AI analyzes manufacturing and process data to help production
    teams flag potentially problematic units **before** they move further down
    the line. It is a screening and decision-support tool, not a replacement
    for human quality-control judgment.

    Use the pages in the left sidebar to explore the project:

    - **🔍 Predict** – enter a single manufacturing observation and get a live model prediction.
    - **📁 Batch Prediction** – upload a CSV of observations and score them all at once.
    - **📊 Model Insights** – model performance, feature importance, and known limitations.
    """
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.header("About FactoryGuard AI")
    st.markdown(
        """
        **Final Model**
        Random Forest Classifier

        **Target**
        `final_pass` (1 = passed, 0 = potentially problematic)

        **Decision Threshold**
        0.50

        **Important**
        This system is intended as a screening and decision-support tool,
        not a replacement for human quality-control judgment.
        """
    )

# ============================================================
# LOAD DATA / ARTIFACTS
# ============================================================

with st.spinner("Loading dataset and model artifacts..."):
    reference_df = load_reference_data()
    preprocessor, model = load_artifacts()

# ============================================================
# KEY METRICS
# ============================================================

st.header("Model Snapshot")

metrics_df = pd.read_csv(METRICS_PATH)
metrics = dict(zip(metrics_df["Metric"], metrics_df["Percentage"]))

col1, col2, col3, col4 = st.columns(4)
col1.metric("Accuracy", f"{metrics['Accuracy']:.1f}%")
col2.metric("ROC-AUC", f"{metrics['ROC-AUC']:.1f}%")
col3.metric("Minority Recall", f"{metrics['Minority Recall']:.1f}%")
col4.metric("False Positive Rate", f"{metrics['False Positive Rate']:.1f}%")

st.caption(
    "\"Minority\" refers to Class 0 (potentially problematic units), which makes up "
    "roughly 12% of observations. See the Model Insights page for the full breakdown."
)

# ============================================================
# DATASET SNAPSHOT
# ============================================================

st.header("Dataset Snapshot")

col1, col2, col3 = st.columns(3)
col1.metric("Total Observations", f"{len(reference_df):,}")
col2.metric("Plants", reference_df["plant"].nunique())
col3.metric("Machines Tracked", reference_df["machine_id"].nunique())

with st.expander("Preview raw manufacturing data"):
    st.dataframe(reference_df.head(20), use_container_width=True)

# ============================================================
# ARCHITECTURE
# ============================================================

st.header("System Architecture")

if ARCHITECTURE_IMAGE_PATH.exists():
    st.image(
        str(ARCHITECTURE_IMAGE_PATH),
        caption="FactoryGuard AI deployment architecture",
        use_container_width=True,
    )
else:
    st.markdown(
        "`User Input → Validation → Feature Engineering → Preprocessing "
        "→ Random Forest → Prediction`"
    )

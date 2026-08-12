import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils import (
    load_reference_data,
    load_artifacts,
    run_batch_prediction,
    RAW_INPUT_COLUMNS,
)

st.set_page_config(page_title="Batch Prediction - FactoryGuard AI", page_icon="📁", layout="wide")

st.title("📁 Batch Prediction")

st.markdown(
    """
    **What is this page for?**

    The Predict and What-If pages handle **one unit at a time** - useful for
    exploring a single case. In a real plant, you'd often have a spreadsheet
    of dozens or hundreds of units from a shift, a batch, or a day, and want
    predictions for **all of them at once**.

    That's this page: upload a CSV of manufacturing observations, and get a
    prediction + probability for every row back in one table, ready to
    download and act on (e.g., route flagged units to manual inspection).
    """
)

st.markdown("**Required columns in your CSV** (must match these names exactly):")
st.code(", ".join(RAW_INPUT_COLUMNS), language="text")

reference_df = load_reference_data()
preprocessor, model = load_artifacts()

with st.expander("Don't have a file handy? Download a sample template"):
    template_df = reference_df[RAW_INPUT_COLUMNS].head(5)
    st.dataframe(template_df, use_container_width=True)
    st.download_button(
        "Download sample CSV",
        data=template_df.to_csv(index=False),
        file_name="factoryguard_sample_input.csv",
        mime="text/csv",
    )

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    try:
        batch_df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Could not read the uploaded file: {e}")
        st.stop()

    st.subheader("Preview")
    st.dataframe(batch_df.head(10), use_container_width=True)
    st.caption(f"{len(batch_df)} row(s) detected.")

    if st.button("🔍 Run Batch Prediction", use_container_width=True):
        with st.spinner("Scoring uploaded observations..."):
            result_df, errors = run_batch_prediction(batch_df, preprocessor, model, reference_df)

        if errors:
            st.error("Input validation failed:")
            for err in errors:
                st.markdown(f"- {err}")
        else:
            st.success(f"Scored {len(result_df)} observation(s).")

            n_pass = int((result_df["prediction"] == 1).sum())
            n_flag = int((result_df["prediction"] == 0).sum())

            col1, col2, col3 = st.columns(3)
            col1.metric("Predicted Pass", n_pass)
            col2.metric("Predicted Problematic", n_flag)
            col3.metric("Flagged Rate", f"{n_flag / len(result_df):.1%}")

            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                st.markdown("**Pass vs. Problematic**")
                st.bar_chart(
                    result_df["prediction_label"].value_counts()
                )
            with chart_col2:
                st.markdown("**Distribution of pass-probability**")
                st.bar_chart(
                    pd.cut(result_df["class_1_probability"], bins=10)
                    .value_counts()
                    .sort_index()
                )

            st.subheader("Full Results")
            st.dataframe(result_df, use_container_width=True)

            st.download_button(
                "Download results as CSV",
                data=result_df.to_csv(index=False),
                file_name="factoryguard_batch_predictions.csv",
                mime="text/csv",
                use_container_width=True,
            )

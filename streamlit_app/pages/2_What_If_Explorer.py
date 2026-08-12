import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils import (
    load_reference_data,
    load_artifacts,
    get_category_options,
    get_numeric_ranges,
    run_single_prediction,
    run_batch_prediction,
    build_sensitivity_frame,
    RAW_INPUT_COLUMNS,
    NUMERICAL_COLUMNS,
    FIELD_HELP,
    EXAMPLE_SCENARIOS,
)

st.set_page_config(page_title="What-If Explorer - FactoryGuard AI", page_icon="🎛️", layout="wide")

st.title("🎛️ What-If Explorer")
st.markdown(
    "Unlike the Predict page (fill in a form, click submit), everything here "
    "updates **live** as you move a slider - so you can build intuition for "
    "which factors actually move the prediction."
)

reference_df = load_reference_data()
preprocessor, model = load_artifacts()
category_options = get_category_options(reference_df)
numeric_ranges = get_numeric_ranges(reference_df)

# ============================================================
# BASELINE SCENARIO
# ============================================================

st.subheader("1. Start from a baseline")
baseline_choice = st.radio(
    "Pick a starting point, then adjust the sliders below it.",
    options=["Typical pass", "Typical problem case", "Random real record"],
    horizontal=True,
)

if baseline_choice == "Random real record":
    if st.button("🎲 Draw a new random record"):
        st.session_state["wi_random_idx"] = reference_df.sample(1).index[0]
    if "wi_random_idx" not in st.session_state:
        st.session_state["wi_random_idx"] = reference_df.sample(1).index[0]
    baseline = reference_df.loc[st.session_state["wi_random_idx"], RAW_INPUT_COLUMNS].to_dict()
else:
    baseline = EXAMPLE_SCENARIOS[baseline_choice]

st.divider()

# ============================================================
# LIVE-ADJUSTABLE INPUTS
# ============================================================
# Deliberately outside any st.form - every widget change triggers an
# immediate rerun, so the prediction below updates instantly.

st.subheader("2. Adjust the inputs")

current = {}

col1, col2, col3 = st.columns(3)
with col1:
    current["plant"] = st.selectbox("Plant", category_options["plant"],
                                     index=category_options["plant"].index(baseline["plant"]),
                                     help=FIELD_HELP["plant"])
    current["material_grade"] = st.selectbox("Material Grade", category_options["material_grade"],
                                               index=category_options["material_grade"].index(baseline["material_grade"]),
                                               help=FIELD_HELP["material_grade"])
    current["defect_type"] = st.selectbox("Defect Type", category_options["defect_type"],
                                           index=category_options["defect_type"].index(baseline["defect_type"]),
                                           help=FIELD_HELP["defect_type"])
with col2:
    current["shift"] = st.selectbox("Shift", category_options["shift"],
                                     index=category_options["shift"].index(baseline["shift"]),
                                     help=FIELD_HELP["shift"])
    current["inspection_method"] = st.selectbox("Inspection Method", category_options["inspection_method"],
                                                  index=category_options["inspection_method"].index(baseline["inspection_method"]),
                                                  help=FIELD_HELP["inspection_method"])
    current["decision_rework"] = st.selectbox("Rework Decision", [0, 1],
                                               index=int(baseline["decision_rework"]),
                                               format_func=lambda x: "No" if x == 0 else "Yes",
                                               help=FIELD_HELP["decision_rework"])
with col3:
    current["line"] = st.selectbox("Production Line", category_options["line"],
                                    index=category_options["line"].index(baseline["line"]),
                                    help=FIELD_HELP["line"])
    current["machine_id"] = st.selectbox("Machine ID", category_options["machine_id"],
                                          index=category_options["machine_id"].index(baseline["machine_id"]),
                                          help=FIELD_HELP["machine_id"])

st.markdown("**Drag to explore** (these are the biggest drivers of the prediction):")

slider_col1, slider_col2 = st.columns(2)

with slider_col1:
    lo, hi, _ = numeric_ranges["cost_usd"]
    current["cost_usd"] = st.slider("Cost (USD)", lo, hi, float(baseline["cost_usd"]), help=FIELD_HELP["cost_usd"])

    current["defect_severity_0to3"] = st.select_slider(
        "Defect Severity (0-3)", options=[0, 1, 2, 3], value=int(baseline["defect_severity_0to3"]),
        help=FIELD_HELP["defect_severity_0to3"]
    )

    lo, hi, _ = numeric_ranges["energy_kwh"]
    current["energy_kwh"] = st.slider("Energy (kWh)", lo, hi, float(baseline["energy_kwh"]), help=FIELD_HELP["energy_kwh"])

    lo, hi, _ = numeric_ranges["machine_age_yrs"]
    current["machine_age_yrs"] = st.slider("Machine Age (years)", lo, hi, float(baseline["machine_age_yrs"]), help=FIELD_HELP["machine_age_yrs"])

with slider_col2:
    lo, hi, _ = numeric_ranges["total_cycle_time_min"]
    current["total_cycle_time_min"] = st.slider("Total Cycle Time (min)", lo, hi, float(baseline["total_cycle_time_min"]), help=FIELD_HELP["total_cycle_time_min"])

    lo, hi, _ = numeric_ranges["process_speed_units_hr"]
    current["process_speed_units_hr"] = st.slider("Process Speed (units/hr)", lo, hi, float(baseline["process_speed_units_hr"]), help=FIELD_HELP["process_speed_units_hr"])

    lo, hi, _ = numeric_ranges["temp_c"]
    current["temp_c"] = st.slider("Temperature (°C)", lo, hi, float(baseline["temp_c"]), help=FIELD_HELP["temp_c"])

    lo, hi, _ = numeric_ranges["humidity_pct"]
    current["humidity_pct"] = st.slider("Humidity (%)", lo, hi, float(baseline["humidity_pct"]), help=FIELD_HELP["humidity_pct"])

current["event_ts"] = baseline["event_ts"]

input_df = pd.DataFrame([current])[RAW_INPUT_COLUMNS]

# ============================================================
# LIVE PREDICTION
# ============================================================

st.divider()
st.subheader("3. Live prediction")

result, errors = run_single_prediction(input_df, preprocessor, model, reference_df)

if errors:
    st.error("This combination isn't valid: " + " | ".join(errors))
else:
    prob_pass = result["class_1_probability"]
    result_col, chart_col = st.columns([1, 2])

    with result_col:
        if result["prediction"] == 0:
            st.error("⚠️ Potentially Problematic")
        else:
            st.success("✅ Likely to Pass")
        st.metric("Pass probability", f"{prob_pass:.1%}")

    with chart_col:
        st.progress(float(prob_pass))
        st.caption("This bar moves as you adjust any slider or dropdown above.")

    # --------------------------------------------------------
    # SENSITIVITY CHART - vary ONE feature, hold the rest fixed
    # --------------------------------------------------------
    st.divider()
    st.subheader("4. Sensitivity: what if only ONE thing changed?")
    st.markdown(
        "Pick a feature below. Every other field stays exactly as set above - "
        "this isolates the effect of that one feature on the pass probability."
    )

    sweepable = [c for c in RAW_INPUT_COLUMNS if c not in ("event_ts",)]
    vary_column = st.selectbox("Feature to vary", options=sweepable, index=sweepable.index("cost_usd"))

    sweep_df, sweep_values = build_sensitivity_frame(current, vary_column, reference_df)
    sweep_result_df, sweep_errors = run_batch_prediction(sweep_df, preprocessor, model, reference_df)

    if sweep_errors:
        st.warning("Could not compute sensitivity for this feature.")
    else:
        chart_data = pd.DataFrame({
            vary_column: sweep_values,
            "Pass probability": sweep_result_df["class_1_probability"].values,
        }).set_index(vary_column)
        st.line_chart(chart_data)
        st.caption(
            f"Current value of '{vary_column}': {current[vary_column]} — "
            "move the slider/dropdown above to change the fixed baseline for this chart."
        )

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
    RAW_INPUT_COLUMNS,
    FINAL_THRESHOLD,
    FIELD_HELP,
    SECTION_HELP,
    EXAMPLE_SCENARIOS,
)

st.set_page_config(page_title="Predict - FactoryGuard AI", page_icon="🔍", layout="wide")

st.title("🔍 Predict a Single Observation")
st.markdown(
    "Enter the manufacturing and process information below to get a live "
    "prediction from the trained FactoryGuard AI model. Hover the **(?)** "
    "next to any field for what it means."
)

reference_df = load_reference_data()
preprocessor, model = load_artifacts()
category_options = get_category_options(reference_df)
numeric_ranges = get_numeric_ranges(reference_df)

# ============================================================
# ONE-CLICK EXAMPLES
# ============================================================
# Prefills the form via session_state so a new user can explore
# realistic scenarios instead of typing 17 fields blind.

st.markdown("**New here? Load a real example first:**")
ex_col1, ex_col2, ex_col3 = st.columns([1, 1, 2])

if ex_col1.button("✅ Load 'Typical Pass' example", use_container_width=True):
    for key, value in EXAMPLE_SCENARIOS["Typical pass"].items():
        st.session_state[f"in_{key}"] = value
    st.rerun()

if ex_col2.button("⚠️ Load 'Typical Problem' example", use_container_width=True):
    for key, value in EXAMPLE_SCENARIOS["Typical problem case"].items():
        st.session_state[f"in_{key}"] = value
    st.rerun()

st.divider()


def sval(key, default):
    """Read a prefilled value from session_state, if an example was loaded."""
    return st.session_state.get(f"in_{key}", default)


def num_input(label, column, **kwargs):
    lo, hi, mean = numeric_ranges[column]
    default = sval(column, round(mean, 2))
    return st.number_input(
        label,
        min_value=lo,
        max_value=hi,
        value=float(default),
        help=FIELD_HELP.get(column, ""),
        **kwargs,
    )


def cat_select(label, column):
    options = category_options[column]
    default = sval(column, options[0])
    index = options.index(default) if default in options else 0
    return st.selectbox(label, options=options, index=index, help=FIELD_HELP.get(column, ""))


with st.form(key="factoryguard_input_form"):

    # --------------------------------------------------------
    # Section A - Production Information
    # --------------------------------------------------------
    st.subheader("1. Production Information")
    st.caption(SECTION_HELP["production"])
    col1, col2, col3 = st.columns(3)
    with col1:
        plant = cat_select("Plant", "plant")
    with col2:
        line = cat_select("Production Line", "line")
    with col3:
        shift = cat_select("Shift", "shift")

    # --------------------------------------------------------
    # Section B - Machine & Material Information
    # --------------------------------------------------------
    st.subheader("2. Machine & Material Information")
    st.caption(SECTION_HELP["machine_material"])
    col1, col2, col3 = st.columns(3)
    with col1:
        machine_id = cat_select("Machine ID", "machine_id")
    with col2:
        machine_age_yrs = num_input("Machine Age (years)", "machine_age_yrs", step=0.1)
    with col3:
        material_grade = cat_select("Material Grade", "material_grade")

    # --------------------------------------------------------
    # Section C - Environmental Conditions
    # --------------------------------------------------------
    st.subheader("3. Environmental Conditions")
    st.caption(SECTION_HELP["environment"])
    col1, col2 = st.columns(2)
    with col1:
        temp_c = num_input("Temperature (°C)", "temp_c", step=0.1)
    with col2:
        humidity_pct = num_input("Humidity (%)", "humidity_pct", step=0.1)

    # --------------------------------------------------------
    # Section D - Process Information
    # --------------------------------------------------------
    st.subheader("4. Process Information")
    st.caption(SECTION_HELP["process"])
    col1, col2, col3 = st.columns(3)
    with col1:
        process_speed_units_hr = num_input(
            "Process Speed (units/hr)", "process_speed_units_hr", step=1.0
        )
    with col2:
        total_cycle_time_min = num_input(
            "Total Cycle Time (min)", "total_cycle_time_min", step=0.1
        )
    with col3:
        decision_rework = st.selectbox(
            "Rework Decision",
            options=[0, 1],
            index=sval("decision_rework", 0),
            format_func=lambda x: "No" if x == 0 else "Yes",
            help=FIELD_HELP["decision_rework"],
        )

    # --------------------------------------------------------
    # Section E - Inspection & Defect Information
    # --------------------------------------------------------
    st.subheader("5. Inspection & Defect Information")
    st.caption(SECTION_HELP["inspection"])
    col1, col2, col3 = st.columns(3)
    with col1:
        inspection_method = cat_select("Inspection Method", "inspection_method")
    with col2:
        defect_type = cat_select("Defect Type", "defect_type")
    with col3:
        severity_default = sval("defect_severity_0to3", 0)
        defect_severity_0to3 = st.selectbox(
            "Defect Severity (0-3)",
            options=[0, 1, 2, 3],
            index=[0, 1, 2, 3].index(severity_default),
            help=FIELD_HELP["defect_severity_0to3"],
        )

    # --------------------------------------------------------
    # Section F - Energy & Cost
    # --------------------------------------------------------
    st.subheader("6. Energy & Cost Information")
    st.caption(SECTION_HELP["energy_cost"])
    col1, col2 = st.columns(2)
    with col1:
        energy_kwh = num_input("Energy Consumption (kWh)", "energy_kwh", step=0.01)
    with col2:
        cost_usd = num_input("Cost (USD)", "cost_usd", step=0.01)

    # --------------------------------------------------------
    # Section G - Event Timestamp
    # --------------------------------------------------------
    st.subheader("7. Event Timestamp")
    st.caption(SECTION_HELP["timestamp"])
    default_ts = pd.to_datetime(sval("event_ts", "2026-01-01 12:00:00"))
    col1, col2 = st.columns(2)
    with col1:
        event_date = st.date_input("Event Date", value=default_ts.date())
    with col2:
        event_time = st.time_input("Event Time", value=default_ts.time(), help=FIELD_HELP["event_ts"])

    submitted = st.form_submit_button("🔍 Run Prediction", use_container_width=True)


if submitted:

    event_ts = f"{event_date} {event_time}"

    input_data = {
        "plant": plant, "line": line, "shift": shift, "machine_id": machine_id,
        "machine_age_yrs": machine_age_yrs, "material_grade": material_grade,
        "temp_c": temp_c, "humidity_pct": humidity_pct,
        "process_speed_units_hr": process_speed_units_hr,
        "inspection_method": inspection_method, "defect_type": defect_type,
        "defect_severity_0to3": defect_severity_0to3, "decision_rework": decision_rework,
        "total_cycle_time_min": total_cycle_time_min, "energy_kwh": energy_kwh,
        "cost_usd": cost_usd, "event_ts": event_ts,
    }

    input_df = pd.DataFrame([input_data])[RAW_INPUT_COLUMNS]

    result, errors = run_single_prediction(input_df, preprocessor, model, reference_df)

    if errors:
        st.error("Input validation failed:")
        for err in errors:
            st.markdown(f"- {err}")
    else:
        prob_fail = result["class_0_probability"]
        prob_pass = result["class_1_probability"]

        st.divider()
        st.subheader("Prediction Result")

        result_col, detail_col = st.columns([1, 1.4])

        with result_col:
            if result["prediction"] == 0:
                st.error("⚠️ Potentially Problematic")
            else:
                st.success("✅ Likely to Pass")

            st.metric("Confidence in this call", f"{max(prob_pass, prob_fail):.0%}")

        with detail_col:
            st.markdown(f"**Probability of passing:** {prob_pass:.1%}")
            st.progress(float(prob_pass))
            st.markdown(f"**Probability of being problematic:** {prob_fail:.1%}")
            st.progress(float(prob_fail))
            st.caption(
                f"Decision rule: flagged as 'Potentially Problematic' if pass-probability "
                f"falls below the {FINAL_THRESHOLD:.0%} threshold."
            )

        with st.expander("View the exact input that was submitted"):
            st.dataframe(input_df, use_container_width=True)

        st.info(
            "FactoryGuard AI is a screening tool. Treat a 'Potentially Problematic' "
            "result as a signal for human review, not an automatic rejection — "
            "see the Model Insights page for how often each type of mistake happens."
        )

"""
FactoryGuard AI - Streamlit shared utilities.

Centralises path resolution, artifact loading, and prediction
helpers so that app.py and every file under pages/ can reuse the
exact same logic instead of duplicating it.
"""

import sys
import warnings
from pathlib import Path

import pandas as pd
import streamlit as st

# ============================================================
# PROJECT PATHS
# ============================================================
# This file lives at <PROJECT_ROOT>/streamlit_app/utils.py, so the
# project root is always one level up from here - regardless of
# whether the caller is app.py or a file under streamlit_app/pages/.

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "manufacturing_quality_decisions_10000.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "final_factoryguard_model.pkl"
PREPROCESSOR_PATH = PROJECT_ROOT / "models" / "preprocessing_pipeline.pkl"

METRICS_PATH = PROJECT_ROOT / "reports" / "06_Model_Interpretation" / "tables" / "final_model_metrics.csv"
FEATURE_IMPORTANCE_PATH = PROJECT_ROOT / "reports" / "06_Model_Interpretation" / "tables" / "top_15_features.csv"
BUSINESS_INTERP_PATH = PROJECT_ROOT / "reports" / "06_Model_Interpretation" / "tables" / "business_interpretation.csv"
STRENGTHS_PATH = PROJECT_ROOT / "reports" / "06_Model_Interpretation" / "tables" / "model_strengths.csv"
LIMITATIONS_PATH = PROJECT_ROOT / "reports" / "06_Model_Interpretation" / "tables" / "model_limitations.csv"
FUTURE_IMPROVEMENTS_PATH = PROJECT_ROOT / "reports" / "06_Model_Interpretation" / "tables" / "future_improvements.csv"
INPUT_SCHEMA_PATH = PROJECT_ROOT / "reports" / "07_Deployment" / "tables" / "factoryguard_input_schema.csv"

ARCHITECTURE_IMAGE_PATH = Path(__file__).resolve().parent / "assets" / "factoryguard_deployment_architecture.png"
FEATURE_IMPORTANCE_IMAGE_PATH = Path(__file__).resolve().parent / "assets" / "top_15_feature_importance.png"

FINAL_THRESHOLD = 0.50

# ============================================================
# UI TEXT: field tooltips + section descriptions
# ============================================================
# Plain-language help text shown as (?) tooltips on each widget, and
# as captions under each section header - so the form teaches the
# domain instead of just collecting numbers.

FIELD_HELP = {
    "plant": "Which factory location made this unit.",
    "line": "Which physical assembly line inside that plant (like a specific conveyor belt).",
    "shift": "Which work shift was on duty: day, night, or swing (evening/rotating).",
    "machine_id": "The specific machine that processed this unit.",
    "machine_age_yrs": "Years the machine has been in service. Older machines can drift out of calibration.",
    "material_grade": "Quality tier of the raw material fed into the machine.",
    "temp_c": "Ambient/process temperature. Heat can affect material behavior and machine performance.",
    "humidity_pct": "Ambient humidity. Affects material curing, static buildup, and corrosion risk.",
    "process_speed_units_hr": "How many units per hour the line was running - a proxy for how rushed the run was.",
    "total_cycle_time_min": "Minutes to complete one unit, start to finish.",
    "decision_rework": "Whether this unit was already flagged for rework before the final QC check.",
    "inspection_method": "How the unit was checked: manual (human), sensor, or vision (camera/AI).",
    "defect_type": "What kind of flaw was found, if any.",
    "defect_severity_0to3": "How severe the defect is: 0 = none, 3 = most severe.",
    "energy_kwh": "Electricity used to produce this one unit.",
    "cost_usd": "Total production cost for this one unit.",
    "event_ts": "When this event happened. Used to derive hour-of-day, day-of-week, and month, since defect rates can vary by timing.",
}

SECTION_HELP = {
    "production": "Where and when this unit was made.",
    "machine_material": "What equipment and raw material were used.",
    "environment": "Ambient factory conditions at the time.",
    "process": "How the manufacturing run itself performed.",
    "inspection": "What quality control found, if anything.",
    "energy_cost": "Resources consumed producing this one unit.",
    "timestamp": "When this specific event occurred.",
}

# Two real records from the training data (one that passed cleanly,
# one that was flagged) - used to one-click prefill the Predict form
# so a new user can explore without typing 17 fields from scratch.
EXAMPLE_SCENARIOS = {
    "Typical pass": {
        "plant": "plant_1", "line": "line_A", "shift": "day", "machine_id": "MC104",
        "machine_age_yrs": 1.55, "material_grade": "grade_B", "temp_c": 5.9,
        "humidity_pct": 45.5, "process_speed_units_hr": 104.3,
        "inspection_method": "manual", "defect_type": "none", "defect_severity_0to3": 0,
        "decision_rework": 0, "total_cycle_time_min": 33.7, "energy_kwh": 1.413,
        "cost_usd": 25.53, "event_ts": "2025-08-27 17:15:31",
    },
    "Typical problem case": {
        "plant": "plant_3", "line": "line_D", "shift": "day", "machine_id": "MC142",
        "machine_age_yrs": 7.31, "material_grade": "grade_C", "temp_c": 9.8,
        "humidity_pct": 58.1, "process_speed_units_hr": 108.4,
        "inspection_method": "sensor", "defect_type": "scratch", "defect_severity_0to3": 3,
        "decision_rework": 1, "total_cycle_time_min": 72.3, "energy_kwh": 1.872,
        "cost_usd": 159.56, "event_ts": "2025-09-27 21:26:55",
    },
}

# ============================================================
# GLOSSARY - single source of truth, reused by the Predict page
# (as inline captions) and the How It Works page (as a full
# glossary) so the wording never drifts between the two.
# ============================================================

FORM_SECTIONS = [
    {
        "title": "1. Production Information",
        "summary": "Where and when the unit was made.",
        "fields": [
            ("plant", "Plant",
             "Which of the 3 factories made this unit (plant_1, plant_2, plant_3)."),
            ("line", "Production Line",
             "Which specific line inside that plant (line_A-line_D) - like separate "
             "parallel conveyor lines running in one building."),
            ("shift", "Shift",
             "Which crew was working: day, night, or swing (a rotating shift bridging the two)."),
        ],
    },
    {
        "title": "2. Machine & Material Information",
        "summary": "What equipment and raw material were used.",
        "fields": [
            ("machine_id", "Machine ID",
             "Which specific machine (60 tracked, e.g. MC104) processed it - "
             "individual machines wear and drift differently over time."),
            ("machine_age_yrs", "Machine Age (years)",
             "How long that machine has been in service. Older machines are more "
             "likely to drift out of calibration."),
            ("material_grade", "Material Grade",
             "Quality tier of the raw material used (grade_A / grade_B / grade_C) - "
             "higher grade generally means more consistent material."),
        ],
    },
    {
        "title": "3. Environmental Conditions",
        "summary": "The room/process conditions at the time of production.",
        "fields": [
            ("temp_c", "Temperature (°C)",
             "Ambient or process temperature. Many manufacturing processes "
             "(curing, molding) are sensitive to temperature drift."),
            ("humidity_pct", "Humidity (%)",
             "Ambient humidity. Can affect coatings, adhesives, and surface finishing."),
        ],
    },
    {
        "title": "4. Process Information",
        "summary": "How the manufacturing run itself behaved.",
        "fields": [
            ("process_speed_units_hr", "Process Speed (units/hr)",
             "Throughput - how fast the line ran. Faster isn't always better for quality."),
            ("total_cycle_time_min", "Total Cycle Time (min)",
             "How long this specific unit took start-to-finish. Unusually short or "
             "long times can be a sign something was off."),
            ("decision_rework", "Rework Decision",
             "Whether the unit was pulled mid-process and reworked before final "
             "inspection (Yes/No)."),
        ],
    },
    {
        "title": "5. Inspection & Defect Information",
        "summary": "What quality control found when they checked it.",
        "fields": [
            ("inspection_method", "Inspection Method",
             "How it was checked: manual (human eye), sensor (automated sensor), "
             "or vision (camera / computer-vision)."),
            ("defect_type", "Defect Type",
             "What was found: none, scratch, crack, dimension (wrong size), "
             "finish (surface issue), or contamination."),
            ("defect_severity_0to3", "Defect Severity (0-3)",
             "How bad the defect was, from 0 (none) to 3 (severe)."),
        ],
    },
    {
        "title": "6. Energy & Cost Information",
        "summary": "Resources spent making this unit.",
        "fields": [
            ("energy_kwh", "Energy Consumption (kWh)",
             "Electricity used to produce this unit."),
            ("cost_usd", "Cost (USD)",
             "Production cost of this unit. This is the single most influential "
             "input to the model - it relies on cost more than any other field."),
        ],
    },
    {
        "title": "7. Event Timestamp",
        "summary": "Exactly when the unit was produced.",
        "fields": [
            ("event_ts", "Event Timestamp",
             "The date and time this unit was processed. The model quietly derives "
             "hour-of-day, day-of-week, and month from this, since quality can shift "
             "around shift-changes or end-of-month rushes."),
        ],
    },
]

ML_TERMS_GLOSSARY = [
    ("Class 0 / Class 1",
     "The two possible outcomes. Class 1 = passed quality control (about 88% of "
     "historical units). Class 0 = potentially problematic (about 12%) - rarer, "
     "and the harder case for the model to catch."),
    ("Probability",
     "How confident the model is, from 0-100%. Not a guarantee - 68% Class 1 means "
     "'leans that way', not 'definitely fine'."),
    ("Decision threshold (0.50)",
     "The cutoff rule: if the Class 1 probability is 50% or higher, the app labels "
     "it a pass. This is a dial the business could tune, not a fixed law."),
    ("Accuracy",
     "Out of all predictions, the percentage that were correct overall (~85% here). "
     "Can be misleading on imbalanced data like this - see Recall below."),
    ("Minority class",
     "Class 0 (the problematic units), since they're rare in the data (~12%). "
     "'Minority precision/recall' both describe performance specifically on this "
     "rarer, harder class."),
    ("Recall (minority)",
     "Of all the units that were ACTUALLY problematic, what % did the model catch? "
     "~35% here - it misses roughly 2 out of 3 real problem cases."),
    ("Precision (minority)",
     "Of everything the model FLAGGED as problematic, what % actually were? "
     "~40% here - more than half of its warnings are false alarms."),
    ("ROC-AUC",
     "A single score (0-100%) for how well the model separates the two classes "
     "overall, regardless of threshold. ~70% is meaningfully better than a coin "
     "flip, but not excellent."),
    ("False Positive / False Negative",
     "False positive = flagged as problematic but was actually fine (false alarm). "
     "False negative = looked fine but was actually problematic (a missed defect) - "
     "usually the costlier mistake in quality control."),
    ("Feature importance",
     "A ranking of which inputs (cost, defect severity, energy use, etc.) the "
     "model leans on most when making a decision."),
    ("Validation",
     "Before predicting, the app checks your input makes sense - no missing "
     "fields, categories match known values, numbers are in a realistic range."),
    ("Random Forest",
     "The type of model used - hundreds of simple decision trees vote, and the "
     "average of their votes becomes the final probability."),
    ("Preprocessing pipeline",
     "A behind-the-scenes step that converts raw inputs (like 'plant_1', 'day') "
     "into the numeric format the model needs, using the same rules used in training."),
]

# The raw input columns the trained pipeline requires (mirrors
# src/validation.py RAW_INPUT_COLUMNS exactly).
RAW_INPUT_COLUMNS = [
    "plant", "line", "shift", "machine_id", "machine_age_yrs",
    "material_grade", "temp_c", "humidity_pct", "process_speed_units_hr",
    "inspection_method", "defect_type", "defect_severity_0to3",
    "decision_rework", "total_cycle_time_min", "energy_kwh",
    "cost_usd", "event_ts",
]

CATEGORICAL_COLUMNS = [
    "plant", "line", "shift", "machine_id",
    "material_grade", "inspection_method", "defect_type",
]

NUMERICAL_COLUMNS = [
    "machine_age_yrs", "temp_c", "humidity_pct", "process_speed_units_hr",
    "defect_severity_0to3", "decision_rework", "total_cycle_time_min",
    "energy_kwh", "cost_usd",
]


# ============================================================
# CACHED LOADERS
# ============================================================

@st.cache_data(show_spinner=False)
def load_reference_data() -> pd.DataFrame:
    """Load the raw dataset used both as the model's training
    reference (for validation ranges/categories) and for the
    dashboard's exploratory views."""
    return pd.read_csv(RAW_DATA_PATH)


@st.cache_resource(show_spinner=False)
def load_artifacts():
    """Load the trained preprocessing pipeline and final model.

    Uses the project's own src/prediction.py loader so the app stays
    in sync with however the model is (re)trained/saved.
    """
    from src.prediction import load_factoryguard_artifacts

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        preprocessor, model = load_factoryguard_artifacts(
            MODEL_PATH, PREPROCESSOR_PATH
        )
    return preprocessor, model


@st.cache_data(show_spinner=False)
def get_category_options(_reference_df: pd.DataFrame) -> dict:
    """Build the dropdown option lists from the actual dataset so the
    UI can never submit a category the model has never seen."""
    options = {}
    for column in CATEGORICAL_COLUMNS:
        options[column] = sorted(
            _reference_df[column].dropna().astype(str).unique().tolist()
        )
    return options


@st.cache_data(show_spinner=False)
def get_numeric_ranges(_reference_df: pd.DataFrame) -> dict:
    """Build {column: (min, max, mean)} from the actual dataset so
    numeric widgets default to sane, in-range values."""
    ranges = {}
    for column in NUMERICAL_COLUMNS:
        series = _reference_df[column]
        ranges[column] = (
            float(series.min()),
            float(series.max()),
            float(series.mean()),
        )
    return ranges


# ============================================================
# PREDICTION HELPERS
# ============================================================

def run_single_prediction(input_df: pd.DataFrame, preprocessor, model, reference_df):
    """Run one row through the full FactoryGuard AI pipeline.

    Returns (result_dict, errors). result_dict is None if validation
    failed, in which case errors is a non-empty list of messages.
    """
    from src.validation import validate_factoryguard_input
    from src.prediction import predict_factoryguard

    is_valid, errors = validate_factoryguard_input(input_df, reference_df)
    if not is_valid:
        return None, errors

    result = predict_factoryguard(
        input_df, preprocessor, model, reference_df, threshold=FINAL_THRESHOLD
    )
    return result, []


def build_sensitivity_frame(base_row: dict, vary_column: str, reference_df: pd.DataFrame,
                             n_points: int = 20) -> pd.DataFrame:
    """Build n_points copies of base_row with `vary_column` swept across
    its full observed range (numeric) or all known categories
    (categorical), for a one-feature-at-a-time sensitivity chart."""
    if vary_column in NUMERICAL_COLUMNS:
        lo, hi, _ = get_numeric_ranges(reference_df)[vary_column]
        sweep_values = list(pd.Series(
            [lo + i * (hi - lo) / (n_points - 1) for i in range(n_points)]
        ))
    else:
        sweep_values = get_category_options(reference_df)[vary_column]

    rows = []
    for value in sweep_values:
        row = dict(base_row)
        row[vary_column] = value
        rows.append(row)

    return pd.DataFrame(rows)[RAW_INPUT_COLUMNS], sweep_values


def run_batch_prediction(batch_df: pd.DataFrame, preprocessor, model, reference_df,
                          threshold: float = FINAL_THRESHOLD):
    """Vectorised version of the single-row pipeline for CSV uploads.

    Returns (result_df, errors). result_df is None if validation
    failed, in which case errors is a non-empty list of messages.
    """
    from src.validation import validate_factoryguard_input
    from src.feature_engineering import (
        engineer_factoryguard_features,
        align_factoryguard_schema,
    )

    is_valid, errors = validate_factoryguard_input(batch_df, reference_df)
    if not is_valid:
        return None, errors

    engineered_df = engineer_factoryguard_features(batch_df)
    model_input = align_factoryguard_schema(engineered_df, preprocessor)
    processed_input = preprocessor.transform(model_input)

    probabilities = model.predict_proba(processed_input)
    classes = list(model.classes_)
    class_0_idx = classes.index(0)
    class_1_idx = classes.index(1)

    result_df = batch_df.copy().reset_index(drop=True)
    result_df["class_0_probability"] = probabilities[:, class_0_idx]
    result_df["class_1_probability"] = probabilities[:, class_1_idx]
    result_df["prediction"] = (result_df["class_1_probability"] >= threshold).astype(int)
    result_df["prediction_label"] = result_df["prediction"].map(
        {0: "Class 0 - Potentially Problematic", 1: "Class 1 - Majority Class (Pass)"}
    )

    return result_df, []


import numpy as np
import pandas as pd


RAW_INPUT_COLUMNS = [
    "plant",
    "line",
    "shift",
    "machine_id",
    "machine_age_yrs",
    "material_grade",
    "temp_c",
    "humidity_pct",
    "process_speed_units_hr",
    "inspection_method",
    "defect_type",
    "defect_severity_0to3",
    "decision_rework",
    "total_cycle_time_min",
    "energy_kwh",
    "cost_usd",
    "event_ts"
]


NUMERICAL_COLUMNS = [
    "machine_age_yrs",
    "temp_c",
    "humidity_pct",
    "process_speed_units_hr",
    "defect_severity_0to3",
    "decision_rework",
    "total_cycle_time_min",
    "energy_kwh",
    "cost_usd"
]


CATEGORICAL_COLUMNS = [
    "plant",
    "line",
    "shift",
    "machine_id",
    "material_grade",
    "inspection_method",
    "defect_type"
]


DATETIME_COLUMNS = [
    "event_ts"
]


def validate_factoryguard_input(
    input_df,
    reference_df
):
    """
    Validate raw FactoryGuard AI inference input.

    Returns:
        is_valid: bool
        errors: list[str]
    """

    errors = []

    # ---------------------------------------------
    # Input type
    # ---------------------------------------------

    if not isinstance(
        input_df,
        pd.DataFrame
    ):
        errors.append(
            "Input must be a pandas DataFrame."
        )

        return False, errors

    # ---------------------------------------------
    # Required columns
    # ---------------------------------------------

    missing_columns = [
        column
        for column in RAW_INPUT_COLUMNS
        if column not in input_df.columns
    ]

    if missing_columns:

        errors.append(
            "Missing required columns: "
            f"{missing_columns}"
        )

        return False, errors

    # ---------------------------------------------
    # Missing values
    # ---------------------------------------------

    missing_values = (
        input_df[
            RAW_INPUT_COLUMNS
        ]
        .isna()
        .sum()
    )

    missing_values = (
        missing_values[
            missing_values > 0
        ]
    )

    if not missing_values.empty:

        errors.append(
            "Missing values found: "
            f"{missing_values.to_dict()}"
        )

    # ---------------------------------------------
    # Numerical validation
    # ---------------------------------------------

    for column in NUMERICAL_COLUMNS:

        numeric_values = pd.to_numeric(
            input_df[column],
            errors="coerce"
        )

        if numeric_values.isna().any():

            errors.append(
                f"Column '{column}' "
                "contains non-numeric values."
            )

            continue

        if not np.isfinite(
            numeric_values
        ).all():

            errors.append(
                f"Column '{column}' "
                "contains infinite values."
            )

        min_value = reference_df[
            column
        ].min()

        max_value = reference_df[
            column
        ].max()

        if (
            numeric_values < min_value
        ).any():

            errors.append(
                f"Column '{column}' contains "
                f"value(s) below the observed "
                f"minimum of {min_value}."
            )

        if (
            numeric_values > max_value
        ).any():

            errors.append(
                f"Column '{column}' contains "
                f"value(s) above the observed "
                f"maximum of {max_value}."
            )

    # ---------------------------------------------
    # Categorical validation
    # ---------------------------------------------

    for column in CATEGORICAL_COLUMNS:

        allowed_values = set(
            reference_df[column]
            .dropna()
            .astype(str)
            .unique()
        )

        provided_values = set(
            input_df[column]
            .astype(str)
        )

        invalid_values = (
            provided_values
            - allowed_values
        )

        if invalid_values:

            errors.append(
                f"Column '{column}' contains "
                f"invalid value(s): "
                f"{sorted(invalid_values)}"
            )

    # ---------------------------------------------
    # Timestamp validation
    # ---------------------------------------------

    parsed_timestamp = pd.to_datetime(
        input_df["event_ts"],
        errors="coerce"
    )

    if parsed_timestamp.isna().any():

        errors.append(
            "Column 'event_ts' contains "
            "invalid timestamp value(s)."
        )

    return (
        len(errors) == 0,
        errors
    )

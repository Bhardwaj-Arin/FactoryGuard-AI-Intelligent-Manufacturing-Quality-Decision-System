
import numpy as np
import pandas as pd


def engineer_factoryguard_features(input_df):
    """
    Reproduce the Phase 4 feature engineering
    required for FactoryGuard AI inference.
    """

    df = input_df.copy()

    # ---------------------------------------------
    # Temporal features
    # ---------------------------------------------

    df["event_ts"] = pd.to_datetime(
        df["event_ts"],
        errors="raise"
    )

    df["event_hour"] = (
        df["event_ts"].dt.hour
    )

    df["event_day_of_week"] = (
        df["event_ts"].dt.dayofweek
    )

    df["event_month"] = (
        df["event_ts"].dt.month
    )

    # Remove original timestamp
    df.drop(
        columns=["event_ts"],
        inplace=True
    )

    # ---------------------------------------------
    # Machine age group
    # ---------------------------------------------

    age_bins = [
        -np.inf,
        5,
        10,
        np.inf
    ]

    age_labels = [
        "New",
        "Moderate",
        "Old"
    ]

    df["machine_age_group"] = pd.cut(
        df["machine_age_yrs"],
        bins=age_bins,
        labels=age_labels
    )

    # ---------------------------------------------
    # Plant-shift interaction
    # ---------------------------------------------

    df["plant_shift"] = (
        df["plant"].astype(str)
        + "_"
        + df["shift"].astype(str)
    )

    # ---------------------------------------------
    # Material-shift interaction
    # ---------------------------------------------

    df["material_shift"] = (
        df["material_grade"].astype(str)
        + "_"
        + df["shift"].astype(str)
    )

    return df


def align_factoryguard_schema(
    engineered_df,
    preprocessing_pipeline
):
    """
    Select and order the exact columns expected
    by the saved preprocessing pipeline.
    """

    expected_columns = list(
        preprocessing_pipeline.feature_names_in_
    )

    missing_columns = [
        column
        for column in expected_columns
        if column not in engineered_df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Required model-input columns are missing: "
            f"{missing_columns}"
        )

    return engineered_df[
        expected_columns
    ].copy()

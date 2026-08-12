
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from .feature_engineering import (
    engineer_factoryguard_features,
    align_factoryguard_schema
)

from .validation import (
    validate_factoryguard_input
)


FINAL_THRESHOLD = 0.50


def load_factoryguard_artifacts(
    model_path,
    preprocessor_path
):
    """
    Load the saved FactoryGuard AI model
    and preprocessing pipeline.
    """

    model = joblib.load(
        model_path
    )

    preprocessor = joblib.load(
        preprocessor_path
    )

    return preprocessor, model


def predict_factoryguard(
    input_df,
    preprocessing_pipeline,
    final_model,
    reference_df,
    threshold=FINAL_THRESHOLD
):
    """
    Complete FactoryGuard AI inference pipeline.

    Workflow:

    Input
    → Validation
    → Feature Engineering
    → Schema Alignment
    → Preprocessing
    → Random Forest
    → Probability
    → Threshold
    → Result
    """

    # ---------------------------------------------
    # 1. Validate input
    # ---------------------------------------------

    is_valid, errors = (
        validate_factoryguard_input(
            input_df,
            reference_df
        )
    )

    if not is_valid:

        raise ValueError(
            "Input validation failed: "
            + " | ".join(errors)
        )

    # ---------------------------------------------
    # 2. Feature engineering
    # ---------------------------------------------

    engineered_df = (
        engineer_factoryguard_features(
            input_df
        )
    )

    # ---------------------------------------------
    # 3. Schema alignment
    # ---------------------------------------------

    model_input = (
        align_factoryguard_schema(
            engineered_df,
            preprocessing_pipeline
        )
    )

    # ---------------------------------------------
    # 4. Preprocessing
    # ---------------------------------------------

    processed_input = (
        preprocessing_pipeline.transform(
            model_input
        )
    )

    # ---------------------------------------------
    # 5. Generate probabilities
    # ---------------------------------------------

    probabilities = (
        final_model.predict_proba(
            processed_input
        )[0]
    )

    classes = list(
        final_model.classes_
    )

    class_0_probability = (
        probabilities[
            classes.index(0)
        ]
    )

    class_1_probability = (
        probabilities[
            classes.index(1)
        ]
    )

    # ---------------------------------------------
    # 6. Apply threshold
    # ---------------------------------------------

    prediction = int(
        class_1_probability >= threshold
    )

    # ---------------------------------------------
    # 7. Human-readable result
    # ---------------------------------------------

    if prediction == 0:

        prediction_label = (
            "Class 0 — Potentially Problematic"
        )

    else:

        prediction_label = (
            "Class 1 — Majority Class"
        )

    return {
        "prediction": prediction,
        "prediction_label": prediction_label,
        "class_0_probability": (
            class_0_probability
        ),
        "class_1_probability": (
            class_1_probability
        ),
        "threshold": threshold,
        "model_input": model_input,
        "processed_input": processed_input
    }

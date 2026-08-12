# Folder Structure

> **Project:** FactoryGuard AI: Intelligent Manufacturing Quality Decision System
> **Project Type:** End-to-End Manufacturing Quality Decision System
> **Purpose:** Define the organization, architecture, and development workflow of the FactoryGuard AI repository.

---

# Table of Contents

1. Introduction
2. Why Project Structure Matters
3. Project Directory Overview
4. Root Directory Files
5. Folder Descriptions
6. Detailed Directory Breakdown
7. Data Flow Across the Project
8. Project Architecture
9. Development Guidelines
10. Best Practices
11. Folder Responsibilities
12. Conclusion

---

# 1. Introduction

A well-organized project structure is one of the foundations of a professional Machine Learning project. As manufacturing analytics projects grow, they include datasets, notebooks, reusable source code, trained models, business reports, dashboards, documentation, configuration files, and deployment assets. Without a structured repository, maintaining and extending the project quickly becomes difficult.

FactoryGuard AI follows a modular repository architecture where every directory has a clearly defined responsibility. This organization improves readability, maintainability, collaboration, and reproducibility while supporting the complete lifecycle of a Manufacturing Quality Decision System.

The repository structure has been designed following common software engineering, Data Science, and MLOps practices so that the project remains scalable as new datasets, models, dashboards, and business features are added.

---

# 2. Why Project Structure Matters

A standardized folder structure provides several benefits.

- Keeps the repository organized and easy to navigate.
- Separates data, code, documentation, and artifacts.
- Encourages reusable and modular code.
- Simplifies debugging and testing.
- Makes collaboration easier.
- Supports deployment and future enhancements.
- Improves GitHub presentation.
- Helps recruiters quickly understand the project.

Instead of storing everything in a single folder, FactoryGuard AI groups related files into dedicated directories.

---

# 3. Project Directory Overview

FactoryGuard_AI/
│
├── artifacts/
├── configs/
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── external/
│
├── docs/
├── models/
├── notebooks/
├── reports/
│   ├── figures/
│   └── tables/
│
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── visualization/
│   ├── utils/
│   └── pipeline/
│
├── streamlit/
├── tests/
│
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
└── main.py

This structure separates project assets based on their purpose rather than their file type.

---

# 4. Root Directory Files

The root directory contains the files required to configure, execute, and understand the project.

---

## README.md

The main entry point for the repository.

### Purpose

- Project introduction
- Installation guide
- Features
- Folder structure
- Usage instructions
- Screenshots
- Future improvements
- License information

---

## requirements.txt

Lists all Python dependencies required to run the project.

Example packages include:

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- xgboost
- shap
- streamlit
- joblib

Keeping dependencies in one file ensures reproducibility across environments.

---

## LICENSE

Specifies the legal license under which the project is distributed.

Common choices include:

- MIT License
- Apache 2.0
- GPL

---

## .gitignore

Defines files and folders that Git should ignore.

Typical entries include:

- virtual environments
- cache files
- temporary files
- model checkpoints
- operating system files

---

## main.py

Acts as the primary entry point for executing the machine learning pipeline.

Responsibilities may include:

- Loading configuration
- Running preprocessing
- Training models
- Generating predictions
- Saving outputs

---

# 5. Folder Descriptions

---

## artifacts/

### Purpose

Stores all generated outputs produced during project execution.

Typical contents include:

- trained models
- encoders
- scalers
- feature transformers
- prediction outputs
- serialized pipelines

Artifacts are generated automatically and should never contain manually edited files.

---

## configs/

### Purpose

Stores project configuration files.

Examples:

- model parameters
- feature lists
- file paths
- logging configuration
- experiment settings

Separating configuration from code makes the project easier to maintain.

---

## data/

### Purpose

Stores all datasets used throughout the project.

The data directory is divided into multiple stages.

---

### raw/

Contains the original dataset exactly as received.

Characteristics:

- Never modified
- Read-only
- Source of truth

---

### interim/

Contains partially cleaned datasets.

Examples:

- missing values handled
- inconsistent formatting corrected
- preliminary preprocessing

---

### processed/

Contains cleaned and feature-engineered datasets that are ready for machine learning and business analytics.

Typical files include:

- cleaned_manufacturing_data.csv
- engineered_features.csv
- model_ready_dataset.csv

These datasets are used during model training, evaluation, dashboard development, and business insight generation.

---

### external/

Stores data collected from external sources.

Examples:

- benchmark datasets
- industry reference data
- supplementary information

---

## docs/

### Purpose

Contains all project documentation.

Examples:

- Project Overview
- Business Problem
- Folder Structure
- Tech Stack
- Development Notes
- Future Scope

Good documentation improves maintainability and interview readiness.

---

## models/

### Purpose

Stores finalized machine learning models.

Examples:

- Random Forest
- XGBoost
- LightGBM
- CatBoost
- Stacking Ensemble

Only production-ready or finalized models should be stored here.

---

## notebooks/

### Purpose

Contains Jupyter notebooks used throughout development.

Typical notebooks include:

- 01_Business_Understanding.ipynb
- 02_Data_Understanding.ipynb
- 03_Data_Cleaning.ipynb
- 04_Exploratory_Data_Analysis.ipynb
- 05_Feature_Engineering.ipynb
- 06_Model_Development.ipynb
- 07_Model_Evaluation.ipynb
- 08_Explainable_AI.ipynb
- 09_Business_Insights.ipynb

Notebooks are primarily used for experimentation and analysis.

---

## reports/

### Purpose

Stores generated reports and visualizations.

---

### figures/

Contains:

- charts
- plots
- confusion matrices
- feature importance graphs
- SHAP plots

---

### tables/

Contains exported tabular data and analytical summaries.

Examples:

- EDA Summary Report
- Feature Engineering Report
- Model Evaluation Report
- Business Insights Report

---

## src/

### Purpose

Contains reusable Python source code.

Unlike notebooks, source code is modular, reusable, and production-oriented.

---

### src/data/

Responsible for:

- data loading
- validation
- preprocessing

Example files:

- loader.py
- validator.py
- preprocessing.py

---

### src/features/

Responsible for feature engineering.

Tasks include:

- encoding
- scaling
- transformations
- feature selection

---

### src/models/

Responsible for:

- model training
- prediction
- evaluation
- hyperparameter tuning

---

### src/visualization/

Responsible for generating visualizations.

Examples:

- histograms
- boxplots
- correlation heatmaps
- ROC curves

---

### src/utils/

Contains utility functions.

Examples:

- helper functions
- logging
- common constants
- file operations

---

### src/pipeline/

Coordinates the complete machine learning workflow.

Typical sequence:

- Load manufacturing dataset
- Validate data
- Clean data
- Engineer features
- Train models
- Evaluate models
- Generate business insights
- Save artifacts

---

## streamlit/

### Purpose

Contains the interactive web application.

Responsibilities:

- Manufacturing Dashboard
- Quality Analytics Dashboard
- Business Insights Dashboard
- Model Prediction Interface
- KPI Monitoring
- Interactive Visualizations

This folder provides the front-end through which users interact with the trained model.

---

## tests/

### Purpose

Contains automated tests.

Examples:

- preprocessing tests
- feature engineering tests
- model prediction tests
- utility function tests

Testing ensures project reliability and helps prevent regressions.

---

# 6. Detailed Directory Breakdown

FactoryGuard_AI/
│
├── artifacts/          → Generated ML outputs
├── configs/            → Configuration files
├── data/
│   ├── raw/            → Original datasets
│   ├── interim/        → Partially cleaned datasets
│   ├── processed/      → Model-ready datasets
│   └── external/       → External datasets
│
├── docs/               → Documentation
├── models/             → Final trained models
├── notebooks/          → Jupyter notebooks
├── reports/
│   ├── figures/        → Images & visualizations
│   └── tables/         → Tabular summary reports
│
├── src/
│   ├── data/           → Data loading & validation
│   ├── features/       → Feature engineering
│   ├── models/         → Model development
│   ├── visualization/  → Charts & graphs
│   ├── utils/          → Helper functions
│   └── pipeline/       → End-to-end pipeline
│
├── streamlit/          → Dashboard application
├── tests/              → Unit tests
│
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
└── main.py

---

# 7. Data Flow Across the Project

The movement of data through the project follows a structured pipeline.

Manufacturing Dataset
        │
        ▼
Data Validation
        │
        ▼
Data Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
Quality Analytics Dataset
        │
        ▼
Machine Learning Models
        │
        ▼
Model Evaluation
        │
        ▼
Business Insights
        │
        ▼
Quality Intelligence Dashboard
        │
        ▼
Manufacturing Decision Support

This flow ensures every stage has a clearly defined input and output.

---

# 8. Project Architecture

Business Understanding
        │
        ▼
Manufacturing Data Collection
        │
        ▼
Data Preparation
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Feature Engineering
        │
        ▼
Machine Learning Models
        │
        ▼
Model Evaluation
        │
        ▼
Business Insights
        │
        ▼
Explainable AI
        │
        ▼
Streamlit Dashboard
        │
        ▼
Manufacturing Quality Decision Support

Each stage builds upon the previous one, creating a complete end-to-end machine learning workflow.

---

# 9. Development Guidelines

To maintain consistency throughout the project:

- Keep notebooks focused on experimentation.
- Move reusable logic into the src/ directory.
- Never modify files in data/raw/.
- Save trained models in models/ or artifacts/.
- Store generated visualizations in reports/figures/.
- Update documentation whenever the project changes.
- Use meaningful file and folder names.

These guidelines help maintain a clean and professional repository.

---

# 10. Best Practices

The FactoryGuard AI repository follows several software engineering best practices.

- Modular code organization
- Separation of concerns
- Reusable functions
- Configuration-driven development
- Version control using Git
- Comprehensive documentation
- Reproducible workflows
- Clear project hierarchy

Following these principles makes the project easier to understand, extend, and deploy.

---

# 11. Folder Responsibilities

| Folder | Primary Responsibility |
|---|---|
| artifacts/ | Saved models, encoders, transformers and generated outputs |
| configs/ | Project configuration and parameters |
| data/ | Manufacturing datasets across different processing stages |
| docs/ | Business and technical documentation |
| models/ | Final trained machine learning models |
| notebooks/ | Research, experimentation and analysis |
| reports/ | Figures, tables and business reports |
| src/ | Modular reusable source code |
| streamlit/ | Manufacturing Quality Intelligence Dashboard |
| tests/ | Testing and validation scripts |

Each folder has a single, well-defined purpose, reducing complexity and improving maintainability.

---

# 12. Conclusion

A well-designed repository structure is fundamental to developing scalable and maintainable machine learning solutions. By organizing datasets, source code, documentation, reports, models, and deployment assets into dedicated directories, FactoryGuard AI becomes easier to understand, extend, and maintain throughout its lifecycle.

The modular architecture adopted in this project supports every stage of the Manufacturing Quality Decision System—from business understanding and data preparation to machine learning, business analytics, explainable AI, dashboard development, and deployment. This organization follows industry best practices and provides a strong foundation for future enhancements such as MLOps, cloud deployment, IoT integration, and enterprise-scale manufacturing analytics.
# FactoryGuard AI — Intelligent Manufacturing Quality Decision System

An end-to-end machine learning decision-support system for identifying potentially problematic manufacturing cases from structured manufacturing and process data.

## 🚀 Live Demo

**Streamlit App:** Coming soon

**GitHub Repository:**  
https://github.com/Bhardwaj-Arin/FactoryGuard-AI-Intelligent-Manufacturing-Quality-Decision-System

---

## 📌 Project Overview

FactoryGuard AI is an end-to-end machine learning classification project designed to screen manufacturing observations and identify cases that may require further quality inspection.

The system takes manufacturing and process-related information such as:

- Plant
- Production line
- Shift
- Machine information
- Machine age
- Material grade
- Temperature
- Humidity
- Process speed
- Inspection method
- Defect type
- Defect severity
- Rework decision
- Cycle time
- Energy consumption
- Production cost
- Event timestamp

and uses a trained Random Forest classification model to estimate the probability of each class.

The project is designed as a **screening and decision-support system**, rather than a fully automated quality-control system.

---

## 🎯 Objective

The primary objective is to build an end-to-end machine learning system capable of identifying potentially problematic manufacturing observations while considering the consequences of false positives and false negatives.

The target variable is:

```text
final_pass
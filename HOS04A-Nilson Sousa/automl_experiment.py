"""
automl_experiment.py
---------------------
A lightweight AutoML simulation.

"AutoML" here means: instead of a human manually picking one algorithm,
we automatically train several candidate models, score each one with
cross-validation, and select the best performer without further
human intervention. This is the core idea behind AutoML frameworks
(e.g., Auto-sklearn, TPOT, H2O AutoML) — just scaled down for a classroom
exercise.

Output:
- model/best_model.pkl          -> the winning model, saved for deployment
- model/performance_log.csv     -> an audit trail of every model tried
"""

import os
import csv
from datetime import datetime

import joblib
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

MODEL_DIR = "model"
BEST_MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")
LOG_PATH = os.path.join(MODEL_DIR, "performance_log.csv")


def ensure_model_dir():
    os.makedirs(MODEL_DIR, exist_ok=True)


def log_result(row, header):
    """Append a row to the performance log, writing the header once."""
    file_exists = os.path.isfile(LOG_PATH)
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)


def run_automl():
    ensure_model_dir()

    # 1. Load data (breast cancer dataset: binary classification, built into sklearn)
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )

    # 2. Candidate models — this is the "search space" AutoML explores
    candidates = {
        "LogisticRegression": LogisticRegression(max_iter=5000),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "GradientBoosting": GradientBoostingClassifier(random_state=42),
        "KNeighbors": KNeighborsClassifier(n_neighbors=5),
        "SVM": SVC(probability=True, random_state=42),
    }

    header = [
        "timestamp", "cycle", "model_name",
        "cv_mean_accuracy", "cv_std_accuracy", "test_accuracy", "notes"
    ]

    best_name = None
    best_model = None
    best_cv_score = -np.inf
    best_test_score = None

    print("Running AutoML search across candidate models...\n")

    for name, model in candidates.items():
        # 3. Evaluate each candidate with 5-fold cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
        mean_cv = cv_scores.mean()
        std_cv = cv_scores.std()

        # Fit on full training set to get a held-out test score too
        model.fit(X_train, y_train)
        test_score = model.score(X_test, y_test)

        print(f"{name:18s} | CV acc: {mean_cv:.4f} (+/- {std_cv:.4f}) | Test acc: {test_score:.4f}")

        log_result(
            [datetime.now().isoformat(timespec="seconds"), "automl_initial",
             name, f"{mean_cv:.4f}", f"{std_cv:.4f}", f"{test_score:.4f}", "candidate evaluated"],
            header,
        )

        # 4. Track the best performer by cross-validation accuracy
        if mean_cv > best_cv_score:
            best_cv_score = mean_cv
            best_test_score = test_score
            best_name = name
            best_model = model

    # 5. Save the winning model for deployment / for kaizen_cycle.py to build on
    joblib.dump(best_model, BEST_MODEL_PATH)

    log_result(
        [datetime.now().isoformat(timespec="seconds"), "automl_initial",
         best_name, f"{best_cv_score:.4f}", "-", f"{best_test_score:.4f}",
         "SELECTED as best_model.pkl"],
        header,
    )

    print(f"\nBest model: {best_name} (CV acc: {best_cv_score:.4f}, Test acc: {best_test_score:.4f})")
    print(f"Saved to {BEST_MODEL_PATH}")


if __name__ == "__main__":
    run_automl()

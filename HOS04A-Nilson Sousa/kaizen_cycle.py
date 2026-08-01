"""
kaizen_cycle.py
----------------
Simulates one cycle of KaizenML: "kaizen" (改善) means continuous,
incremental improvement. In an MLOps context, that means:

  1. New data arrives (or the world drifts).
  2. We retrain a candidate model on the updated data.
  3. We compare it against the currently deployed model.
  4. We ONLY replace the deployed model if the candidate is actually better.

This keeps a production model improving over time without ever
regressing in quality — the model only moves forward.

Run this file multiple times to simulate multiple improvement cycles.
Each run adds a new row to model/performance_log.csv, and prints
whether the deployed model was replaced.
"""

import os
import csv
import random
from datetime import datetime

import joblib
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

MODEL_DIR = "model"
BEST_MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")
LOG_PATH = os.path.join(MODEL_DIR, "performance_log.csv")

HEADER = [
    "timestamp", "cycle", "model_name",
    "cv_mean_accuracy", "cv_std_accuracy", "test_accuracy", "notes"
]


def log_result(row):
    file_exists = os.path.isfile(LOG_PATH)
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(HEADER)
        writer.writerow(row)


def simulate_new_data(random_state):
    """
    Simulate 'new data arriving' by re-splitting the dataset with a
    different random seed each run (stand-in for a fresh data pull /
    natural data drift in a real pipeline).
    """
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


def get_current_model_test_score(X_test, y_test):
    """Load the currently deployed model and score it on this cycle's test data."""
    if not os.path.isfile(BEST_MODEL_PATH):
        return None, None
    current_model = joblib.load(BEST_MODEL_PATH)
    return current_model, current_model.score(X_test, y_test)


def run_kaizen_cycle():
    if not os.path.isfile(BEST_MODEL_PATH):
        print("No existing best_model.pkl found. Run automl_experiment.py first.")
        return

    # A different seed each run stands in for "new data" / hyperparameter tuning
    random_state = random.randint(0, 10_000)
    X_train, X_test, y_train, y_test = simulate_new_data(random_state)

    # 1. Score the CURRENTLY deployed model on this cycle's data
    current_model, current_score = get_current_model_test_score(X_test, y_test)

    # 2. Train a CANDIDATE model — slightly different hyperparameters,
    #    representing an incremental tuning step (the "kaizen" tweak)
    candidate_n_estimators = random.choice([80, 100, 120, 150, 200])
    candidate_max_depth = random.choice([None, 5, 10, 15])
    candidate_model = RandomForestClassifier(
        n_estimators=candidate_n_estimators,
        max_depth=candidate_max_depth,
        random_state=random_state,
    )
    candidate_model.fit(X_train, y_train)
    candidate_score = candidate_model.score(X_test, y_test)

    print(f"Deployed model test accuracy:  {current_score:.4f}")
    print(f"Candidate model test accuracy: {candidate_score:.4f} "
          f"(n_estimators={candidate_n_estimators}, max_depth={candidate_max_depth})")

    timestamp = datetime.now().isoformat(timespec="seconds")

    # 3. Only replace the deployed model if the candidate genuinely improves on it
    if candidate_score > current_score:
        joblib.dump(candidate_model, BEST_MODEL_PATH)
        print("Candidate model IMPROVED performance — replacing best_model.pkl")
        log_result([
            timestamp, "kaizen", "RandomForest_candidate",
            "-", "-", f"{candidate_score:.4f}",
            f"IMPROVED (+{candidate_score - current_score:.4f}) — replaced deployed model"
        ])
    else:
        print("Candidate model did NOT improve performance — keeping current deployed model")
        log_result([
            timestamp, "kaizen", "RandomForest_candidate",
            "-", "-", f"{candidate_score:.4f}",
            f"no improvement ({candidate_score - current_score:+.4f}) — kept previous model"
        ])


if __name__ == "__main__":
    run_kaizen_cycle()

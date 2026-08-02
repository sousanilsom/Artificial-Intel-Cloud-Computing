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

IMPROVEMENT_LOG_PATH = os.path.join(MODEL_DIR, "improvement_log.csv")

HEADER = [
    "timestamp", "cycle", "model_name",
    "cv_mean_accuracy", "cv_std_accuracy", "test_accuracy", "notes"
]

IMPROVEMENT_HEADER = [
    "timestamp", "previous_test_accuracy", "new_test_accuracy",
    "accuracy_gain", "n_estimators", "max_depth"
]


def log_result(row):
    file_exists = os.path.isfile(LOG_PATH)
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(HEADER)
        writer.writerow(row)


def log_improvement(timestamp, previous_score, new_score, n_estimators, max_depth):
    file_exists = os.path.isfile(IMPROVEMENT_LOG_PATH)
    with open(IMPROVEMENT_LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(IMPROVEMENT_HEADER)
        writer.writerow([
            timestamp,
            f"{previous_score:.4f}",
            f"{new_score:.4f}",
            f"{new_score - previous_score:+.4f}",
            n_estimators,
            max_depth,
        ])


EVAL_RANDOM_STATE = 42


def get_fixed_eval_split():
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=EVAL_RANDOM_STATE
    )
    return X_train, X_test, y_train, y_test


def simulate_new_training_data(X_train, y_train, random_state):
    rng = np.random.RandomState(random_state)
    n = X_train.shape[0]
    idx = rng.choice(n, size=n, replace=True)
    return X_train[idx], y_train[idx]


def get_current_model_test_score(X_test, y_test):
    if not os.path.isfile(BEST_MODEL_PATH):
        return None, None
    current_model = joblib.load(BEST_MODEL_PATH)
    return current_model, current_model.score(X_test, y_test)


def run_kaizen_cycle():
    if not os.path.isfile(BEST_MODEL_PATH):
        print("No existing best_model.pkl found. Run automl_experiment.py first.")
        return

    X_train_pool, X_test, y_train_pool, y_test = get_fixed_eval_split()

    random_state = random.randint(0, 10_000)
    X_train, y_train = simulate_new_training_data(X_train_pool, y_train_pool, random_state)

    current_model, current_score = get_current_model_test_score(X_test, y_test)

    candidate_configs = [
        (random.choice([80, 100, 120, 150, 200, 250]), random.choice([None, 5, 8, 10, 15, 20]))
        for _ in range(5)
    ]

    best_candidate_model = None
    best_candidate_score = -1
    best_candidate_n_estimators = None
    best_candidate_max_depth = None

    for n_estimators, max_depth in candidate_configs:
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
        )
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        print(f"  tried n_estimators={n_estimators}, max_depth={max_depth} -> acc={score:.4f}")
        if score > best_candidate_score:
            best_candidate_score = score
            best_candidate_model = model
            best_candidate_n_estimators = n_estimators
            best_candidate_max_depth = max_depth

    candidate_model = best_candidate_model
    candidate_score = best_candidate_score
    candidate_n_estimators = best_candidate_n_estimators
    candidate_max_depth = best_candidate_max_depth

    print(f"Deployed model test accuracy:  {current_score:.4f}")
    print(f"Best candidate this cycle:     {candidate_score:.4f} "
          f"(n_estimators={candidate_n_estimators}, max_depth={candidate_max_depth})")

    timestamp = datetime.now().isoformat(timespec="seconds")
    readable_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Old Accuracy: {current_score:.3f} | New Accuracy: {candidate_score:.3f}")

    if candidate_score > current_score:
        joblib.dump(candidate_model, BEST_MODEL_PATH)

        print("New model is better! Replacing the previous one.")
        print(f"Log updated at {readable_time}")
        print(f"Log saved to {LOG_PATH}")

        log_improvement(
            timestamp, current_score, candidate_score,
            candidate_n_estimators, candidate_max_depth
        )
        log_result([
            timestamp, "kaizen", "RandomForest_candidate",
            "-", "-", f"{candidate_score:.4f}",
            f"IMPROVED (+{candidate_score - current_score:.4f}) — replaced deployed model at {readable_time}"
        ])
    else:
        print("New model not better. Keeping the previous one.")
        print(f"Log updated at {readable_time}")
        print(f"Log saved to {LOG_PATH}")
        log_result([
            timestamp, "kaizen", "RandomForest_candidate",
            "-", "-", f"{candidate_score:.4f}",
            f"no improvement ({candidate_score - current_score:+.4f}) — kept previous model"
        ])


if __name__ == "__main__":
    run_kaizen_cycle()

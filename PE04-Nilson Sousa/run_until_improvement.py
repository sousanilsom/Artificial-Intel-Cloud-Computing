"""
run_until_improvement.py
-------------------------
Runs kaizen_cycle.py's run_kaizen_cycle() repeatedly until an
improvement is detected (best_model.pkl gets replaced), or until
max_attempts is reached. Saves you from manually re-running the
script by hand dozens of times.

Usage:
    python3 run_until_improvement.py
"""

import os
from kaizen_cycle import run_kaizen_cycle, IMPROVEMENT_LOG_PATH

MAX_ATTEMPTS = 40

before_exists = os.path.isfile(IMPROVEMENT_LOG_PATH)
before_size = os.path.getsize(IMPROVEMENT_LOG_PATH) if before_exists else 0

for attempt in range(1, MAX_ATTEMPTS + 1):
    print(f"\n--- Attempt {attempt}/{MAX_ATTEMPTS} ---")
    run_kaizen_cycle()

    after_exists = os.path.isfile(IMPROVEMENT_LOG_PATH)
    after_size = os.path.getsize(IMPROVEMENT_LOG_PATH) if after_exists else 0

    if after_exists and after_size > before_size:
        print(f"\nImprovement found on attempt {attempt}. Stopping.")
        break
else:
    print(f"\nNo improvement found after {MAX_ATTEMPTS} attempts. "
          f"The deployed model may already be near its ceiling for this dataset.")
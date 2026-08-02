# HOS03A - Continuous Delivery for Machine Learning Models

**AI 510 Artificial Intelligence of Cloud Computing**
An MLOps Foundation Exercise

Nilson Sousa

## Steps

1. Created the folder structure (`app.py`, `train_model.py`, `requirements.txt`, `Dockerfile`, `.dockerignore`, `model/`).
2. `train_model.py` trains a `RandomForestClassifier` on the Iris dataset and saves it to `model/iris_model.pkl`.
3. `app.py` is a Flask API exposing `/` (status) and `/predict` (POST, returns `{"prediction": <int>}`).
4. `requirements.txt` lists Flask, scikit-learn, joblib, and numpy.
5. `Dockerfile` builds a `python:3.8-slim` image, installs dependencies, and runs `app.py`.
6. `.dockerignore` excludes `__pycache__/`, `*.pyc`, `*.pkl`, and `.env` from the build context.
7. The CD (Continuous Delivery) workflow installs dependencies, retrains the model, launches the Flask app, and runs a test `/predict` request on every push to `main`.

## GitHub Actions location note

GitHub only picks up workflow YAML files from the **repository root's**
`.github/workflows/` directory, not from a subfolder inside an assignment
directory. Since this repo hosts multiple assignments in subfolders, the
functional workflow for this exercise lives at the repo root as
[`.github/workflows/hos03a_cd_pipeline.yml`](../.github/workflows/hos03a_cd_pipeline.yml)
(named distinctly so it doesn't collide with other assignments' workflows),
and `cd`s into `HOS03A-Nilson Sousa/` before each step.

## Verified locally

Ran the exact sequence the CD pipeline runs:
```bash
pip install -r requirements.txt
python train_model.py
python app.py &
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
# {"prediction": 0}
```

After pushing, check the **Actions** tab on GitHub to confirm the
`HOS03A - CD ML Model Deployment` workflow runs successfully (green check).
If the Actions tab isn't visible or the workflow doesn't trigger, enable
Actions under **Settings > Actions > General**.

## Files

- `train_model.py` - trains and saves the Iris classifier
- `app.py` - Flask API (`/` and `/predict`)
- `requirements.txt` - Flask, scikit-learn, joblib, numpy
- `Dockerfile` - container build definition
- `.dockerignore` - excludes `__pycache__`, `*.pyc`, `*.pkl`, `.env`
- `model/iris_model.pkl` - trained model artifact
- `../.github/workflows/hos03a_cd_pipeline.yml` - the CD workflow (repo root, see note above)

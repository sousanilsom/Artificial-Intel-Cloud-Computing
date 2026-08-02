# HOS02A - Containerize ML Model API with Flask and Docker

**AI 510 Artificial Intelligence of Cloud Computing**
An MLOps Foundation Exercise

Nilson Sousa

## Steps

1. Created a `model/` folder and a Python virtual environment.
2. Created `requirements.txt` (Flask, scikit-learn, joblib, numpy) and installed the dependencies.
3. Created `train_model.py`, which trains a `RandomForestClassifier` on the Iris dataset and saves it to `model/iris_model.pkl`.
4. Created `app.py`, a Flask API with:
   - `/` - basic status page
   - `/health` - health check
   - `/metadata` - model info (type, feature names, target classes)
   - `/predict` - returns the predicted class and species name
5. Created `.dockerignore` to keep `.venv`, `__pycache__`, and `*.pyc` out of the image.
6. Created a `Dockerfile` that installs dependencies and runs `app.py`.
7. Built the image and ran the container:
   ```bash
   docker build -t iris-api .
   docker run -p 5000:5000 iris-api
   ```
8. Verified the containerized API:
   ```bash
   curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
   ```
   Response: `{"prediction": 0, "species": "setosa"}`

## Verified locally

Built and ran the image with Docker (via colima on macOS), remapped to host port 5050
locally only because macOS AirPlay Receiver occupies port 5000 on this machine
(the Dockerfile/image itself still expose port 5000, matching the assignment):

```
GET  /            -> <h3>Iris Prediction API is Running</h3>
GET  /health       -> {"status": "OK"}
GET  /metadata     -> {"model_type": "RandomForestClassifier", "features": [...], "target_classes": ["setosa", "versicolor", "virginica"]}
POST /predict      -> {"prediction": 0, "species": "setosa"}
```

## Files

- `train_model.py` - trains and saves the Iris classifier
- `app.py` - Flask API (status, health, metadata, predict routes)
- `requirements.txt` - Flask, scikit-learn, joblib, numpy
- `Dockerfile` - container build definition
- `.dockerignore` - excludes `.venv`, `__pycache__`, `*.pyc` from the image
- `model/iris_model.pkl` - trained model artifact

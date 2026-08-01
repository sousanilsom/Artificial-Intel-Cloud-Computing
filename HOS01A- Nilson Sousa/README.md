# HOS01A - Build & Serve Your First Machine Learning Model with Flask

**AI 510 Artificial Intelligence of Cloud Computing**
An MLOps Foundation Exercise

Nilson Sousa

## Steps

1. Installed Flask:
   ```
   pip install Flask
   ```

2. Created `app.py` with a minimal Flask "Hello World" app to confirm the environment worked:
   ```python
   from flask import Flask

   app = Flask(__name__)

   @app.route('/')
   def hello_world():
       return "Hello World"

   if __name__ == '__main__':
       app.run()
   ```
   Ran it and confirmed the page loaded in the browser.

3. Created `train_model.py`, which loads the Iris dataset, trains a `RandomForestClassifier`, and saves it to `model/iris_model.pkl` with `joblib`.

4. Revised `app.py` to load the saved model and expose a `/predict` endpoint that accepts JSON features and returns a prediction.

5. Installed the remaining dependencies:
   ```
   pip install scikit-learn joblib numpy
   ```

6. Ran `train_model.py` to produce `model/iris_model.pkl`, then started `app.py` and verified the API:
   ```
   curl -X POST http://127.0.0.1:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
   ```
   Response: `{"prediction": 0}`

## Files

- `train_model.py` - trains and saves the Iris classifier
- `app.py` - Flask API serving the trained model
- `requirements.txt` - Flask, scikit-learn, joblib, numpy
- `model/iris_model.pkl` - trained model artifact

## Reflection

Running this locally, "serving" the model is just a Flask process reading a `.pkl` file off disk and responding to requests on `127.0.0.1`. The MLOps ideas carry over directly to the cloud: the same `app.py` and `model/iris_model.pkl` can be packaged (e.g., in a container) and deployed behind a real load balancer, with the training step (`train_model.py`) becoming a separate, repeatable pipeline job instead of a manual script run. What changes in the cloud is everything around the model - versioning the artifact, automating retraining, monitoring prediction traffic, and scaling the API - rather than the core train/save/serve pattern itself, which is exactly what this exercise walks through end to end.

from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("model/iris_model.pkl")
species = {0: "setosa", 1: "versicolor", 2: "virginica"}

@app.route("/")
def home():
    return "<h3>Iris Prediction API is Running</h3>"

@app.route("/health")
def health():
    return jsonify({"status": "OK"})

@app.route("/metadata")
def metadata():
    return jsonify({
        "model_type": "RandomForestClassifier",
        "features": ["sepal length", "sepal width", "petal length", "petal width"],
        "target_classes": list(species.values())
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        features = np.array(data["features"]).reshape(1, -1)
        prediction = model.predict(features)[0]
        return jsonify({"prediction": int(prediction), "species": species[prediction]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

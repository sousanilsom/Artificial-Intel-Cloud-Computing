from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model
model = joblib.load('model.pkl')

# Map numeric labels to human-readable species names
species_map = {0: "setosa", 1: "versicolor", 2: "virginica"}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)
    predicted_label = int(prediction[0])
    species_name = species_map[predicted_label]
    return jsonify({'prediction': predicted_label, 'species': species_name})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
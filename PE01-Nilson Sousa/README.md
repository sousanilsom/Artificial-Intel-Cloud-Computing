# PE01 - Programming Exercise

**AI 510 Artificial Intelligence of Cloud Computing**

Nilson Sousa

## Task

Modify the `/predict` route from HOS01A so the response includes both the
numeric class label and the human-readable species name, instead of just:
```json
{"prediction": 0}
```

## Change

Added a `species_map` dictionary and used it to look up the species name
from the predicted label:

```python
species_map = {0: "setosa", 1: "versicolor", 2: "virginica"}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)
    label = int(prediction[0])
    return jsonify({'prediction': label, 'species': species_map[label]})
```

## Verified

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
# {"prediction": 0, "species": "setosa"}

curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [6.7, 3.0, 5.2, 2.3]}'
# {"prediction": 2, "species": "virginica"}
```

## Files

- `train_model.py` - trains and saves the Iris classifier
- `app.py` - Flask API with the updated `/predict` route
- `requirements.txt` - Flask, scikit-learn, joblib, numpy
- `model/iris_model.pkl` - trained model artifact

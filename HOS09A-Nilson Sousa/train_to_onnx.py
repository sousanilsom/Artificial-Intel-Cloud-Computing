from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnxruntime as rt
import joblib
import numpy as np
import os

# Step 1: Train a simple model
iris = load_iris()
X, y = iris.data, iris.target
model = LogisticRegression(max_iter=200)
model.fit(X, y)

# Step 2: Save native Scikit-learn model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/iris_model.pkl")

# Step 3: Convert to ONNX format
initial_type = [("input", FloatTensorType([None, 4]))]
onnx_model = convert_sklearn(model, initial_types=initial_type)
with open("models/iris_model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

# Step 4: Load ONNX model for inference
sess = rt.InferenceSession("models/iris_model.onnx")
input_name = sess.get_inputs()[0].name

# Step 5: Compare predictions for 3 samples
samples = [0, 50, 100]  # One sample from each Iris class
print("\n=== Prediction Comparison (Scikit-learn vs ONNX) ===")
for idx in samples:
    input_data = X[idx:idx+1].astype(np.float32)
    skl_pred = model.predict(input_data)
    onnx_pred = sess.run(None, {input_name: input_data})[0]
    print(f"Sample {idx}: sklearn -> {skl_pred[0]}, onnx -> {int(onnx_pred[0])}")

print("\n Interoperability test completed successfully!")

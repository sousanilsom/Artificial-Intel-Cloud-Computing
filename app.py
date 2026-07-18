import os
import sys
import platform
from flask import Flask, jsonify

# Initializing the Flask application instance
app = Flask(__name__)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Placeholder for your machine learning prediction pipeline."""
    return jsonify({"status": "success", "message": "Prediction endpoint operational"})

@app.route('/metadata', methods=['GET'])
def metadata():
    """Placeholder for your model architecture or data pipeline definitions."""
    return jsonify({"model_name": "Basic Classifier", "version": "1.0.0"})

# ==========================================
# NEW REQUIRED PE02 ROUTE
# ==========================================

# Import modules to check version metrics dynamically
import flask
import sklearn
import joblib

@app.route('/runtime', methods=['GET'])
def runtime_info():
    """
    Returns container runtime metadata including language environment,
    operating system platform, hostname, and specific dependency versions.
    """
    try:
        package_versions = {
            "flask": flask.__version__,
            "scikit-learn": sklearn.__version__,
            "joblib": joblib.__version__
        }
    except AttributeError:
        package_versions = {
            "flask": getattr(flask, '__version__', 'unknown'),
            "scikit-learn": getattr(sklearn, '__version__', 'unknown'),
            "joblib": getattr(joblib, '__version__', 'unknown')
        }

    runtime_data = {
        "python_version": sys.version,
        "operating_system": platform.platform(),
        "hostname": platform.node() or os.environ.get('HOSTNAME', 'unknown'),
        "dependencies": package_versions
    }
    
    return jsonify(runtime_data)

if __name__ == '__main__':
    # Run the internal web server on development port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
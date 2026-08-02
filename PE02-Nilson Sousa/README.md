# PE02 - Programming Exercise

**AI 510 Artificial Intelligence of Cloud Computing**

Nilson Sousa

## Task

Improve HOS02 by adding a new `/runtime` route (without changing or
removing `/predict` or `/metadata`) that returns container runtime info:
Python version, OS platform, hostname, and installed versions of Flask,
scikit-learn, and joblib.

## Change

Appended new imports and the new route below the existing HOS02 code in
`app.py`, without touching the existing routes:

```python
# --- PE02: new imports and route appended below existing code ---
import platform
import socket
from importlib.metadata import version

@app.route("/runtime")
def runtime():
    return jsonify({
        "python_version": platform.python_version(),
        "platform": platform.system(),
        "hostname": socket.gethostname(),
        "packages": {
            "flask": version("flask"),
            "scikit-learn": version("scikit-learn"),
            "joblib": version("joblib")
        }
    })
```

Note: this block is placed after the existing routes but *before* the
`if __name__ == "__main__":` block at the very end of the file. Flask
registers routes as the module executes top-to-bottom, and the last
line calls `app.run()`, which blocks — so any route defined after that
line would never actually register. Keeping the new route just above
it is the only way to both append it "below the existing code" and
have it actually work.

## Verified

Built and ran the Docker image (`docker build -t iris-api-pe02 .` /
`docker run -p 5000:5000 iris-api-pe02`):

```bash
curl http://localhost:5000/runtime
# {"hostname": "...", "packages": {"flask": "3.1.3", "joblib": "1.5.3", "scikit-learn": "1.9.0"}, "platform": "Linux", "python_version": "3.11.15"}

curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
# {"prediction": 0, "species": "setosa"}  <- unchanged, still works

curl http://localhost:5000/metadata
# unchanged, still works
```

## Files

- `train_model.py` - trains and saves the Iris classifier
- `app.py` - Flask API with the new `/runtime` route appended
- `requirements.txt` - Flask, scikit-learn, joblib, numpy
- `Dockerfile` - container build definition
- `.dockerignore` - excludes `.venv`, `__pycache__`, `*.pyc` from the image
- `model/iris_model.pkl` - trained model artifact

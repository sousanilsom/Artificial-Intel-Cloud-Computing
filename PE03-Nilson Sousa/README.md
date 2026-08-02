# PE03 - Programming Exercise

**AI 510 Artificial Intelligence of Cloud Computing**

Nilson Sousa

## Task

Improve HOS03 by adding a "Validate Model Output" step to the GitHub
Actions workflow: an integration test that calls the deployed Flask
API's `/predict` endpoint and checks the response actually contains a
`prediction`, failing the build if it doesn't.

## Change

Built on the HOS03A files (`app.py`, `train_model.py`, `requirements.txt`,
`Dockerfile`, `.dockerignore`) and added a new workflow at the repo root,
[`.github/workflows/pe03_cd_pipeline.yml`](../.github/workflows/pe03_cd_pipeline.yml)
(GitHub only recognizes workflows there, not in a subfolder — same reason
HOS03A's workflow also lives at the repo root). It runs the same
install/train/serve steps as HOS03A, plus a new validation step:

```yaml
- name: Validate Model Output
  run: |
    response=$(curl -s -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"features": [6.7, 3.1, 4.4, 1.4]}')
    echo "$response"
    if [[ "$response" == *"prediction"* ]]; then
      echo "Model prediction check passed."
    else
      echo "Model prediction check failed."
      exit 1
    fi
```

## Verified

Ran the same check locally before pushing:
```bash
python train_model.py
python app.py &
curl -s -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"features": [6.7, 3.1, 4.4, 1.4]}'
# {"prediction": 1}
# Model prediction check passed.
```

After pushing, confirmed on GitHub's **Actions** tab that the
`PE03 - CD ML Model Deployment` workflow run succeeded (green check),
with the "Validate Model Output" step showing `Model prediction check
passed.` — see the screenshot submitted alongside this folder.

## Files

- `train_model.py` - trains and saves the Iris classifier
- `app.py` - Flask API (`/` and `/predict`)
- `requirements.txt` - Flask, scikit-learn, joblib, numpy
- `Dockerfile` - container build definition
- `.dockerignore` - excludes `__pycache__`, `*.pyc`, `*.pkl`, `.env`
- `model/iris_model.pkl` - trained model artifact
- `../.github/workflows/pe03_cd_pipeline.yml` - the CD workflow with the new validation step (repo root, see note above)

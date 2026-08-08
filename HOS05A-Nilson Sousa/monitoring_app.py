import time
import csv
import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
LOG_DIR = "logs"
CSV_LOG_FILE = os.path.join(LOG_DIR, "request_log.csv")
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
  filename=APP_LOG_FILE,
  level=logging.INFO,
  format="%(asctime)s [%(levelname)s] %(message)s"
)

if not os.path.exists(CSV_LOG_FILE):
  with open(CSV_LOG_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "endpoint", "method", "status_code", "latency_ms"])

request_stats = {
  "total_requests": 0,
  "total_latency_ms": 0.0,
  "errors": 0,
  "start_time": time.time()
}


def log_request(endpoint, method, status_code, latency_ms):
  request_stats["total_requests"] += 1
  request_stats["total_latency_ms"] += latency_ms
  if status_code >= 400:
    request_stats["errors"] += 1

  timestamp = datetime.utcnow().isoformat()
  with open(CSV_LOG_FILE, "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([timestamp, endpoint, method, status_code, f"{latency_ms:.2f}"])
    logging.info(f"{method} {endpoint} -> {status_code} ({latency_ms:.2f} ms)")


@app.before_request
def start_timer():
  request.start_time = time.time()


@app.after_request
def record_request(response):
  latency_ms = (time.time() - getattr(request, "start_time", time.time())) * 1000
  log_request(request.path, request.method, response.status_code, latency_ms)
  return response


@app.route("/predict", methods=["POST"])
def predict():
  data = request.get_json(force=True, silent=True) or {}
  features = data.get("features", [])
  prediction = sum(features) % 3 if features else 0
  return jsonify({"prediction": prediction})


@app.route("/monitor", methods=["GET"])
def monitor():
  avg_latency = (
    request_stats["total_latency_ms"] / request_stats["total_requests"]
    if request_stats["total_requests"] > 0 else 0
  )
  return jsonify({
    "total_requests": request_stats["total_requests"],
    "total_errors": request_stats["errors"],
    "average_latency_ms": round(avg_latency, 2)
  })


@app.route("/health", methods=["GET"])
def health():
  uptime_seconds = time.time() - request_stats["start_time"]
  status = "healthy" if request_stats["errors"] == 0 else "degraded"
  return jsonify({
    "status": status,
    "uptime_seconds": round(uptime_seconds, 2),
    "total_requests": request_stats["total_requests"]
  })


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)

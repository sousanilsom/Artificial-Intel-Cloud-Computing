import time
import csv
import os
from datetime import datetime
from flask import Flask, request, jsonify

# Configure logs directory
LOG_DIR = "logs"
CSV_LOG_FILE = os.path.join(LOG_DIR, "request_log.csv")
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Create logs directory
os.makedirs(LOG_DIR, exist_ok=True)

# Initialize Flask app
app = Flask(__name__)

# Write CSV header
if not os.path.exists(CSV_LOG_FILE):
    with open(CSV_LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "endpoint", "method", "status_code", "latency_ms"])

# Request stats
request_stats = {
    "total_requests": 0,
    "total_latency_ms": 0.0,
    "errors": 0,
    "start_time": time.time()
}

def write_log(level, message):
    """Write directly to app.log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    log_entry = f"{timestamp} [{level}] {message}\n"
    with open(APP_LOG_FILE, "a") as f:
        f.write(log_entry)
    print(log_entry.strip())

def log_request(endpoint, method, status_code, latency_ms):
    """Log request to CSV and app.log"""
    request_stats["total_requests"] += 1
    request_stats["total_latency_ms"] += latency_ms
    
    if status_code >= 400:
        request_stats["errors"] += 1
    
    timestamp = datetime.utcnow().isoformat()
    
    # Log to CSV
    with open(CSV_LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, endpoint, method, status_code, f"{latency_ms:.2f}"])
    
    # Log to file
    write_log("INFO", f"{method} {endpoint} -> {status_code} ({latency_ms:.2f} ms)")

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
    """Prediction endpoint with INPUT VALIDATION for PE05"""
    try:
        data = request.get_json(force=True, silent=True) or {}
        
        # VALIDATION: Check if features key exists
        if "features" not in data:
            write_log("ERROR", "Invalid input data. Missing 'features' key.")
            return jsonify({"error": "Invalid input data. Expected 'features' key."}), 400
        
        features = data.get("features")
        
        # VALIDATION: Check if features is a list
        if not isinstance(features, list):
            write_log("ERROR", f"Invalid input data. 'features' must be a list, got {type(features).__name__}.")
            return jsonify({"error": "Invalid input data. 'features' must be a list."}), 400
        
        # VALIDATION: Check if features has exactly 4 elements
        if len(features) != 4:
            write_log("ERROR", f"Invalid input data. 'features' must have exactly 4 values, got {len(features)}.")
            return jsonify({"error": "Invalid input data. Expected 'features' with 4 numeric values."}), 400
        
        # VALIDATION: Check if all features are numeric
        try:
            numeric_features = [float(f) for f in features]
        except (ValueError, TypeError):
            write_log("ERROR", f"Invalid input data. 'features' values must be numeric. Got: {features}")
            return jsonify({"error": "Invalid input data. All 'features' must be numeric values."}), 400
        
        # Perform prediction
        prediction = sum(numeric_features) % 3
        write_log("INFO", f"Successful prediction: {numeric_features} -> {prediction}")
        
        return jsonify({"prediction": prediction}), 200
        
    except Exception as e:
        write_log("ERROR", f"Error processing request: {str(e)}")
        return jsonify({"error": "Invalid input data."}), 400

@app.route("/monitor", methods=["GET"])
def monitor():
    """Return monitoring statistics"""
    avg_latency = (
        request_stats["total_latency_ms"] / request_stats["total_requests"]
        if request_stats["total_requests"] > 0
        else 0
    )
    
    return jsonify({
        "total_requests": request_stats["total_requests"],
        "total_errors": request_stats["errors"],
        "average_latency_ms": round(avg_latency, 2)
    })

@app.route("/health", methods=["GET"])
def health():
    """Return system health status"""
    uptime_seconds = time.time() - request_stats["start_time"]
    status = "healthy" if request_stats["errors"] == 0 else "degraded"
    
    return jsonify({
        "status": status,
        "uptime_seconds": round(uptime_seconds, 2),
        "total_requests": request_stats["total_requests"]
    })

if __name__ == "__main__":
    write_log("INFO", "Flask app starting on 0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)

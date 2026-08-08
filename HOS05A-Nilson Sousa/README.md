# HOS05A: Automating Monitoring & Logging in MLOps

## Overview
This hands-on skill lab demonstrates the implementation of monitoring and logging for a Flask-based ML API. The project creates a production-ready monitoring system that tracks inference requests, detects performance drift, and maintains comprehensive audit logs.

## Project Structure
```
HOS05A-Nilson Sousa/
├── monitoring_app.py      # Flask app with monitoring logic
├── requirements.txt       # Project dependencies
├── logs/                  # Directory for runtime logs
│   └── .gitkeep          # Ensures directory is tracked in Git
└── README.md             # This file
```

## Learning Outcomes
By completing this lab, you will:
- Implement model monitoring and logging for an ML API
- - Track inference requests and detect performance drift over time
  - - Use CSV logging for request statistics and debugging
    - - Understand observability integration into MLOps lifecycle
      - - Build production-ready logging infrastructure
       
        - ## Implementation Steps
       
        - ### 1. Install Dependencies
        - ```bash
          pip install -r requirements.txt
          ```

          ### 2. Run the Flask Application
          ```bash
          python monitoring_app.py
          ```
          The API will start on `http://localhost:5000`

          ### 3. Test the Endpoints

          **Make a prediction:**
          ```bash
          curl -X POST http://localhost:5000/predict \
            -H "Content-Type: application/json" \
            -d '{"features": [1.0, 2.0, 3.0]}'
          ```

          **View monitoring statistics:**
          ```bash
          curl http://localhost:5000/monitor
          ```

          **Check system health:**
          ```bash
          curl http://localhost:5000/health
          ```

          ## Key Features

          ### Request Logging
          - CSV-based logging of all requests with timestamps
          - - Tracks request count, response time, and endpoint usage
            - - Maintains request statistics in memory for performance monitoring
             
              - ### Monitoring Endpoints
              - - `/predict` - Primary inference endpoint (POST)
                - - `/monitor` - Returns aggregated statistics and performance metrics (GET)
                  - - `/health` - Returns system health status (GET)
                   
                    - ### Log Files
                    - - `requests.csv` - Request history with timestamps and durations
                      - - `app.log` - Application logs for debugging
                       
                        - ## File Descriptions
                       
                        - ### monitoring_app.py
                        - Main Flask application implementing:
                        - - Request timing decorators for performance monitoring
                          - - CSV logging for audit trail
                            - - JSON-based request/response handling
                              - - Three API endpoints for inference and monitoring
                               
                                - ### requirements.txt
                                - Specifies project dependencies (Flask 3.0.3)
                               
                                - ## Testing in Codespace
                                - You can test this application in GitHub Codespace:
                                - 1. Open repository in Codespace
                                  2. 2. Run `pip install -r requirements.txt`
                                     3. 3. Run `python monitoring_app.py`
                                        4. 4. Use the provided curl commands to test endpoints
                                           5. 5. Check logs/ directory for generated log files
                                             
                                              6. ## References
                                              7. - Flask Documentation: https://flask.palletsprojects.com/
                                                 - - MLOps Monitoring Best Practices
                                                   - - Observability in Machine Learning Systems

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import json
import os
from datetime import datetime
import threading

app = Flask(__name__)
CORS(app)

# Global variable to track pipeline status
pipeline_status = {"running": False, "progress": 0, "message": ""}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    return jsonify(pipeline_status)

@app.route('/api/candidates')
def get_candidates():
    try:
        # Return mock data for demo purposes
        candidates = [
            {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "123-456-7890",
                "job_title": "Software Engineer",
                "match_score": 0.85,
                "interview_time": "2024-01-30 10:00:00"
            },
            {
                "name": "Jane Smith",
                "email": "jane@example.com",
                "phone": "098-765-4321",
                "job_title": "Data Scientist",
                "match_score": 0.92,
                "interview_time": "2024-01-30 11:00:00"
            }
        ]
        return jsonify({"success": True, "candidates": candidates})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/run-pipeline', methods=['POST'])
def run_pipeline():
    global pipeline_status
    
    if pipeline_status["running"]:
        return jsonify({"success": False, "message": "Pipeline is already running"})
    
    def pipeline_worker():
        global pipeline_status
        try:
            pipeline_status = {"running": True, "progress": 10, "message": "Initializing database..."}
            
            pipeline_status = {"running": True, "progress": 30, "message": "Processing job descriptions..."}
            
            pipeline_status = {"running": True, "progress": 50, "message": "Extracting CV data..."}
            
            pipeline_status = {"running": True, "progress": 70, "message": "Matching candidates..."}
            
            pipeline_status = {"running": True, "progress": 90, "message": "Scheduling interviews..."}
            
            pipeline_status = {"running": False, "progress": 100, "message": "Pipeline completed successfully!"}

        except Exception as e:
            pipeline_status = {"running": False, "progress": 0, "message": f"Error: {str(e)}"}
    
    # Start pipeline in background thread
    thread = threading.Thread(target=pipeline_worker)
    thread.daemon = True
    thread.start()
    
    return jsonify({"success": True, "message": "Pipeline started"})

@app.route('/api/job-descriptions')
def get_job_descriptions():
    try:
        # Return mock job descriptions
        job_descriptions = [
            {
                "title": "Software Engineer",
                "summary": "We are looking for a skilled software engineer with experience in Python and web development."
            },
            {
                "title": "Data Scientist",
                "summary": "Seeking a data scientist with strong analytical skills and machine learning experience."
            }
        ]
        return jsonify({"success": True, "jobs": job_descriptions})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/stats')
def get_stats():
    try:
        return jsonify({
            "success": True,
            "stats": {
                "total_candidates": 2,
                "total_jobs": 2,
                "jobs_breakdown": {"Software Engineer": 1, "Data Scientist": 1},
                "average_match_score": 0.885
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get('PORT', 10000))
    
    # Force Flask to use the port
    app.run(debug=False, host='0.0.0.0', port=port)

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import json
import os
from datetime import datetime
import threading
from Agents.jd_summarizer import summarize_all_jds
from Agents.cv_extractor import extract_cvs
from Agents.matcher import match_jd_cv
from Agents.shortlister import shortlist_candidates
from Agents.scheduler import schedule_interviews
from Database.db_handler import init_db, store_results, get_all_candidates

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
        candidates = get_all_candidates()
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
            init_db()

            pipeline_status = {"running": True, "progress": 20, "message": "Summarizing Job Descriptions..."}
            jd_summary = summarize_all_jds("Data/job_description.csv")

            pipeline_status = {"running": True, "progress": 30, "message": "Extracting CV data..."}
            cvs = extract_cvs("Data/CVs1/")

            pipeline_status = {"running": True, "progress": 50, "message": "Matching CVs with JD summary..."}
            match_scores = match_jd_cv(jd_summary, cvs)

            pipeline_status = {"running": True, "progress": 70, "message": "Shortlisting candidates..."}
            shortlisted = shortlist_candidates(match_scores, cvs)

            pipeline_status = {"running": True, "progress": 85, "message": "Scheduling interviews..."}
            shortlisted = schedule_interviews(shortlisted)

            pipeline_status = {"running": True, "progress": 95, "message": "Storing results in DB..."}
            store_results(shortlisted)

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
        summaries_dir = "Data/summaries"
        job_descriptions = []
        
        if os.path.exists(summaries_dir):
            for filename in os.listdir(summaries_dir):
                if filename.endswith('.txt'):
                    with open(os.path.join(summaries_dir, filename), 'r', encoding='utf-8') as f:
                        content = f.read()
                        job_descriptions.append({
                            "title": filename.replace('.txt', '').replace('-', ' '),
                            "summary": content
                        })
        
        return jsonify({"success": True, "jobs": job_descriptions})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/stats')
def get_stats():
    try:
        candidates = get_all_candidates()
        
        # Calculate statistics
        total_candidates = len(candidates)
        jobs = {}
        for candidate in candidates:
            job_title = candidate.get('job_title', 'Unknown')
            if job_title not in jobs:
                jobs[job_title] = 0
            jobs[job_title] += 1
        
        # Get average match score
        avg_score = 0
        if candidates:
            scores = [float(c.get('match_score', 0)) for c in candidates if c.get('match_score')]
            avg_score = sum(scores) / len(scores) if scores else 0
        
        return jsonify({
            "success": True,
            "stats": {
                "total_candidates": total_candidates,
                "total_jobs": len(jobs),
                "jobs_breakdown": jobs,
                "average_match_score": round(avg_score, 3)
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)

from Agents.jd_summarizer import summarize_all_jds
from Agents.cv_extractor import extract_cvs
from Agents.matcher import match_jd_cv
from Agents.shortlister import shortlist_candidates
from Agents.scheduler import schedule_interviews
from Database.db_handler import init_db, store_results
from Emails.email_sender import send_email
import os

def run_pipeline():
    try:
        print("🔧 [1] Initializing database...")
        init_db()

        print("📝 [2] Summarizing Job Descriptions...")
        jd_summary = summarize_all_jds("Data/job_description.csv")

        print("📄 [3] Extracting CV data...")
        cvs = extract_cvs("Data/CVs1/")

        print("🤝 [4] Matching CVs with JD summary...")
        match_scores = match_jd_cv(jd_summary, cvs)

        print("📌 [5] Shortlisting candidates...")
        shortlisted = shortlist_candidates(match_scores, cvs)

        print("📅 [6] Scheduling interviews...")
        shortlisted = schedule_interviews(shortlisted)  # ✅ Capture updated list

        print("💾 [7] Storing results in DB...")
        store_results(shortlisted)  # ✅ Now includes interview time & date

        print("📧 [8] Sending confirmation emails...")
        for candidate in shortlisted:
            send_email(candidate)

        print("✅ All tasks completed successfully!")

    except Exception as e:
        print(f"❌ Error in pipeline execution: {e}")

if __name__ == "__main__":
    run_pipeline()

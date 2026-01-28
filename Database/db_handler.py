import sqlite3
import os

DB_PATH = "database/hire_smart.db"

def init_db():
    """Initializes the SQLite database and creates required tables."""
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop and recreate the table every time for fresh state
    cursor.execute("DROP TABLE IF EXISTS candidates")

    cursor.execute("""
        CREATE TABLE candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            cv_path TEXT,
            score REAL,
            status TEXT,
            matched_jd TEXT,
            interview_date TEXT,
            interview_time TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized and table ready (reset).")

def store_results(shortlisted: list):
    """
    Stores shortlisted candidates in the database.
    """
    if not shortlisted:
        print("⚠️ No candidates to store.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for candidate in shortlisted:
        cursor.execute("""
            INSERT INTO candidates (
                name, email, phone, cv_path, score, status,
                matched_jd, interview_date, interview_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            candidate.get("name"),
            candidate.get("email"),
            candidate.get("phone"),
            candidate.get("cv_path"),
            candidate.get("score"),
            candidate.get("status", "shortlisted"),
            candidate.get("job_title"),
            candidate.get("interview_date"),
            candidate.get("interview_time")
        ))

    conn.commit()
    conn.close()
    print(f"📦 Stored {len(shortlisted)} candidates in the database.")

def get_all_candidates():
    """
    Retrieves all candidates from the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, email, phone, cv_path, score, status, 
               matched_jd, interview_date, interview_time
        FROM candidates
        ORDER BY score DESC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    candidates = []
    for row in rows:
        candidates.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3],
            "cv_path": row[4],
            "match_score": row[5],
            "status": row[6],
            "job_title": row[7],
            "interview_date": row[8],
            "interview_time": f"{row[8]} {row[9]}" if row[8] and row[9] else None,
            "candidate_id": os.path.basename(row[4]).replace('.pdf', '') if row[4] else f"Candidate_{row[0]}"
        })
    
    return candidates

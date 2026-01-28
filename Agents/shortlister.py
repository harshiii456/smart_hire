from typing import Dict, List, Tuple
from Utils.text_utils import extract_name, extract_email, extract_phone

def shortlist_candidates(match_scores: Dict[str, List[Tuple[str, float]]], cvs: Dict[str, str], threshold: float = 0.50) -> List[Dict]:
    """
    Shortlists top 5 candidates for each job with score >= threshold.
    Adds metadata (name, email, phone) extracted from the CV text.
    """
    print("📋 Shortlisting top 5 candidates per job with match score >= {:.2f}...".format(threshold))
    shortlisted = []

    for job_title, scores in match_scores.items():
        top_candidates = []

        # Filter candidates above threshold
        filtered = [(cv_filename, score) for cv_filename, score in scores if score >= threshold]

        # Sort by score descending and pick top 5
        top_5 = sorted(filtered, key=lambda x: x[1], reverse=True)[:5]

        for cv_filename, score in top_5:
            cv_text = cvs.get(cv_filename, "")
            email = extract_email(cv_text)

            if not email:
                print(f"⚠️ {cv_filename} skipped due to missing email.")
                continue

            candidate = {
                "name": extract_name(cv_text),
                "email": email,
                "phone": extract_phone(cv_text),
                "cv_path": cv_filename,
                "job_title": job_title,
                "score": score
            }

            shortlisted.append(candidate)
            print(f"✅ {cv_filename} shortlisted for {job_title} (score: {score})")

    return shortlisted

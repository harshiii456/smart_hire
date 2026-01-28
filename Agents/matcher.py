# Agents/matcher.py

from sentence_transformers import SentenceTransformer, util #type: ignore
from typing import Dict, List
import torch

# Load the model
model = SentenceTransformer("all-MiniLM-L6-v2")

def match_jd_cv(jd_summaries: Dict[str, str], cvs: Dict[str, str]) -> Dict[str, List[tuple]]:
    """
    Matches each CV to each JD summary using cosine similarity.
    Returns a dict of {job_title: [(cv_name, score), ...]} sorted by score.
    """
    match_results = {}

    print("🔎 Generating embeddings and calculating similarities...")

    for job_title, jd_summary in jd_summaries.items():
        jd_embedding = model.encode(jd_summary, convert_to_tensor=True)
        matches = []

        for cv_name, cv_text in cvs.items():
            cv_embedding = model.encode(cv_text, convert_to_tensor=True)
            similarity = util.cos_sim(jd_embedding, cv_embedding).item()
            matches.append((cv_name, round(similarity, 3)))

        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        match_results[job_title] = matches

    print("✅ Matching complete!")
    return match_results

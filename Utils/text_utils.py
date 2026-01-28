# utils/text_utils.py

import re
import string

def clean_text(text: str) -> str:
    """
    Lowercases, removes extra whitespace, punctuation, and special characters.
    """
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()

def extract_email(text: str) -> str:
    """
    Extracts the first email found in the text.
    """
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else ""

def extract_phone(text: str) -> str:
    """
    Extracts a phone number (basic pattern).
    """
    match = re.search(r'(\+91[\-\s]?)?[0]?[6789]\d{9}', text)
    return match.group(0) if match else ""

def extract_name(text: str) -> str:
    """
    Very naive name extractor using common header formats.
    You could replace this with an NER model later.
    """
    lines = text.strip().split('\n')
    if lines:
        return lines[0].strip()
    return "Unknown"

def jaccard_similarity(set1, set2):
    """
    Simple Jaccard similarity for matching.
    """
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if union else 0

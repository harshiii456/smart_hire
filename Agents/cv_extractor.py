# agents/cv_extractor.py

import os
import fitz  # PyMuPDF #type: ignore

def extract_cvs(cv_folder: str) -> dict:
    """
    Extracts text content from all PDF CVs in the given folder.
    Returns a dictionary {filename: extracted_text}.
    """
    cv_data = {}
    supported_ext = ('.pdf',)

    for filename in os.listdir(cv_folder):
        if filename.lower().endswith(supported_ext):
            file_path = os.path.join(cv_folder, filename)

            try:
                doc = fitz.open(file_path)
                text = ""

                for page in doc:
                    try:
                        text += page.get_text()
                    except Exception as e:
                        print(f"⚠️ Failed to extract text from a page in {filename}: {e}")
                        continue

                doc.close()
                if text.strip():
                    cv_data[filename] = text
                else:
                    print(f"⚠️ No text found in {filename}")

            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

    return cv_data

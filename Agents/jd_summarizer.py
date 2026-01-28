import pandas as pd
import subprocess
import os

def summarize_all_jds(csv_path: str, save_folder: str = "data/summaries") -> dict:
    """
    Reads JDs from a CSV file and summarizes them using Ollama,
    unless a summary already exists in the save_folder.
    """
    os.makedirs(save_folder, exist_ok=True)

    try:
        df = pd.read_csv(csv_path, encoding="ISO-8859-1")
        summaries = {}

        for index, row in df.iterrows():
            title = row['Job Title']
            description = row['Job Description']
            file_name = f"{title.replace('/', '-')}.txt"
            file_path = os.path.join(save_folder, file_name)

            # ✅ Skip summarization if file already exists
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    summaries[title] = f.read()
                print(f"📂 Loaded existing summary for: {title}")
                continue

            # Generate new summary
            prompt = f"""
            Summarize the following Job Description into clear bullet points 
            highlighting responsibilities, required skills, and qualifications:\n\n
            {description}
            """

            result = subprocess.run(
                ["ollama", "run", "mistral", prompt],
                capture_output=True,
                text=True,
                check=True
            )

            summary = result.stdout.strip()
            summaries[title] = summary

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(summary)

            print(f"📝 Summarized and saved: {title}")

        return summaries

    except Exception as e:
        print(f"❌ Error during JD summarization: {e}")
        return {}

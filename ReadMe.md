# 💼 HireSmart AI

**Intelligent Automation for Job Candidate Screening**

HireSmart AI is a multi-agent system designed to automate the job screening process. It reads job descriptions, extracts and evaluates candidate CVs, calculates semantic similarity, shortlists the best-fit candidates, and schedules interviews — all with minimal manual intervention.

---

## 🚀 Features

- 📄 **JD Summarization**: Cleans and condenses job descriptions using LLM.
- 📑 **CV Extraction**: Extracts text from PDFs using PyMuPDF.
- ⚖️ **Matching Engine**: Computes semantic similarity between CVs and JDs.
- 🎯 **Shortlisting Agent**: Filters top candidates based on match score and metadata.
- 🗓️ **Scheduler Agent**: Sends automated interview invites with Google Meet links.
- 🗃️ **SQLite Integration**: Stores shortlisted candidate data for record-keeping.

---

## 🧠 Agents in Action

| Agent Name        | Description                                                             |
|-------------------|-------------------------------------------------------------------------|
| JD Summarizer     | Uses LLM to extract key points from job descriptions.                   |
| CV Extractor      | Parses resumes (PDFs) into clean text for processing.                   |
| Matcher           | Uses sentence transformers to compute similarity scores.                |
| Shortlister       | Filters candidates by score & extracts name, email, phone.              |
| Scheduler         | Sends personalized emails and schedules interviews via Google Calendar. |

---

## 🛠️ Technologies Used

- **Python 3.1+**
- **Ollama + Mistral** (LLM for summarization)
- **SentenceTransformers** (`all-MiniLM-L6-v2`)
- **Torch** (backend for embeddings)
- **PyMuPDF (fitz)** for CV parsing
- **SQLite3** for candidate tracking
- **Google Calendar API + Gmail SMTP** for scheduling
- **dotenv** for credential management

---

## 📂 Project Structure

```bash
HireSmartAI/
│
├── agents/
│   ├── jd_summarizer.py
│   ├── cv_extractor.py
│   ├── matcher.py
│   ├── shortlister.py
│   └── scheduler.py
│
├── data/
│   ├── cvs/                  # Candidate resumes (PDFs)
│   └── job_descriptions/     # Raw and summarized JDs
│
├── database/
│   ├── hire_smart.db
│   └── db_handler.py
│
├── emails/
│   └── email_sender.py
│
├── utils/
│   └── text_utils.py
│
├── main.py                   # Runs full pipeline
├── requirements.txt
└── README.md

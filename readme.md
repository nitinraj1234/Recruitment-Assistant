# Recruitment Assistant

A resume screening and interview preparation tool built with Streamlit, LangChain, and Groq. It takes a candidate's resume, scores it against a target role or a custom job description, and generates interview questions and improvement suggestions — all without storing any data between sessions.

Live demo: https://recruitment-assistant-bauel4dzgwouw2klwyssxj.streamlit.app

---

## What it does

Most ATS tools are black boxes. This one shows you exactly what it found, what it missed, and why it made the decision it did. You upload a resume, pick a role, and within a few seconds you get a score, a breakdown of matched and missing skills, and a set of interview questions tailored to that candidate's actual profile.

There are four main functions:

**Resume Scoring** — The tool compares the resume against a skill list for the selected role (or extracts skills directly from a pasted job description). It uses vector similarity search rather than simple keyword matching, so it can recognise that a candidate who mentions "fine-tuning LLMs" has the "transformers" skill even if they never wrote that exact word. The output is a score out of 100 with a configurable pass threshold.

**Document Q&A** — You can ask free-form questions about the resume and get direct answers. Useful for quickly checking specifics like "how many years of experience does this candidate have in Python" or "what was their role at their last job" without reading the whole document. It uses a combination of semantic retrieval and raw document injection to minimise hallucination.

**Interview Question Generator** — Generates a structured set of interview questions based on the candidate's resume, the target role, and the gaps identified during scoring. You can choose between Technical, Behavioral, and Situational question types, set a difficulty level, and control how many questions are produced.

**Resume Improvement Suggestions** — Gives section-by-section guidance on how to strengthen the resume for the target role. It focuses on the skills that were identified as missing and suggests how to frame existing experience to address those gaps.

---

## Supported roles

The tool has built-in skill profiles for eight roles. When no job description is provided, scoring runs against the relevant profile.

- AI Engineer
- Backend Engineer
- Frontend Engineer
- Full Stack Engineer
- Data Scientist
- Data Engineer
- DevOps Engineer
- Data Analyst

If your target role is not in this list, paste a job description instead and the tool will extract the skill requirements from it automatically.

---

## How the scoring works

When a resume is uploaded, the text is split into overlapping chunks and converted into vector embeddings using the `all-MiniLM-L6-v2` model from HuggingFace. These are stored in a FAISS index for fast similarity search.

For each skill in the role profile, the tool runs a similarity search against this index. The distance score determines whether the skill is counted as a strong match, a partial match, or missing. The final ATS score is the percentage of required skills that cleared the match threshold.

When a job description is provided, the Groq LLM (Llama 3.3 70B) first extracts the key skills from the JD text, then runs the same vector matching process against those extracted skills.

---

## Setup

**Prerequisites**

- Python 3.11
- A Groq API key (free tier works fine, get one at console.groq.com)

**Installation**

```bash
git clone https://github.com/nitinraj1234/Recruitment-Assistant.git
cd Recruitment-Assistant
pip install -r requirements.txt
```

**Running locally**

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`, paste your Groq API key in the sidebar, and you are ready to go.

---

## Usage

1. Enter your Groq API key in the left panel
2. Set the minimum score threshold (default is 70)
3. Select the target role from the dropdown, or leave it and paste a job description in the text area below
4. Upload the candidate's resume as a PDF or TXT file
5. Use the four tabs to run analysis, ask questions, generate interview questions, or get improvement suggestions

The session is stateless. Nothing is saved after you close the browser tab.

---

## Project structure

```
Recruitment-Assistant/
├── app.py              # Streamlit UI and tab layout
├── agents.py           # Core agent class, scoring logic, LLM calls
├── ui.py               # CSS styling and display helper functions
├── requirements.txt    # Python dependencies
└── runtime.txt         # Python version pin for Streamlit Cloud
```

---

## Dependencies

| Package | Purpose |
|---|---|
| streamlit | Web interface |
| langchain-groq | Groq LLM integration |
| langchain-huggingface | HuggingFace embeddings |
| langchain-community | FAISS vector store wrapper |
| faiss-cpu | Vector similarity search |
| sentence-transformers | Local embedding model |
| PyPDF2 | PDF text extraction |
| matplotlib | Score pie chart |
| pandas | Data handling |
| python-dotenv | Local environment variable loading |

---

## Limitations

- PDF extraction quality depends on how the PDF was created. Scanned image-based PDFs will not extract text properly.
- The scoring is based on skill presence, not depth of experience. A candidate who mentioned Docker once gets the same score as someone with five years of Kubernetes experience.
- The tool works best with English-language resumes.
- There is no persistent storage. Each session starts fresh.

---

## License

MIT

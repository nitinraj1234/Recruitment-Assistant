# Recruitment Assistant

A resume screening and interview preparation tool built with Streamlit, LangChain, and Groq. It takes a candidate's resume, scores it against a target role or a custom job description, and generates interview questions and improvement suggestions — all without storing any data between sessions.

Live demo: https://recruitment-assistant-bauel4dzgwouw2klwyssxj.streamlit.app

---

## Who is this for

**Recruiters** use it to screen resumes faster. Instead of reading every document manually, you upload the resume, select the role, and get a score with a clear breakdown of what matched and what did not. You can also auto-generate role-specific interview questions tailored to that candidate's actual profile, which saves significant prep time before a call.

**Students and job seekers** use it to understand exactly why their resume is getting filtered out. You can paste a real job description, upload your resume, and see which skills the system finds and which ones it misses. The improvement suggestions tell you specifically what to add or reframe in each section to increase your score for that role. Many students use it to test their resume against multiple roles before deciding where to apply.

---

## What it does

There are four main functions:

**Resume Scoring** — The tool compares the resume against a skill list for the selected role, or extracts skills directly from a pasted job description. It uses vector similarity search rather than simple keyword matching, so it can recognise related skills even when the exact keyword is not present. The output is a score out of 100 with a configurable pass threshold.

**Document Q&A** — Ask free-form questions about the resume and get direct answers. Useful for recruiters who want to quickly verify specifics like years of experience, previous job titles, or listed projects without reading the full document. It uses a combination of semantic retrieval and raw document scanning to stay accurate.

**Interview Question Generator** — Generates a structured set of interview questions based on the candidate's resume, the target role, and the skill gaps identified during scoring. You can choose between Technical, Behavioral, and Situational question types, set a difficulty level, and control how many questions are produced. For students, this is also a useful way to predict what an interviewer might ask you.

**Resume Improvement Suggestions** — Gives section-by-section guidance on how to strengthen the resume for the target role. It focuses on the skills identified as missing and suggests how to frame existing experience to address those gaps. Students can use this before applying; recruiters can share the output as structured feedback to candidates.

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

## How to use the demo

1. Open the live demo link above
2. In the **sidebar on the left**, set the **Minimum Screening Threshold** (default is 70)
3. In the **sidebar**, select your **Target Position** from the dropdown
4. Scroll down to **Document Input Settings** and upload your resume as a PDF or TXT file
5. Optionally paste a job description if you want to match against a specific role instead of the built-in profile
6. Use the four tabs to run analysis, ask questions, generate interview questions, or get improvement suggestions

---

## How the scoring works

When a resume is uploaded, the text is split into overlapping chunks and converted into vector embeddings using the `all-MiniLM-L6-v2` model from HuggingFace. These are stored in a FAISS index for fast similarity search.

For each required skill, the tool runs a similarity search against this index. The distance score determines whether the skill is counted as a strong match, partial match, or missing. The final ATS score is the percentage of required skills that cleared the match threshold.

When a job description is provided, the Groq LLM (Llama 3.3 70B) first extracts the key skills from the JD text, then runs the same vector matching process against those extracted skills.

---

## Local Setup

**Prerequisites**

- Python 3.11

**Installation**

```bash
git clone https://github.com/nitinraj1234/Recruitment-Assistant.git
cd Recruitment-Assistant
pip install -r requirements.txt
```

**Configuration**

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key at [console.groq.com](https://console.groq.com).

**Run**

```bash
streamlit run app.py
```

---

## Project structure

```
Recruitment-Assistant/
├── app.py              # Streamlit UI and tab layout
├── agents.py           # Core agent class, scoring logic, LLM calls
├── ui.py               # CSS styling and display helper functions
├── requirements.txt    # Python dependencies
├── runtime.txt         # Python version pin for Streamlit Cloud
└── .env                # API key (local only, not committed to GitHub)
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
- The scoring is based on skill presence, not depth of experience. A candidate who mentioned Docker once scores the same as someone with five years of Kubernetes experience.
- The tool works best with English-language resumes.
- There is no persistent storage. Each session starts fresh.

---

## License

MIT

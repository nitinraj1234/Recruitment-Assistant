# Recruitment Assistant

A simple, fast resume screening and interview preparation app built with Streamlit, LangChain, and Groq. It scans a candidate's resume, grades it against a target job role or a custom job description, and drops a list of tailored interview questions and resume improvement notes—all on a temporary basis without storing any candidate data between reloads.

Live demo: https://recruitment-assistant-bauel4dzgwouw2klwyssxj.streamlit.app

---

## What it's used for

* **Recruiters & Hiring Managers:** Instead of manually scanning every line of a stack of PDFs, you can drop a resume in, pick a role context, and immediately see an estimated percentage match with a clean breakdown of what requirements were hit and what was missing. It also spins up contextual interview questions matched specifically to that applicant's skill gaps before a screening call.
* **Job Seekers & Students:** Use it to check why your resume might be missing the mark. You can paste the exact job text you are targeting, upload your resume, and check exactly which skills are matching or going unnoticed. The improvement breakdown suggests exactly what keywords to add or reframe to raise your match likelihood.

---

## Core Features

1. **Resume Match Scoring:** Compares an uploaded profile against target skills using vector proximity rather than rigid word matching (so it understands related concepts even if the exact keyword differs). Outputs a clean score against a customizable target filter.
2. **Document Q&A Terminal:** A free-form question input box where you can interrogate the document file directly. Useful for pulling specific facts quickly—like confirming absolute years of experience, locating niche project achievements, or pulling details out without scrolling pages.
3. **Interview Evaluator Engine:** Generates evaluation questions based directly on the intersection of the resume and the job criteria gaps. You can tune the output by selecting Technical, Behavioral, or Situational focuses, adjust the complexity tiers, and choose how many questions to produce.
4. **Resume Improvement Roadmap:** Delivers a clear guide on how to restructure or polish particular blocks of your document. It focuses directly on fixing requirements gaps so you know exactly what points to flesh out with metrics before submitting.

---

## Supported Built-In Roles

If you don't have a specific job description on hand, the app features pre-configured engineering and corporate skill profiles for a variety of roles:

* AI / ML / NLP / Generative AI Engineer
* Backend / Frontend / Full Stack / SDE Engineer
* Data Scientist / Data Engineer / Data Analyst
* Cloud / DevOps / Platform / Network / Security Engineer
* Embedded Systems / VLSI Engineer
* Product Manager / Business Analyst / UI-UX Designer
* Strategy Consultant / Financial Analyst
* R&D / Process Development Engineer

*Have a role not listed? Just paste the raw job details text directly into the text field and the app will parse requirements out automatically.*

---

## How It Works Under the Hood

When a file is loaded, PyPDF2 reads out the raw text lines. The app splits this text into small overlapping paragraphs and converts those segments into vector embeddings using a local `all-MiniLM-L6-v2` instance from HuggingFace. This collection is indexed inside an in-memory FAISS instance.

* When validating skills, the app queries your index with target keyword queries. The resulting vector distance defines whether a requirement is flagged as a strong match, a partial match, or a missing element.
* When working with a custom job description, the app prompts a Llama 3.3 70B instance via Groq to pull a clean list of requirements, which are then passed into the exact same vector verification loop.

---

## Local Development Setup

### Prerequisites
* Python 3.11
* Git

### Installation
```bash
# Clone the workspace repository
git clone [https://github.com/nitinraj1234/Recruitment-Assistant.git](https://github.com/nitinraj1234/Recruitment-Assistant.git)
cd Recruitment-Assistant

# Install required Python packages
pip install -r requirements.txt

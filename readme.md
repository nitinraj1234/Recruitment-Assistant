# Recruitment Assistant

This is a simple website built with Streamlit, LangChain, and Groq. It makes it super easy to check resumes and get ready for job interviews. The website reads a candidate's resume, gives it a grade based on how well it fits a specific job, and shows you exactly what is missing. It does all of this safely without saving any of your personal files or information.

Live demo: https://recruitment-assistant-bauel4dzgwouw2klwyssxj.streamlit.app




## Who is this for?

* **Recruiters & Hiring Managers:** Instead of wasting hours reading every single line of a huge stack of PDFs, you can just upload a resume to get a quick match score. The website shows you exactly what skills the candidate has and where they need to improve. You can even type questions into a chat box to pull out hidden details from the resume instantly. 
* **Job Seekers:** You can figure out exactly why your resume is getting rejected by automatic company scanners. By picking a job title or pasting a real job description, you can see which keywords the app finds and which ones it misses. This helps you fix your resume before you actually apply. The app gives you easy tips to fix your Summary, Experience, and Projects sections. You can also use the generated questions to practice your answers and study your weak spots so you feel confident before the real interview.

---

## What the Website Does

1. **Resume Screening Report:** This shows you a total match score percentage. It uses a smart vector store similarity search that understands related skills, so it still works even if you did not use the exact matching words.
2. **Document Verification Q&A:** A simple search box where you can ask direct questions about the resume, like *"How many years of experience does this person have with React?"* or *"Where did they work last?"*
3. **Interview Questions:** This creates custom practice questions based on the resume. You can change the difficulty (Easy, Medium, Hard) and pick the type of question (Technical, Behavioral, or Situational).
4. **Refinement Suggestions:** Gives you an easy blueprint on how to rewrite or clean up different parts of your resume (like your Summary, Work Experience, or Projects) to match the job better.

---

## How to Use It

1. **Select a Position:** Pick a target job role from the dropdown menu in the center of the page.
2. **(Optional) Paste a Job Description:** If you have a specific job description from a company website, paste the text into the large box.
3. **Upload the Resume:** Drag and drop your candidate resume (must be a PDF) into the file uploader. 
4. **Check the Report:** Head to the **Resume Screening Report** tab to look at your overall score circle and check which keywords passed or failed.
5. **Chat with the Resume:** Open the **Document Verification Q&A** tab and type a free-form question to extract secret details from the file text.
6. **Practice or Prep:** Use the **Interview Questions** and **Refinement Suggestions** tabs to see AI-generated mock interview prep questions and clear resume rewrite goals.

---
## How the Website Works

When you upload a PDF resume, the app uses a python tool called `PyPDF2` to read all the text. Then, it splits that text into small pieces called chunks and makes a mini digital map of the sentences based on what the words mean (these are called vector embeddings). The app saves this map temporarily in a vectorstore called FAISS.

Depending on what buttons you click in the sidebar, the matching works in two ways:

1. **Using a Pre-set Role:** If you pick a normal job title from the menu (like *Data Scientist*), the app takes a built-in list of important skills for that job and searches your resume map. It looks for matching skills based on how close the ideas are, not just matching the exact letters.
2. **Using a Custom Job Description:** If you paste a real job description into the text box *after* picking a role, the app skips the built-in list. It sends the text to a smart AI model (`meta-llama/llama-4-scout-17b-16e-instruct` using Groq) to pull out the most important skills from that specific job description. Then, it runs semantic search on your resume using those custom keywords.

After the search finishes, the app figures out your final score, highlights which skills were found or missed, and uses the AI model to make your custom interview questions and resume tips.

### How the Q&A Box Works (RAG)
For the **Document Verification Q&A** tab, we use a technique called **RAG (Retrieval-Augmented Generation)**. When you type a question about the resume, the app does not just hand your question blindly to the AI. Instead, it searches the temporary digital map (FAISS) to pull out the exact sentences in the resume that match your question. Then, it hands both your question and those matching resume lines to the AI model. This setup forces the AI to answer using only the real facts inside the document, preventing it from making up fake information.

---

## Tech Stack (Tools We Used)

* **Frontend & UI:** `Streamlit` (To build the web interface and buttons quickly with Python).
* **AI Model Engine:** `Groq API` running `meta-llama/llama-4-scout-17b-16e-instruct` (For super-fast text generation and smart resume tips).
* **AI Framework:** `LangChain` (To connect our prompt layouts, AI calls, and document chunking tools together).
* **Vector Embeddings:** `Hugging Face` (`all-MiniLM-L6-v2` model to turn text chunks into vector embeddings ).
* **Vector Database:** `FAISS` (A fast, local memory database to store vectors and perform semantic search ).
* **PDF Reader:** `PyPDF2` (To extract raw text strings directly out of uploaded PDF resumes).

---

import os
import re
import io
import json
import tempfile
from io import StringIO


import PyPDF2
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

ROLE_KEYWORDS = {
   
    "AI Engineer": [
        "python", "machine learning", "deep learning", "tensorflow", "pytorch",
        "nlp", "computer vision", "mlops", "hugging face", "reinforcement learning",
        "data engineering", "feature engineering", "auto ml", "llm", "transformers",
        "langchain", "vector database", "rag", "fine-tuning", "model deployment"
    ],
    "Backend Engineer": [
        "java", "node.js", "python", "rest api", "graphql", "microservices",
        "docker", "kubernetes", "aws", "spring boot", "sql", "nosql",
        "redis", "kafka", "grpc", "ci/cd", "system design", "scalability"
    ],
    "Frontend Engineer": [
        "react", "javascript", "typescript", "html", "css", "vue",
        "angular", "webpack", "redux", "graphql", "responsive design",
        "accessibility", "testing", "performance optimization", "figma"
    ],
    "Full Stack Engineer": [
        "react", "node.js", "python", "javascript", "typescript", "sql",
        "nosql", "docker", "aws", "rest api", "git", "agile",
        "html", "css", "mongodb", "postgresql"
    ],
    "Data Scientist": [
        "python", "machine learning", "statistics", "pandas", "numpy",
        "scikit-learn", "visualization", "sql", "r", "tensorflow",
        "hypothesis testing", "a/b testing", "regression", "classification",
        "deep learning", "nlp", "time series"
    ],
    "Data Engineer": [
        "python", "spark", "kafka", "airflow", "sql", "etl",
        "data warehousing", "aws", "gcp", "azure", "dbt", "hadoop",
        "redshift", "bigquery", "data modeling", "pipeline"
    ],
    "DevOps Engineer": [
        "docker", "kubernetes", "ci/cd", "jenkins", "terraform", "ansible",
        "aws", "linux", "bash", "monitoring", "prometheus", "grafana",
        "git", "helm", "networking", "security"
    ],
    "Data Analyst": [
        "sql", "excel", "python", "tableau", "power bi", "statistics",
        "data visualization", "pandas", "reporting", "a/b testing",
        "google analytics", "looker", "r"
    ],
    "Software Development Engineer (SDE)": [
        "data structures", "algorithms", "c++", "java", "python", "system design",
        "object oriented design", "dynamic programming", "graphs", "trees",
        "rest api", "sql", "git", "low level design", "high level design"
    ],
    "Embedded Systems Engineer": [
        "c", "c++", "rtos", "microcontrollers", "arm", "embedded linux",
        "uart", "spi", "i2c", "can bus", "firmware", "bare metal",
        "signal processing", "hardware debugging", "oscilloscope", "pcb"
    ],

   
    "Cloud Engineer": [
        "aws", "gcp", "azure", "terraform", "kubernetes", "docker",
        "cloud architecture", "iam", "vpc", "load balancing", "auto scaling",
        "s3", "ec2", "lambda", "cloud security", "cost optimization"
    ],
    "Site Reliability Engineer (SRE)": [
        "sre", "linux", "python", "go", "kubernetes", "docker", "prometheus",
        "grafana", "incident management", "slo", "sli", "error budget",
        "terraform", "ci/cd", "on-call", "chaos engineering", "observability"
    ],
    "Platform Engineer": [
        "kubernetes", "helm", "terraform", "ci/cd", "docker", "aws",
        "internal developer platform", "argocd", "github actions", "linux",
        "python", "bash", "observability", "service mesh", "istio"
    ],
    "Network Engineer": [
        "tcp/ip", "bgp", "ospf", "vlans", "routing", "switching",
        "cisco", "firewalls", "network security", "vpn", "dns", "dhcp",
        "load balancers", "wireshark", "network automation", "python"
    ],
    "Security Engineer": [
        "penetration testing", "owasp", "siem", "vulnerability assessment",
        "network security", "cryptography", "identity management", "oauth",
        "aws security", "incident response", "threat modeling", "firewalls",
        "python", "burp suite", "zero trust"
    ],

  
    "ML Engineer": [
        "python", "machine learning", "pytorch", "tensorflow", "scikit-learn",
        "mlops", "model training", "feature engineering", "model deployment",
        "docker", "kubernetes", "airflow", "aws sagemaker", "experiment tracking",
        "mlflow", "data pipelines", "a/b testing"
    ],
    "Computer Vision Engineer": [
        "python", "opencv", "pytorch", "tensorflow", "yolo", "cnn",
        "image segmentation", "object detection", "image classification",
        "data augmentation", "cuda", "onnx", "model deployment", "deep learning"
    ],
    "NLP Engineer": [
        "python", "nlp", "transformers", "hugging face", "bert", "gpt",
        "text classification", "named entity recognition", "summarization",
        "langchain", "rag", "llm", "fine-tuning", "spacy", "tokenization"
    ],
    "Generative AI Engineer": [
        "llm", "langchain", "rag", "prompt engineering", "fine-tuning",
        "openai api", "hugging face", "vector database", "pinecone", "faiss",
        "python", "langsmith", "agents", "function calling", "embeddings"
    ],
    "VLSI Engineer": [
        "verilog", "vhdl", "rtl design", "synthesis", "timing analysis",
        "fpga", "asic", "cadence", "synopsys", "physical design",
        "dft", "verification", "uvm", "system verilog", "timing closure"
    ],

  
    "Product Manager (PM)": [
        "product roadmap", "user stories", "agile", "scrum", "stakeholder management",
        "market research", "competitive analysis", "product strategy", "kpi",
        "wireframing", "jira", "a/b testing", "go-to-market", "prioritization", "okr"
    ],
    "UI/UX Designer": [
        "figma", "sketch", "adobe xd", "user research", "wireframing", "prototyping",
        "usability testing", "information architecture", "interaction design",
        "visual design", "design systems", "accessibility", "user flows", "typography"
    ],
    "Strategy Consultant": [
        "business strategy", "market analysis", "financial modeling", "powerpoint",
        "excel", "stakeholder management", "problem solving", "due diligence",
        "competitive landscape", "go-to-market strategy", "mba", "consulting frameworks",
        "mckinsey", "bcg", "data analysis", "presentation"
    ],
    "Business Analyst": [
        "requirements gathering", "business process", "sql", "excel", "power bi",
        "tableau", "stakeholder management", "use cases", "gap analysis",
        "process mapping", "jira", "agile", "data analysis", "brd", "functional specification"
    ],
    "Financial Analyst": [
        "financial modeling", "excel", "valuation", "dcf", "financial statements",
        "budgeting", "forecasting", "variance analysis", "bloomberg", "sql",
        "power bi", "accounting", "cfa", "python", "investment analysis"
    ],
    "R&D / Process Development Engineer": [
        "research", "experimental design", "data analysis", "python", "matlab",
        "literature review", "prototyping", "process optimization", "six sigma",
        "statistical analysis", "lab techniques", "technical writing", "patent",
        "scale-up", "doe", "simulation"
    ],
}

CUT_OFF_SCORE = 70  


class ResumeAnalysisAgent:
    def __init__(self, api_key: str, cut_off_score: int = CUT_OFF_SCORE):
        self.api_key = api_key.strip()
        self.cut_off_score = cut_off_score

        self.resume_text = None
        self.jd_text = None
        self.vector_store = None         
        self.analysis_result = None
        self.extracted_skills = None
        self.weaknesses = None

        os.environ["GROQ_API_KEY"] = self.api_key

    def extract_text_from_pdf(self, uploaded_file) -> str:
        try:
            uploaded_file.seek(0)
            reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
        except Exception as e:
            return f"Error extracting PDF text: {str(e)}"

    def extract_text_from_txt(self, uploaded_file) -> str:
        try:
            uploaded_file.seek(0)
            content = uploaded_file.read()
            if isinstance(content, bytes):
                return content.decode("utf-8").strip()
            return content.strip()
        except Exception as e:
            return f"Error reading text file: {str(e)}"

    def extract_text_from_file(self, uploaded_file) -> str:
        try:
            filename = uploaded_file.name.lower()
            ext = filename.split(".")[-1]
            if ext == "pdf":
                return self.extract_text_from_pdf(uploaded_file)
            elif ext in ("txt", "text"):
                return self.extract_text_from_txt(uploaded_file)
            else:
                return self.extract_text_from_pdf(uploaded_file)
        except Exception as e:
            return f"Error: {str(e)}" 

    def create_vector_store_for_pdf(self, text: str) -> FAISS:
        splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
        chunks = splitter.split_text(text)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = FAISS.from_texts(chunks, embeddings)
        return vector_store

    def create_vector_store_for_text(self, text: str) -> FAISS:
        splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
        chunks = splitter.split_text(text)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = FAISS.from_texts(chunks, embeddings)
        return vector_store

    def check_skill_match(self, skill: str) -> float:
        try:
            docs = self.vector_store.similarity_search_with_score(skill, k=4)
            if docs:
                avg_score = sum(doc[1] for doc in docs) / len(docs)
                if avg_score < 1.35:
                    return 10.0
                elif avg_score < 1.60:
                    return 7.0
                elif avg_score < 1.75:
                    return 4.0
            return 0.0
        except Exception:
            return 0.0

    def analyse_skills(self, keywords: list) -> dict:
        if not self.vector_store:
            return {"error": "Vector store not created. Upload resume first."}

        skill_scores = {}
        strengths = []
        missing_skills = []

        for skill in keywords:
            score = self.check_skill_match(skill)
            skill_scores[skill] = score
            if score >= 4.0:
                strengths.append(skill)
            else:
                missing_skills.append(skill)

        if keywords:
            matched = len(strengths)
            total_score = round((matched / len(keywords)) * 100, 2)
        else:
            total_score = 0

        selected = total_score >= self.cut_off_score

        reasoning = (
            f"Out of {len(keywords)} required skills, {len(strengths)} were identified "
            f"in the resume content. The calculated ATS score is {total_score}/100. "
            f"The minimum screening cut-off threshold is {self.cut_off_score}. "
            + ("Resume has successfully passed matching standard screening thresholds." if selected
               else "Resume does not meet standard screening thresholds.")
        )

        return {
            "skill_scores": skill_scores,
            "total_score": total_score,
            "selected": selected,
            "strengths": strengths,
            "missing_skills": missing_skills,
            "reasoning": reasoning,
            "min_score": self.cut_off_score,
        }

    def analyse_resume_weakness(self, keywords: list) -> dict:
        if not self.vector_store:
            return {"error": "Vector store not found."}

        llm = ChatGroq(
            groq_api_key=self.api_key,
            model_name="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.3
        )

        missing = []
        for skill in keywords:
            score = self.check_skill_match(skill)
            if score < 4.0:
                missing.append(skill)

        if not missing:
            return {"weaknesses": [], "details": "No major skills deficits detected."}

        prompt = f"""
        The candidate's resume shows lower alignment with the following keywords:
        {', '.join(missing)}

        For each area, provide a brief objective statement outlining:
        1. Professional relevance to the position
        2. Expected technical application alignment issues
        3. Clear steps for credential or profile remediation

        Maintain a strict, formal recruitment tone. Avoid exclamation marks.
        """

        response = llm.invoke([HumanMessage(content=prompt)])
        self.weaknesses = missing

        return {
            "weaknesses": missing,
            "details": response.content,
        }

    def extract_skills_from_jd(self, jd_text: str) -> list:
        llm = ChatGroq(
            groq_api_key=self.api_key,
            model_name="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.1
        )

        prompt = f"""
        Extract all required core technical skills, tools, frameworks, and core professional competencies
        from the following job description. Return ONLY a plain comma-separated list of items.
        Do not add commentary, bullet numbers, or text decorations.

        Job Description:
        {jd_text}

        Skills:
        """

        response = llm.invoke([HumanMessage(content=prompt)])
        skills_raw = response.content.strip()
        skills = [s.strip().lower() for s in skills_raw.split(",") if s.strip()]
        return skills

    def semantic_skill_analysis(self, jd_skills: list) -> dict:
        if not self.vector_store:
            return {"error": "Vector store not found."}

        strengths = []
        missing_skills = []
        skill_scores = {}

        for skill in jd_skills:
            score = self.check_skill_match(skill)
            skill_scores[skill] = score
            if score >= 4.0:
                strengths.append(skill)
            else:
                missing_skills.append(skill)

        total = len(jd_skills)
        matched = len(strengths)
        total_score = round((matched / total) * 100, 2) if total > 0 else 0
        selected = total_score >= self.cut_off_score

        return {
            "skill_scores": skill_scores,
            "total_score": total_score,
            "selected": selected,
            "strengths": strengths,
            "missing_skills": missing_skills,
            "reasoning": (
                f"Matched {matched}/{total} job specification criteria. "
                f"Calculated Score: {total_score}/100. Verification target: {self.cut_off_score}. "
                + ("Status: Approved for selection pipeline." if selected else "Status: Requirements criteria shortfall.")
            ),
            "min_score": self.cut_off_score,
        }

    def analyse_resume(self, role: str, custom_jd_text: str = None) -> dict:
        if not self.resume_text:
            return {"error": "No resume text data found."}

        if not self.vector_store:
            self.vector_store = self.create_vector_store_for_pdf(self.resume_text)

        result = {}

        if custom_jd_text:
            self.jd_text = custom_jd_text
            
            jd_skills = self.extract_skills_from_jd(custom_jd_text)
            self.extracted_skills = jd_skills

            analysis = self.semantic_skill_analysis(jd_skills)
            result.update(analysis)

            weakness = self.analyse_resume_weakness(jd_skills)
            result["weakness_details"] = weakness.get("details", "")
            result["weaknesses"] = weakness.get("weaknesses", [])
            result["analysis_type"] = "Job Description Matching Matrix"
            result["keywords_used"] = jd_skills

        else:
            keywords = ROLE_KEYWORDS.get(role, ROLE_KEYWORDS["AI Engineer"])
            self.extracted_skills = keywords

            analysis = self.analyse_skills(keywords)
            result.update(analysis)

            weakness = self.analyse_resume_weakness(keywords)
            result["weakness_details"] = weakness.get("details", "")
            result["weaknesses"] = weakness.get("weaknesses", [])
            result["analysis_type"] = "Role Profile Core Matrix Mapping"
            result["keywords_used"] = keywords

        self.analysis_result = result
        return result

    def ask_question(self, question: str) -> str:
        if not self.resume_text:
            return "Please provide an uploaded resume profile first."

        llm = ChatGroq(
            groq_api_key=self.api_key,
            model_name="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.1
        )

        retrieved_docs = []
        if self.vector_store:
            try:
                docs = self.vector_store.similarity_search(question, k=6)
                retrieved_docs = [d.page_content for d in docs]
            except Exception:
                pass

        chunks_context = "\n---\n".join(retrieved_docs)
        full_document_fallback = self.resume_text[:6000]

        prompt = f"""
        You are an advanced recruitment auditing system. Your task is to answer user verification queries with absolute, objective accuracy based on the provided resume context blocks.

        INSTRUCTIONS:
        - Prioritize direct factual confirmation. Do not deduce details not explicitly stated.
        - Look comprehensively through the data blocks to find names, headers, contact info, and multiple hidden projects.
        - If the user asks about multiple projects, work history, or candidate names, scan both the target chunks and the raw background sequence below to assemble the complete accurate answer.
        - If the information is missing from both provided blocks, reply: "The document context does not explicitly mention that information."

        TARGET SEARCH CHUNKS:
        {chunks_context}

        RAW BACKGROUND DOCUMENT SEQUENCE (HEADER & DETAILS MAP):
        {full_document_fallback}

        USER VERIFICATION QUERY:
        {question}

        EXPLICIT OBJECTIVE ANSWER:
        """
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            return response.content.strip()
        except Exception as e:
            return f"Error executing verification query: {str(e)}"

    def generate_interview_questions(self, role: str, question_type: str = "Technical", difficulty: str = "Medium", num_questions: int = 5) -> str:
        if not self.resume_text:
            return "Please provide an uploaded resume profile first."

        llm = ChatGroq(groq_api_key=self.api_key, model_name="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0.5)

        strengths_context = ""
        if self.analysis_result:
            strengths = self.analysis_result.get("strengths", [])
            weaknesses = self.analysis_result.get("weaknesses", [])
            strengths_context = f"Identified Profile Matrix Strengths: {', '.join(strengths)}\nIdentified Gaps: {', '.join(weaknesses)}"

        prompt = f"""
        You are an executive interviewer assessing a candidate for a senior {role} placement.
        Resume Baseline: {self.resume_text[:3500]}
        {strengths_context}
        Generate exactly {num_questions} explicit evaluation assessment questions.
        Category Classification: {question_type} | Evaluation Complexity Target: {difficulty}

        Format each question clearly as:
        Question [number]: [Evaluation Category] - [Question Text]
        Objective rationale for question choice: [Brief context]
        Target criteria milestones for an optimal assessment score: [2-3 objective execution points]
        """
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            return f"Error executing generation workflow: {str(e)}"

    def improve_resume(self, section: str, role: str) -> str:
        if not self.resume_text:
            return "Please provide an uploaded resume profile first."

        llm = ChatGroq(groq_api_key=self.api_key, model_name="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0.4)
        weaknesses = self.analysis_result.get("weaknesses", []) if self.analysis_result else []

        prompt = f"""
        You are a corporate resume optimization advisor. Formulate structured structural refinement directions for the '{section}' portion of the candidate resume targeting a {role} path.
        Current Document Input Context: {self.resume_text[:3500]}
        Target Keywords for Profile Alignment Adjustments: {', '.join(weaknesses) if weaknesses else 'None'}
        
        Provide professional alignment guidance strictly focused on objective impact metric statements.
        """
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            return f"Error executing optimization planning: {str(e)}"

    def cleanup(self):
        self.resume_text = None
        self.jd_text = None
        self.vector_store = None
        self.jd_vector_store = None
        self.analysis_result = None
        self.extracted_skills = None
        self.weaknesses = None

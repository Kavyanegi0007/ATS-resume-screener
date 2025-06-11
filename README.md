# ATS Resume Screener

A smart, AI-powered resume matching tool that evaluates candidate resumes against a job description using semantic similarity, keyword overlap, and NLP techniques. Built with Flask, SentenceTransformers, and a React frontend.

---

##  Features

-  **Semantic Matching** with [Sentence Transformers](https://www.sbert.net/)
-  **SpaCy & NLTK keyword extraction**
-  Support for PDF, DOCX, and TXT resumes
-  Scoring based on:
  - Sentence similarity
  - SpaCy keyword overlap
  - NLTK keyword overlap
-  React-based frontend for easy interaction
-  Backend proxy with Go Fiber to bridge React and Flask APIs

---

##  Tech Stack

| Layer      | Tools/Frameworks                      |
|------------|----------------------------------------|
| Frontend   | React, Tailwind CSS                    |
| Middleware | Go Fiber (`/api/upload`)               |
| Backend    | Python Flask + SentenceTransformers    |
| NLP        | SpaCy, NLTK                            |
| File Parsing | PyPDF2, docx2txt                     |

---




---

## ⚙️ How to Run

### 1. Clone the repo

```bash
git clone https://github.com/Kavyanegi0007/ATS-resume-screener.git
cd ATS-resume-screener


cd go-backend
go run main.go

cd ats
npm run dev

cd python-api
python app2.py

pip install -r requirements.txt


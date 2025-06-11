# ---------- top of file ----------
from flask import Flask, request, jsonify
import os, docx2txt
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define spaCy-based keyword extraction
def spacy_keywords(text):
    doc = nlp(text)
    return [token.text for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]

# Define NLTK-based keyword extraction
def nltk_keywords(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    return [word for word in words if word.lower() not in stop_words and word.isalpha()]

# shorthand so we don’t repeat long names
#spacy_kw   = nltk_spacy.spacy_keywords
#nltk_kw    = nltk_spacy.nltk_keywords
# ----------------------------------

# ---------------- helper ------------
def percent(numerator, denominator):
    """Return 0‑100 percentage as float; avoids ZeroDivisionError."""
    return 100.0 * numerator / denominator if denominator else 0.0
# ------------------------------------

def extract_text(file_path):
    """Try PDF → DOCX → TXT """
    if file_path.endswith('.pdf'):
        text = ""
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            text = ""
    elif file_path.endswith('.docx'):
        try:
            text = docx2txt.process(file_path)
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {e}")
            text = ""
    elif file_path.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading TXT {file_path}: {e}")
            text = ""
    
    return text
# ------------------------------------
def get_match_level(score):
    """
    Categorizes the match level based on cosine similarity.
    
    Args:
        score (float): Cosine similarity score between 0 and 1.

    Returns:
        str: "High", "Medium", or "Low" match level.
    """
    if score >= 0.75:
        return "High"
    elif score >= 0.5:
        return "Medium"
    else:
        return "Low"

app = Flask(__name__)
CORS(app)  
@app.route("/matcher", methods=['POST'])
def matcher():
    try:
        job_description = request.form.get("job_description", "").lower()
        resume_files    = request.files.getlist("resumes")

        if not job_description or not resume_files:
            return jsonify({"error": "Missing job description or resumes"}), 400

        jd_kw_spacy = set(spacy_keywords(job_description))
        jd_kw_nltk  = set(nltk_keywords(job_description))

        resumes_text, filenames, failed = [], [], []
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # ---------- extract text from each resume -------------
        for r in resume_files:
            if r.filename:
                path = os.path.join(app.config['UPLOAD_FOLDER'], r.filename)
                r.save(path)
                txt = extract_text(path).lower().strip()
                try: os.remove(path)        # clean‑up regardless of success/fail
                except: pass

                if txt:
                    resumes_text.append(txt)
                    filenames.append(r.filename)
                else:
                    failed.append(r.filename)

        if not resumes_text:
            return jsonify({"error": "Could not extract text from any resume"}), 400
        # -------------------------------------------------------

        # ----- TF‑IDF cosine (original logic) -----
        vectorizer   = TfidfVectorizer(stop_words='english', max_features=5000)
        tfidf_matrix = vectorizer.fit_transform([job_description] + resumes_text)
        sims         = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        # ------------------------------------------

        # ---------- build result objects ----------
        results = []
        for i, txt in enumerate(resumes_text):
            res_kw_spacy = set(spacy_keywords(txt))
            res_kw_nltk  = set(nltk_keywords(txt))

            spacy_olap = percent(len(res_kw_spacy & jd_kw_spacy), len(res_kw_spacy))
            nltk_olap  = percent(len(res_kw_nltk  & jd_kw_nltk),  len(res_kw_nltk))

            cosine_pct = round(float(sims[i] * 100), 2)

            results.append({
                "filename"      : filenames[i],
                "score"         : cosine_pct,       # TF‑IDF %
                "spacy_overlap" : round(spacy_olap, 2),
                "nltk_overlap"  : round(nltk_olap,  2),
                "match_level"   : get_match_level(sims[i]),
            })
        # ------------------------------------------

        results.sort(key=lambda x: x["score"], reverse=True)

        payload = {
            "matches"               : results,
            "total_resumes_processed": len(results),
            "job_description_length": len(job_description.split()),
        }
        if failed: payload["failed_files"] = failed

        return jsonify(payload), 200

    except Exception as e:
        return jsonify({"error": f"Server error: {e}"}), 500
if __name__ == '__main__':
    app.run(debug=True)

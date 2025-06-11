from flask import Flask, request, jsonify
import os
import docx2txt
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util


import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download resources if not already present
nltk.download('punkt')
nltk.download('stopwords')

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

def spacy_keywords(text):
    doc = nlp(text)
    keywords = [token.lemma_.lower() for token in doc 
                if token.pos_ in {"NOUN", "PROPN", "VERB"} 
                and not token.is_stop and token.is_alpha]
    return list(set(keywords))

def nltk_keywords(text):
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    keywords = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
    return list(set(keywords))


app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

app.config['UPLOAD_FOLDER'] = 'uploads/'  # Where resumes are saved

# ---------- Helper Functions ----------

def extract_text_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return text

def extract_text_docx(file_path):
    try:
        return docx2txt.process(file_path)
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        return ""

def extract_text_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading TXT {file_path}: {e}")
        return ""

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_txt(file_path)
    else:
        return ""
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
# ---------- API Endpoint ----------

@app.route("/matcher", methods=['POST'])
def matcher():
    try:
        job_description = request.form.get("job_description")
        resume_files = request.files.getlist("resumes")

        if not job_description or not resume_files:
            return jsonify({"error": "Missing job description or resumes"}), 400
        
        jd_kw_spacy = set(spacy_keywords(job_description))
        jd_kw_nltk  = set(nltk_keywords(job_description))

        resumes_text = []
        filenames = []
        failed_files = []


        # Create upload folder if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        for resume_file in resume_files:
            if resume_file.filename:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
                resume_file.save(filepath)
                
                extracted_text = extract_text(filepath)
                if extracted_text.strip():  # Only add if text was extracted
                    resumes_text.append(extracted_text)
                    filenames.append(resume_file.filename)
                else:
                    failed_files.append(resume_file.filename)
                
                # Clean up uploaded file
                try:
                    os.remove(filepath)
                except:
                    pass

        if not resumes_text:
            return jsonify({"error": "No text could be extracted from any resume files"}), 400
            

        # TF-IDF & Cosine Similarity
        vectorizer = TfidfVectorizer(
    stop_words='english',
    max_features=5000,)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode([job_description] + resumes_text, convert_to_tensor=True)
        sims = util.cos_sim(embeddings[0], embeddings[1:]).cpu().numpy().flatten()



    

        #tfidf_matrix = vectorizer.fit_transform([job_description] + resumes_text)
        #sims         = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        

        def pct(num, den): return round(100.0 * num / den, 2) if den else 0.0
        
        # Create results with all resumes, sorted by similarity score
        results = []
        for i, similarity in enumerate(sims):
            txt = resumes_text[i].lower()

            # NEW – résumé keywords
            res_kw_spacy = set(spacy_keywords(txt))
            res_kw_nltk  = set(nltk_keywords(txt))

            results.append({
    "filename": filenames[i],
    "score": round(float(similarity * 100), 2),  # Convert to percentage
    "match_level": get_match_level(similarity),
    "spacy_overlap": pct(len(res_kw_spacy & jd_kw_spacy), len(res_kw_spacy)),
    "nltk_overlap": pct(len(res_kw_nltk & jd_kw_nltk), len(res_kw_nltk)),
})

        
        # Sort by score (highest first)
        results.sort(key=lambda x: x["score"], reverse=True)
        response = {
            "matches"               : results,
            "total_resumes_processed": len(results),
            "job_description_length": len(job_description.split()),
        }
        if failed_files:
            response["failed_files"] = failed_files

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": f"Server error: {e}"}), 500

# ---------- Health Check ----------
@app.route("/health", methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Flask API is running"}), 200

# ---------- App Runner ----------
if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, host='0.0.0.0', port=5000) 
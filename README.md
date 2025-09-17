# ATS Resume Screener

A smart, AI-powered resume matching tool that evaluates candidate resumes against job descriptions using semantic similarity, keyword overlap, and advanced NLP techniques. Built with Flask, SentenceTransformers, and a React frontend to help recruiters and job seekers optimize resume-job matching.

![ATS Resume Screener](https://img.shields.io/badge/ATS-Resume%20Screener-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=flat-square)
![React](https://img.shields.io/badge/React-18+-blue?style=flat-square)
![Go](https://img.shields.io/badge/Go-1.19+-00ADD8?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

<img width="1366" height="722" alt="image" src="https://github.com/user-attachments/assets/3140b333-44ff-47fa-b343-e011ff9ee6dd" />
<img width="1351" height="637" alt="image" src="https://github.com/user-attachments/assets/28d81388-d250-4fcd-b2c7-817ae1ea43ac" />

## 🎯 Features

### Core Functionality
- **Semantic Matching**: Advanced similarity analysis using [SentenceTransformers](https://www.sbert.net/)
- **Multi-NLP Analysis**: Combines SpaCy and NLTK for comprehensive keyword extraction
- **Multiple File Formats**: Support for PDF, DOCX, and TXT resume formats
- **Intelligent Scoring**: Multi-layered scoring system for accurate matching

### Scoring Components
- **Sentence Similarity**: Deep semantic understanding of resume content vs job requirements
- **SpaCy Keyword Overlap**: Named Entity Recognition and linguistic analysis
- **NLTK Keyword Overlap**: Traditional keyword matching and frequency analysis
- **Weighted Scoring**: Configurable scoring weights for different matching criteria

### User Experience
- **React Frontend**: Modern, responsive user interface
- **Real-time Analysis**: Instant feedback on resume-job matching
- **Detailed Reports**: Comprehensive breakdown of matching scores
- **File Upload**: Drag-and-drop resume upload functionality

## 🏗️ Architecture

The system uses a multi-layer architecture for optimal performance and scalability:

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React, Tailwind CSS | User interface and interaction |
| **Middleware** | Go Fiber (/api/upload) | Request routing and file handling |
| **Backend** | Python Flask + SentenceTransformers | AI processing and analysis |
| **NLP Engine** | SpaCy, NLTK | Text processing and keyword extraction |
| **File Parser** | PyPDF2, docx2txt | Resume content extraction |

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │    │   Go Fiber       │    │  Python Flask   │
│   (Port 3000)   │◄──►│   Middleware     │◄──►│   Backend       │
│                 │    │   (Port 8080)    │    │   (Port 5000)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │  NLP Processing │
                                                │  • SpaCy        │
                                                │  • NLTK         │
                                                │  • Transformers │
                                                └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **Go 1.19+**
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kavyanegi0007/ATS-resume-screener.git
   cd ATS-resume-screener
   ```

2. **Set up Python Backend**
   ```bash
   cd python-api
   pip install -r requirements.txt
   ```

3. **Set up React Frontend**
   ```bash
   cd ats
   npm install
   ```

4. **Set up Go Middleware**
   ```bash
   cd go-backend
   go mod tidy
   ```

### Running the Application

**Start all services in separate terminals:**

1. **Python Flask Backend**
   ```bash
   cd python-api
   python app2.py
   ```
   *Runs on: http://localhost:5000*

2. **Go Fiber Middleware**
   ```bash
   cd go-backend
   go run main.go
   ```
   *Runs on: http://localhost:8080*

3. **React Frontend**
   ```bash
   cd ats
   npm run dev
   ```
   *Runs on: http://localhost:3000*

### Quick Launch Script

For convenience, create a `start.sh` script:
```bash
#!/bin/bash
echo "Starting ATS Resume Screener..."

# Start Python backend
cd python-api && python app2.py &
PYTHON_PID=$!

# Start Go middleware  
cd ../go-backend && go run main.go &
GO_PID=$!

# Start React frontend
cd ../ats && npm run dev &
REACT_PID=$!

echo "All services started!"
echo "Python Backend: http://localhost:5000"
echo "Go Middleware: http://localhost:8080" 
echo "React Frontend: http://localhost:3000"

# Wait for Ctrl+C
trap "kill $PYTHON_PID $GO_PID $REACT_PID" EXIT
wait
```

## 📋 Usage

### Web Interface

1. **Access the application** at `http://localhost:3000`
2. **Upload a resume** (PDF, DOCX, or TXT format)
3. **Paste or upload a job description**
4. **Click "Analyze"** to get the matching score
5. **Review the detailed results** showing:
   - Overall match percentage
   - Semantic similarity score
   - Keyword overlap analysis
   - Missing keywords suggestions
   - Improvement recommendations

### API Usage

#### Analyze Resume-Job Match

**Endpoint:** `POST /api/analyze`

**Request:**
```bash
curl -X POST http://localhost:8080/api/analyze \
  -H "Content-Type: multipart/form-data" \
  -F "resume=@resume.pdf" \
  -F "job_description=Software Engineer with Python and React experience..."
```

**Response:**
```json
{
  "overall_score": 85.2,
  "semantic_similarity": 0.78,
  "spacy_keywords": {
    "matched": ["Python", "React", "API", "Database"],
    "missing": ["Docker", "AWS", "Kubernetes"],
    "score": 0.82
  },
  "nltk_keywords": {
    "matched": ["software", "development", "engineering"],
    "missing": ["agile", "scrum", "testing"],
    "score": 0.75
  },
  "recommendations": [
    "Add Docker experience to your resume",
    "Include cloud platforms like AWS",
    "Mention agile methodologies"
  ]
}
```

## 🧠 AI/ML Components

### SentenceTransformers
- **Model**: `all-MiniLM-L6-v2` (default)
- **Purpose**: Generate semantic embeddings for resume and job description
- **Output**: Cosine similarity score between 0-1

### SpaCy NLP Pipeline
- **Components**: Tokenization, POS tagging, NER, Dependency parsing
- **Purpose**: Extract entities, skills, and technical terms
- **Models**: `en_core_web_sm` or `en_core_web_md`

### NLTK Processing
- **Features**: Tokenization, Stopword removal, Stemming/Lemmatization
- **Purpose**: Traditional keyword matching and frequency analysis
- **Methods**: TF-IDF, N-gram analysis

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Python Backend
FLASK_PORT=5000
FLASK_DEBUG=True

# Go Middleware
GO_PORT=8080
ALLOWED_ORIGINS=http://localhost:3000

# React Frontend
REACT_APP_API_URL=http://localhost:8080

# AI/ML Configuration
SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L6-v2
SPACY_MODEL=en_core_web_sm
SIMILARITY_THRESHOLD=0.7
MAX_FILE_SIZE=10MB

# Scoring Weights
SEMANTIC_WEIGHT=0.4
SPACY_WEIGHT=0.3
NLTK_WEIGHT=0.3
```

### Scoring Configuration

Adjust scoring weights in `python-api/config.py`:

```python
SCORING_CONFIG = {
    'semantic_weight': 0.4,
    'spacy_weight': 0.3,
    'nltk_weight': 0.3,
    'minimum_threshold': 0.6,
    'keyword_bonus': 0.1
}
```

## 📊 Performance Optimization

### Backend Optimization
- **Model Caching**: SentenceTransformers models are cached after first load
- **Batch Processing**: Process multiple resumes simultaneously
- **Async Processing**: Non-blocking operations for better throughput

### Frontend Optimization  
- **Code Splitting**: React lazy loading for better performance
- **File Upload**: Chunked upload for large files
- **Results Caching**: Cache analysis results for identical inputs

### Resource Requirements
- **RAM**: Minimum 4GB (8GB recommended for production)
- **CPU**: Multi-core recommended for parallel processing
- **Disk**: 2GB for models and dependencies

## 🧪 Testing

### Run Backend Tests
```bash
cd python-api
python -m pytest tests/ -v
```

### Run Frontend Tests
```bash
cd ats
npm test
```

### Integration Tests
```bash
# Test full pipeline
python tests/integration/test_full_pipeline.py
```

### Sample Test Cases
```python
def test_resume_analysis():
    resume_text = "Software engineer with 5 years Python experience..."
    job_desc = "Looking for Python developer with Django skills..."
    
    result = analyze_resume(resume_text, job_desc)
    
    assert result['overall_score'] > 0.7
    assert 'Python' in result['spacy_keywords']['matched']
    assert result['semantic_similarity'] > 0.6
```

## 🚀 Deployment

### Docker Deployment

1. **Create Dockerfile** for each service
2. **Use docker-compose** for orchestration

```yaml
version: '3.8'
services:
  python-backend:
    build: ./python-api
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production

  go-middleware:
    build: ./go-backend  
    ports:
      - "8080:8080"
    depends_on:
      - python-backend

  react-frontend:
    build: ./ats
    ports:
      - "3000:3000"
    depends_on:
      - go-middleware
```

### Cloud Deployment

**Recommended Platforms:**
- **AWS**: ECS, Lambda, S3 for file storage
- **Google Cloud**: Cloud Run, Cloud Storage
- **Azure**: Container Instances, Blob Storage
- **Vercel/Netlify**: For frontend deployment

### Production Considerations
- **Load Balancing**: Distribute requests across multiple instances
- **File Storage**: Use cloud storage for uploaded files
- **Monitoring**: Implement logging and monitoring
- **Security**: Add authentication and input validation

## 🔧 Troubleshooting

### Common Issues

1. **Model Loading Errors**
   ```bash
   # Download required models
   python -m spacy download en_core_web_sm
   python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
   ```

2. **CORS Issues**
   - Ensure Go middleware is running on port 8080
   - Check ALLOWED_ORIGINS in environment variables

3. **File Upload Failures**
   - Verify file size limits
   - Check supported file formats (PDF, DOCX, TXT)
   - Ensure proper MIME type detection

4. **Low Accuracy Scores**
   - Try different SentenceTransformer models
   - Adjust scoring weights
   - Fine-tune keyword extraction parameters

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Health Checks

Monitor service health:
```bash
# Check Python backend
curl http://localhost:5000/health

# Check Go middleware  
curl http://localhost:8080/health

# Check React frontend
curl http://localhost:3000
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Write tests for new features
- Update documentation as needed

## 📈 Roadmap

- [ ] **Advanced ML Models**: Integration with BERT, GPT for better understanding
- [ ] **Resume Builder**: AI-powered resume optimization suggestions
- [ ] **Batch Processing**: Upload and analyze multiple resumes
- [ ] **Analytics Dashboard**: Detailed matching statistics and insights
- [ ] **API Rate Limiting**: Production-ready API with proper limits
- [ ] **Database Integration**: Store analysis history and user data
- [ ] **Mobile App**: React Native mobile application
- [ ] **Real-time Collaboration**: Multi-user workspace for teams

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[SentenceTransformers](https://www.sbert.net/)** - For semantic similarity analysis
- **[SpaCy](https://spacy.io/)** - For advanced NLP processing  
- **[NLTK](https://www.nltk.org/)** - For traditional text processing
- **[React](https://reactjs.org/)** - For the frontend framework
- **[Go Fiber](https://gofiber.io/)** - For the middleware layer
- **[Tailwind CSS](https://tailwindcss.com/)** - For UI styling

## 📞 Contact & Support

- **Author**: Kavya Negi
- **GitHub**: [@Kavyanegi0007](https://github.com/Kavyanegi0007)
- **Project Link**: [ATS Resume Screener](https://github.com/Kavyanegi0007/ATS-resume-screener)

For support, please open an issue on GitHub or reach out through the project's discussion section.

---

⭐ **If you found this project helpful, please give it a star!**

🚀 **Ready to optimize your resume matching process? Get started now!**

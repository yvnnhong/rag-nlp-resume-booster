# RAG Resume Optimization Pipeline

An intelligent resume optimization system that uses Retrieval-Augmented Generation (RAG) and semantic similarity to match resumes against job descriptions, providing actionable feedback for improving job application success rates.

## Overview

This system combines advanced NLP techniques with vector embeddings to analyze resumes and job descriptions, offering detailed matching scores, missing skill identification, and ATS optimization recommendations.

## Features

- **Resume Parsing**: Extracts text from PDF resumes and segments into structured sections (experience, education, skills, projects)
- **Job Description Analysis**: Identifies required skills, preferred skills, experience levels, and other job requirements using regex patterns
- **Semantic Matching**: Uses sentence transformers and vector embeddings to calculate similarity scores between resume content and job requirements
- **ATS Scoring**: Evaluates resume optimization for Applicant Tracking Systems
- **Gap Analysis**: Identifies missing skills and provides actionable recommendations
- **Interactive Interface**: Gradio web interface for easy file uploads and results visualization

## Architecture

### Core Components

1. **PDF Extractor** (`src/parser/pdf_extractor.py`)
   - Extracts text from PDF resumes using PyMUPDF
   - Handles both file uploads and local file processing

2. **Text Processor** (`src/parser/text_processor.py`)
   - Cleans and normalizes extracted text
   - Removes formatting artifacts and standardizes structure
   - Generates multiple text versions for analysis

3. **Section Parser** (`src/parser/section_parser.py`)
   - Identifies resume sections using regex patterns
   - Extracts contact information and structured content
   - Calculates confidence scores for section detection

4. **Job Analyzer** (`src/database/job_analyzer.py`)
   - Parses job descriptions for requirements and skills
   - Identifies experience levels and education requirements
   - Extracts salary ranges and company information

5. **Vector Store** (`src/database/vector_store.py`)
   - Manages semantic similarity matching using sentence transformers
   - Implements ChromaDB for vector storage
   - Calculates overall match scores and generates recommendations

## Technology Stack

- **NLP**: spaCy (NER), NLTK, sentence-transformers, Hugging Face Transformers
- **ML Frameworks**: TensorFlow, PyTorch
- **Vector Databases**: ChromaDB, Pinecone
- **APIs**: OpenAI API, FastAPI
- **Data Processing**: pandas, NumPy, regex
- **File Processing**: PyMUPDF (fitz), PDF extraction
- **Interface**: Gradio, Streamlit
- **Infrastructure**: Docker, logging

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/rag-resume-optimization
cd rag-resume-optimization

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

## Usage

### Basic Usage

```python
from src.parser.pdf_extractor import PDFExtractor
from src.parser.text_processor import TextProcessor
from src.parser.section_parser import SectionParser
from src.database.job_analyzer import JobAnalyzer
from src.database.vector_store import VectorStore

# Initialize components
pdf_extractor = PDFExtractor()
text_processor = TextProcessor()
section_parser = SectionParser()
job_analyzer = JobAnalyzer()
vector_store = VectorStore()

# Process resume
resume_data = pdf_extractor.extract_text_disk("path/to/resume.pdf")
processed_text = text_processor.process_text(resume_data['full_text'])
sections = section_parser.parse_sections(processed_text['cleaned_text'])

# Analyze job description
job_requirements = job_analyzer.analyze_job_description(job_description_text)

# Generate match analysis
match_result = vector_store.match_resume_to_job(
    processed_text['cleaned_text'], 
    job_requirements
)

print(f"Overall Match Score: {match_result.overall_match_score:.2f}")
print(f"ATS Score: {match_result.ats_score:.2f}")
```

### Web Interface

```python
import gradio as gr

# Launch Gradio interface
# TODO: Add Gradio interface implementation
```

## Key Features

### Resume Analysis
- Extracts and categorizes resume sections
- Identifies technical skills using pattern matching
- Analyzes experience levels and education background
- Calculates text processing statistics

### Job Matching
- Semantic similarity scoring using vector embeddings
- Required vs. preferred skills analysis
- Experience level matching
- Missing skills identification

### Recommendations
- Actionable suggestions for resume improvement
- ATS optimization tips
- Keyword density analysis
- Skill gap identification

## Project Structure

```
rag-resume-optimization/
├── src/
│   ├── parser/
│   │   ├── pdf_extractor.py
│   │   ├── text_processor.py
│   │   └── section_parser.py
│   ├── database/
│   │   ├── job_analyzer.py #refactor + add spacy ner
│   │   └── vector_store.py #refactor
│   └── interface/
│       └── gradio_app.py # add dual upload w/ resume + job description 
├── data/
│   └── sample_resumes/
├── tests/
├── requirements.txt
└── README.md
```

## Sample Output

```
Job Analysis Summary for Software Engineer:
Industry: Technology
Experience Level: Mid (3+ years)
Required Skills: python, react, sql, aws, docker
Preferred Skills: kubernetes, tensorflow, pytorch
Education: Bachelor's degree in Computer Science
Salary: $80,000 - $120,000

Overall Match Score: 0.78
Skills Match: 85% of required skills found
Experience Match: Suitable level detected
ATS Score: 0.72

Recommendations:
- Add missing required skill: kubernetes
- Include exact job title "Software Engineer" in resume
- Highlight AWS and Docker experience more prominently
```

## Development Status

This project is actively under development. Core functionality is implemented including PDF processing, text analysis, and semantic matching. The Gradio interface and additional optimization features are in progress.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

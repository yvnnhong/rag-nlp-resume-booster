# Execution Flow

This document outlines the step-by-step execution flow when a resume PDF is processed through the system.

## Pipeline Overview

The system processes resumes through four main stages in the following order:

### 1. PARSER (First Stage)
Raw PDF processing and text extraction:
- **`pdf_extractor.py`** → Extract raw text from PDF file
- **`text_processor.py`** → Clean and normalize the extracted text
- **`section_parser.py`** → Identify and segment resume sections (Experience, Education, Skills, etc.)

### 2. MODELS (Second Stage)
Text vectorization and classification:
- **`embeddings.py`** → Convert text sections to vector embeddings
- **`classification.py`** → Classify and score different resume components (optional)

### 3. ANALYZER (Third Stage)
Multi-faceted resume analysis:
- **`content_analyzer.py`** → Analyze writing quality and content strength
- **`format_analyzer.py`** → Detect formatting issues and structural problems
- **`keyword_analyzer.py`** → Check ATS keyword optimization and density
- **`llm_analyzer.py`** → Generate detailed feedback using LLM

### 4. DATABASE (Concurrent with Stage 3)
Knowledge retrieval and context enhancement:
- **`vector_store.py`** → Query RAG system for relevant improvement tips
- **`knowledge_base.py`** → Retrieve best practices and industry standards

## Data Flow
```
PDF Upload → PARSER → MODELS → ANALYZER + DATABASE → Final Report
```

Each stage builds upon the previous one, with the DATABASE stage providing additional context during the analysis phase.
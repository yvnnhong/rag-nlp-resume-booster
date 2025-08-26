RAG-NLP-RESUME-BOOSTER/
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
│
├── src/
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py   # PDF text extraction
│   │   ├── text_processor.py  # Text cleaning & preprocessing
│   │   └── section_parser.py  # Resume section identification
│   │
│   ├── analyzer/
│   │   ├── __init__.py
│   │   ├── base_analyzer.py   # Base analyzer class
│   │   ├── content_analyzer.py # Content quality analysis
│   │   ├── format_analyzer.py  # Format & structure analysis
│   │   ├── keyword_analyzer.py # ATS keyword analysis
│   │   └── llm_analyzer.py    # LLM-based analysis
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── embeddings.py      # Text embeddings (sentence-transformers)
│   │   ├── classification.py  # PyTorch models for section classification
│   │   └── scoring.py         # Resume scoring models
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── vector_store.py    # ChromaDB/Pinecone integration
│   │   ├── knowledge_base.py  # Resume best practices RAG
│   │   └── schemas.py         # Data models/schemas
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py          # Logging configuration
│       ├── prompts.py         # LLM prompt templates
│       ├── validators.py      # Input validation
│       └── helpers.py         # Utility functions
│
├── interface/
│   ├── __init__.py
│   ├── gradio_app.py         # Main Gradio interface
│   ├── components.py         # Custom Gradio components
│   └── styles.py             # CSS styling
│
├── data/
│   ├── sample_resumes/       # Sample PDFs for testing
│   ├── knowledge_base/       # Resume best practices docs
│   └── processed/            # Processed/cached data
│
├── tests/
│   ├── __init__.py
│   ├── test_parser.py
│   └── test_integration.py
│
├── docs/
│   ├── troubleshooting.md
│   ├── execution_flow.md
│   └── deployment_guide.md

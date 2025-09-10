"""
vector_store.py
This vector store implementation handle: 
- Sentence transformer embeddings for semantic similarity 
-ChromaDB integration for vector storage 
-skills matching with exact, semantic, and contextual detection
-Experience level analysis based on years and role indicators
-ATS score calculation for keyword optimization
-comprehesive matching results complete with resume-boosting 
recommendations (e.x. skills/frameworks you should learn, 
areas of improvement, domain strength/weaknesses)
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Any, Optional
from sentence_transformers import SentenceTransformer
import chromadb 
from chromadb.config import Settings
import os
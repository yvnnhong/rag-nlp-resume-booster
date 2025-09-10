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
from sentence_transformers import SentenceTransformer #uses pytorch 
import chromadb 
from chromadb.config import Settings
import os

logger = logging.getLogger(__name__)
class MatchResult: 
    """Data class for storing match results."""
    def __init__(
        self, 
        skill: str, 
        similarity_score: float, 
        resume_text: str, 
        job_requirement: str, 
        match_type: str #'exact', 'semantic', 'partial'
    ):
        self.skill = skill
        self.similarity_score = similarity_score
        self.resume_text = resume_text
        self.job_requirement = job_requirement
        self.match_type = match_type

class ResumeJobMatch: 
    """Comprehensive matching results betwene resume and job."""
    def __init__(
        self,
        overall_match_score: float,
        skills_analysis: Dict[str, Any],
        experience_match: Dict[str, Any],
        missing_skills: List[str],
        matching_skills: List[MatchResult],
        recommendations: List[str],
        ats_score: float
    ):
        self.overall_match_score = overall_match_score
        self.skills_analysis = skills_analysis
        self.experience_match = experience_match
        self.missing_skills = missing_skills
        self.matching_skills = matching_skills
        self.recommendations = recommendations
        self.ats_score = ats_score

class VectoreStore: 
    """
    Handle embeddings and similarity matching for resume-job analysis.

    Sentence embedding: condenses an entire sentence's meaning into a 
    single vector. Sentences with similar meaning will have embeddings that 
    are "closer" together in a high-dimensional vector space

    Sentence transformer: a library and framework for creating high-quality 
    dense vector embeddings of sentences. Useful for enabling semantic 
    search.

    Embedding model: a ML model that converts text into vectors (embeddings)
    in a multi-dimensional space. These vectors capture the semantic meaning
    and relationships within the data.
    note: sentence transformer = a specific type of embedding model. 
    (sentence transformer models are a subset of embedding models.)
    Here, we use the pre-trained sentence transformer model 
    all-MiniLM-L6-v2 (designed for NLP tasks such as semantic search) 
    as our default embedding model, unless otherwise specified.

    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize vector store with sentence transformer model. 
        Args: model_name: HuggingFace model name for embeddings.

        HuggingFace: a python-based open-source library (platform) 
        where devs can share pre-traine ML models 
        """
        self.model_name = model_name
        self.embedding_model = None
        self.chroma_client = None
        self.collection = None
        
        #Similarity thresholds (using cosine similarity)
        self.exact_match_threshold = 0.95 #x >=0.95
        self.strong_match_threshold = 0.80 #0.80 <= x < 0.95
        self.moderate_match_threshold = 0.60 #0.60 <= x < 0.80

"""
vector_store.py
Focuses on ChromaDB operations and basic vector search. 

This vector store implementation handles: 
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
import re
from src.database.job_analyzer import JobRequirements

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
    """Comprehensive matching results between resume and job."""
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

class VectorStore: 
    """
    Handle embeddings and similarity matching for resume-job analysis.

    Sentence embedding: condenses an entire sentence's meaning into a 
    single vector. Sentences with similar meaning will have embeddings that 
    are "closer" together in a high-dimensional vector space

    Sentence transformer: a library and framework for creating high-quality 
    dense vector embeddings of sentences. Useful for enabling semantic 
    search.

    Embeddings: a specific type of vector that is learned through a ML model
    to capture the meaning + relationships within the original data. 
    Embeddings are almost always vectors, but not all vectors are embeddings.

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
        where devs can share pre-trained ML models 
        """
        self.model_name = model_name
        self.embedding_model = None
        self.chroma_client = None
        self.collection = None
        
        #Similarity thresholds (using cosine similarity)
        self.exact_match_threshold = 0.95 #x >=0.95
        self.strong_match_threshold = 0.80 #0.80 <= x < 0.95
        self.moderate_match_threshold = 0.60 #0.60 <= x < 0.80

        self._initialize_embedding_model()
        self._initialize_vector_database()

    def _initialize_embedding_model(self): 
        """Load the sentence transformer model."""
        try: 
            logger.info(f"Loading embedding model: {self.model_name}")
            self.embedding_model = SentenceTransformer(self.model_name)
            logger.info("Embedding model loaded successfully.")
        except Exception as e: 
            logger.error(f"Failed to load embedding mode: {str(e)}")
            raise 

    def _initialize_vector_database(self): 
        """Initialize ChromaDB for vector storage."""
        try: 
            #create chromadb client 
            #client = object that provides an interface to talk to the ChromaDB server
            #duckdb is the query engine; parquet is the storage format (a highly 
            #compressed, columnar format)
            #basically: we store the vector data in Parquet files, and we query it 
            #with Duckdb (this is local setup -- NOT cloud based, fast, + persistent 
            #b/c it survives between program runs b/c it's saved in ./vector_db)
            self.chroma_client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory="./vector_db"
            ))
            #create or get collection
            """
            get_or_create_collection(): 
            - if a collection with that name already exists, return it 
            - if it doesn't already exist, create a new one, then return it 
            """
            self.collection = self.chroma_client.get_or_create_collection(
                name="resume_job_matching",
                metadata={"description": "Resume and job requirement embeddings"}
            )
            logger.info("Vector database initialized successfully")
        except Exception as e: 
            logger.error(f"Failed to initialize vector database: {str(e)}")
            raise #re-raise to let the caller of the program know what went wrong
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray: 
        """
        Generate embeddings for a list of texts. 
        Args: 
        texts: List of text strings to embed
        returns: a numpy array of embeddings (nd = "n-dimensional")
        """
        try: 
            if not texts: 
                return np.array([])
            embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
        except Exception as e: 
            logger.error(f"Error generating embeddings: {str(e)}")
            return np.array([])
        
    def calculate_similarity(self, text1: str, text2: str) -> float: 
        """
        Calculate semantic similarity between two texts. 
        Args: 
        text1: first text
        text2: second text 
        Returns: a similarity score between 0 and 1 (using cosine similarity)
        """
        try: 
            embeddings = self.generate_embeddings([text1, text2])
            if len(embeddings) != 2: 
                return 0.0
            #compute cosine similarity
            #note: embedding1, embedding2 are 1d np arrays 
            embedding1, embedding2 = embeddings[0], embeddings[1] #unpack
            similarity = np.dot(embedding1, embedding2) / (
                np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
            )
            return float(similarity)
        except Exception as e: 
            logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0

    def match_resume_to_job(self, resume_text: str, job_requirements: Any) -> ResumeJobMatch: 
        """
        Main method to match resume against job requirements.
        Args: 
        resume_text: Cleaned resume text
        job_requirements: JobRequirements object from job_analyzer (imported at top)
        Returns: 
        ResumeJobMatch object
        """
        try: 
            logger.info("Starting resume-job matching analysis")
            #Extract resume skills and content 
            resume_skills = self._extract_resume_skills(resume_text)
            resume_experience = self._extract_experience_indicators(resume_text)
            #Analyze skills matching
            skills_analysis = self._analyze_skills_match(
                resume_skills, resume_text, job_requirements
            )
            #Analyze experience matching
            experience_match = self._analyze_experience_match(
                resume_experience, job_requirements
            )
            #Calculate overall scores 
            overall_score = self._calculate_overall_match_score(
                skills_analysis, experience_match
            )
            #Generate recommendations 
            recommendations = self._generate_recommendations(
                skills_analysis, experience_match, job_requirements
            )
            #Compute ATS score 
            ats_score = self._calculate_ats_score(
                resume_text, job_requirements
            )
            match_result = ResumeJobMatch(
                overall_match_score = overall_score, 
                skills_analysis = skills_analysis,
                experience_match = experience_match,
                missing_skills = skills_analysis['missing_skills'],
                matching_skills = skills_analysis['matching_skills'],
                recommendations=recommendations,
                ats_score=ats_score
            )
            logger.info(f"Matching analysis complete. Overall score: {overall_score: .2f}")
            return match_result
        except Exception as e: 
            logger.error(f"Error in resume-job matching: {str(e)}")
            return self._empty_match_result()
        
    def _extract_resume_skills(self, resume_text: str) -> List[str]: 
        """Extract skills mentioned in resume. """
        skill_patterns = [
            r'\b(?:python|java|javascript|typescript|c\+\+|c#|go|rust|php|ruby|swift|kotlin)\b',
            r'\b(?:react|angular|vue|django|flask|spring|express|node\.?js)\b',
            r'\b(?:mysql|postgresql|mongodb|redis|elasticsearch)\b',
            r'\b(?:aws|azure|gcp|docker|kubernetes|git|jenkins)\b',
            r'\b(?:machine learning|ai|nlp|deep learning|data science)\b',
            r'\b(?:html|css|sql|nosql|rest|api|microservices)\b'
        ]
        skills = set()
        resume_lower = resume_text.lower()
        for pattern in skill_patterns: 
            matches = re.findall(pattern, resume_lower, re.IGNORECASE)
            skills.update(matches)
        return list(skills)
    
    def _extract_experience_indicators(self, resume_text: str) -> Dict[str, Any]: 
        """Extract experience indicators from resume"""
        experience_info = {
            'years_mentioned': [],
            'roles': [],
            'companies': [],
            'estimated_years': 0
        }

            
    




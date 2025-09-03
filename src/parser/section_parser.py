#section_parser.py is step 3 to parse individual sections (e.x education, work history, etc)
import re
import logging
from typing import Dict, List, Optional, Any 

logger = logging.getLogger(__name__)

class ResumeSection: 
    """Data class to represent a parsed resume section."""
    def __init__(self, name: str, content: str, start_index: int, end_index: int, 
                 confidence: float) -> None: 
        self.name = name
        self.content = content
        self.start_index = start_index
        self.end_index = end_index
        self.confidence = confidence

class SectionParser:
    """Parse resume text into distinct sections."""
    def __init__self(self): #Define common section headers and their variations.
        self.section_patterns: Dict[str, List[str]] = {
            'contact': [
                r'contact\s+information',
                r'personal\s+information',
                r'contact\s+details?'
            ],
            'summary': [
                r'professional\s+summary',
                r'career\s+summary',
                r'summary\s+of\s+qualifications?',
                r'summary',
                r'profile',
                r'objective',
                r'career\s+objectives?'
            ],
            'experience': [
                r'professional\s+experience',
                r'work\s+experience',
                r'employment\s+history',
                r'experience',
                r'career\s+history',
                r'work\s+history'
            ],
            'education': [
                r'education',
                r'educational\s+background',
                r'academic\s+background',
                r'qualifications?'
            ],
            'skills': [
                r'technical\s+skills?',
                r'core\s+competencies',
                r'skills?\s+and\s+abilities',
                r'skills?',
                r'competencies',
                r'technologies',
                r'languages', #make a section for programming languages??? 
                r'programming\s+languages?'
            ],
            'projects': [
                r'projects?',
                r'key\s+projects?',
                r'selected\s+projects?',
                r'notable\s+projects?'
            ],
            'certifications': [
                r'certifications?',
                r'licenses?\s+and\s+certifications?',
                r'professional\s+certifications?',
            ],
            'achievements': [
                r'achievements?',
                r'accomplishments?',
                r'awards?\s+and\s+honou?rs?',
                r'awards?',
                r'recognition'
            ]
        }

        #Compile regex patterns for improved performance
        self.compiled_patterns = {}
        for section, patterns in self.section_patterns.items(): 
            self.compiled_patterns[section] = []
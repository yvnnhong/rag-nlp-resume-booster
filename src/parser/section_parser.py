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
        #pipe | means to combine both flags 
        self.compiled_patterns = {}
        for section, patterns in self.section_patterns.items(): 
            self.compiled_patterns[section] = []
            for pattern in patterns: 
                compiled_pattern = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
                self.compiled_patterns[section].append(compiled_pattern)

    def parse_sections(self, resume_text: str) -> Dict[str, Any]: 
        """
        Parses resume text into sections. 
        Args: resume_text (str): Full resume text 
        Returns: dict: Parsed section w/ metadata 
        """
        try: 
            #step 1: Clean text 
            cleaned_text = self._clean_text(resume_text)
            #step 2: find section boundaries 
            section_matches = self._find_section_boundaries(cleaned_text)
            #step 3: extract section content 
            parsed_sections = self._extract_section_content(cleaned_text, section_matches)
            #step 4: extract contact information (usually at the top)
            contact_info = self._extract_contact_info(cleaned_text)
            result = {
                'sections': parsed_sections,
                'contact_info': contact_info,
                'total_sections': len(parsed_sections),
                'text_length': len(cleaned_text),
                'parsing_status': 'success'
            }
            logger.info(f"Successfully parsed {len(parsed_sections)} sections")
            return result
        #exception 
        except Exception as e: 
            logger.error(f"Error parsing resume sections: {str(e)}")
            if resume_text: 
                text_length = len(resume_text)
            else: 
                text_length = 0
            return {
                'sections': {},
                'contact_info': {},
                'total_sections': {},
                'text_length': text_length,
                'parsing_status': 'failed',
                'error': str(e)
            }
        
    def _clean_text(self, text: str) -> str: 
        """Clean and normalize resume text."""
        return ''
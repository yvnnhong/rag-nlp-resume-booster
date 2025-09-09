import re 
import logging
from typing import Dict, List, Set, Any, Optional

logger = logging.getLogger(__name__)
class JobRequirements: 
    """Class to store extracted job requirements."""
    def __init__(
        self, 
        required_skills: List[str], 
        preferred_skills: List[str],
        experience_years: Optional[int],
        experience_level: str, #entry, mid, senior, executive
        education_requirements: List[str],
        certifications: List[str],
        responsibilities: List[str],
        company_info: Dict[str, str], 
        salary_range: Optional[str],
        job_title: str,
        industry: str
    ):
        self.required_skills = required_skills
        self.preferreed_skills = preferred_skills
        self.experience_years = experience_years
        self.experience_level = experience_level
        self.education_requirements = education_requirements
        self.certifications = certifications
        self.responsibilities = responsibilities
        self.company_info = company_info
        self.salary_range = salary_range
        self.job_title = job_title
        self.industry = industry

class JobAnalyzer: 
    """Extract and analyze requirements from job descriptions"""
    def __init__(self): 
        self.tech_skills_patterns = {
            'programming_languages': [ #pipe '|' means "any one of these can match" (match one at a time)
                r'\b(?:python|java|javascript|typescript|c\+\+|c#|go|rust|php|ruby|swift|kotlin|scala|r|matlab)\b',
                r'\b(?:html|css|sql|nosql|bash|powershell)\b'
            ]
        }
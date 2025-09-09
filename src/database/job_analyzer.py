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
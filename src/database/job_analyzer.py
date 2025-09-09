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
            ],
            'frameworks': [
                r'\b(?:react|angular|vue|django|flask|spring|express|laravel|rails|pytorch|tensorflow)\b',
                r'\b(?:node\.?js|next\.?js|nuxt\.?js)\b'
            ],
            'databases': [
                r'\b(?:mysql|postgresql|mongodb|redis|elasticsearch|cassandra|dynamodb|sqlite)\b',
                r'\b(?:oracle|sql\s+server|mariadb)\b'
            ],
            'cloud_platforms': [
                r'\b(?:aws|azure|gcp|google\s+cloud|amazon\s+web\s+services)\b',
                r'\b(?:docker|kubernetes|terraform|ansible)\b'
            ],
            'tools': [
                r'\b(?:git|github|gitlab|jira|confluence|slack|figma|sketch)\b',
                r'\b(?:jenkins|circleci|travis|ci/cd)\b'
            ]
        }
        #Experience level indicators
        self.experience_indicators = {
            'entry': [r'entry\s+level', r'junior', r'0-2\s+years', r'new\s+grad', r'recent\s+graduate'],
            'mid': [r'mid\s+level', r'2-5\s+years', r'3-6\s+years', r'intermediate'],
            'senior': [r'senior', r'5\+\s+years', r'6\+\s+years', r'7\+\s+years', r'lead', r'principal'],
            'executive': [r'director', r'vp', r'vice\s+president', r'c-level', r'chief', r'head\s+of']
        }
        #Education patterns: 
        self.education_patterns = [
            r"bachelor[']?s?\s+(?:degree\s+)?(?:in\s+)?([a-zA-Z\s]+)",
            r"master[']?s?\s+(?:degree\s+)?(?:in\s+)?([a-zA-Z\s]+)",
            r"phd\s+(?:in\s+)?([a-zA-Z\s]+)",
            r"(?:bs|ba|ms|ma|mba)\s+(?:in\s+)?([a-zA-Z\s]+)"
        ]
        #Certification patterns -- note: in re.findall, MUST include the IGNORECASE flag
        self.certification_patterns = [
            r'aws\s+certified\s+([a-zA-Z\s-]+)',
            r'google\s+cloud\s+([a-zA-Z\s-]+)',
            r'microsoft\s+certified\s+([a-zA-Z\s-]+)',
            r'cissp|cism|cisa|comptia\s+([a-zA-Z\s+]+)',
            r'pmp|scrum\s+master|agile\s+certified'
        ]

    def analyze_job_description(self, job_text: str) -> JobRequirements: 
        """
        Main method to extract requirements from job description.
        Args: job_text (str): Raw job description text
        Returns: JobRequirements object 
        """
        jq = JobRequirements()
        return jq #temp


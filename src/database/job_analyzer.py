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
        try: 
            #Step 1: Clean and normalize text
            cleaned_text = self._clean_job_text(job_text)
            #Step 2: Extract different components: 
            job_title = self._extract_job_title(cleaned_text)
            company_info = self._extract_company_info(cleaned_text)
            required_skills = self._extract_required_skills(cleaned_text)
            preferred_skills = self._extract_preferred_skills(cleaned_text)
            experience_info = self._extract_experience_requirements(cleaned_text)
            education_reqs = self._extract_education_requirements(cleaned_text)
            certifications = self._extract_certifications(cleaned_text)
            responsibilities = self._extract_responsibilities(cleaned_text)
            salary_range = self._extract_salary_range(cleaned_text)
            industry = self._extract_industry(cleaned_text)

            requirements = JobRequirements(
                job_title=job_title,
                company_info=company_info,
                required_skills=required_skills,
                preferred_skills=preferred_skills,
                experience_years=experience_info['years'],
                experience_level=experience_info['level'],
                education_requirements=education_reqs,
                certifications=certifications,
                responsibilities=responsibilities,
                salary_range=salary_range,
                industry=industry
            )
            logger.info(f"Successfully analyzed job description for {job_title}.")
            return requirements
        except Exception as e: 
            logger.error(f"Error anlayzing job description: {str(e)}")
            #Next, return empty JobRequirements object
            return JobRequirements(
                job_title="Unknown",
                company_info={},
                required_skills=[],
                preferred_skills=[],
                experience_years=None,
                experience_level="unknown",
                education_requirements=[],
                certifications=[],
                responsibilities=[],
                salary_range=None,
                industry="unknown"
            )
        
    def _clean_job_text(self, text: str) -> str: 
        """Clean and normalize job description text."""
        if not text: 
            return ""
        #Remove excessive whitespace -- re.sub(pattern, replacement, string)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    
    def _extract_job_title(self, text: str) -> str: 
        """Extract job title from the job description."""
        #note: this is very generic; have to add more patterns/variations later 
        #or use semantic search???? 
        #yes. USE SEMANTIC SEARCH ALSKDFALKSJ
        title_patterns = [ #carat ^ means "any char EXCEPT FOR"
            r'(?:job\s+title|position|role):\s*([^\n]+)',
            r'we\s+are\s+looking\s+for\s+(?:a\s+)?([^\n]+?)(?:\s+to\s+)',
            r'seeking\s+(?:a\s+)?([^\n]+?)(?:\s+to\s+|\s+who\s+)',
        ]
        for pattern in title_patterns: 
            match = re.search(pattern, text, re.IGNORECASE)
            if match: 
                return match.group(1).strip().title()
        #Default fallback 
        return "Software engineer"
    
    def _extract_company_info(self, text: str) -> Dict[str, str]: 
        """Extract company information"""
        company_info = {}
        company_patterns = [
            r'(?:company|organization):\s*([^\n]+)',
            r'(?:join|work\s+at)\s+([A-Z][a-zA-Z\s]+)(?:\s+as\s+|\s+to\s+)',
        ]
        for pattern in company_patterns: 
            match = re.search(pattern, text, re.IGNORECASE)
            if match: 
                company_info['company_name'] = match.group(1).strip()
                break
        return company_info
    
    def _extract_required_skills(self, text: str) -> List[str]: 
        return List[str] #temp


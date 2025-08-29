#text_processor.py is step 2 for cleaning and normalizing the text 
#we want to clean and normalize the raw extracted text before trying to parse 
#sections from it 
import re #for regex (re = regular expression)
import string 
import logging 
from typing import Dict, List, Optional, Any
import unicodedata #to normalize unicode strings e.x. remove accents 

logger = logging.getLogger(__name__)

class TextProcessor: 
    def __init__(self):
        self.resume_stopwords = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'can', 'shall', 'this', 'that', 'these', 'those'
        }
        #common resume formatting artifacts to clean
        #r denotes raw string 
        self.formatting_artifacts = {
            r'•\s*',  # Bullet points
            r'○\s*',  # Hollow bullets
            r'▪\s*',  # Square bullets  
            r'‣\s*',  # Triangular bullets
            r'[\u2022\u2023\u25E6\u2043\u2219]\s*',  # Unicode bullets
            r'^\s*[-*]\s+',  # Dash/asterisk bullets
            r'\f',  # Form feed characters
            r'\r',  # Carriage returns
        }
        #compile regex patterns for performance 
        #note: (pattern, re.MULTILINE) -> "look for this pattern @ the beginning of EVERY line",
        #not just the start of the text block 
        self.compiled_artifacts = []
        for pattern in self.formatting_artifacts: 
            compiled_pattern = re.compile(pattern, re.MULTILINE)
            self.compiled_artifacts.append(compiled_pattern)




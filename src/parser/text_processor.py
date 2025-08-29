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
        #r denotes raw string literal -- don't read escape sequences; just read it LITERALLY
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
        #not just  at the start of the text block 
        self.compiled_artifacts = []
        for pattern in self.formatting_artifacts: 
            compiled_pattern = re.compile(pattern, re.MULTILINE)
            self.compiled_artifacts.append(compiled_pattern)

    #main text processing pipeline
    #raw_text = raw extracted text from pdf 
    def process_text(self, raw_text: str) -> Dict[str, Any]:
        try: 
            if not raw_text or not raw_text.strip(): 
                return self._empty_result("Empty input text. Unable to process")
            #initiate 6-step text processing pipeline! 
            #step 1: basic cleaning 
            cleaned_text = self._basic_clean(raw_text)
            #step 2: remove formatting artifacts 
            deformatted_text = self._remove_formatting_artifacts(cleaned_text)
            #step 3: normalize whitespace and structure 
            normalized_text = self._normalize_structure(deformatted_text)
            #step 4: extract and clean individual words 
            words = self._extract_words(normalized_text)
            cleaned_words = self._clean_words(words)
            #step 5: generate processsed versions 
            processed_versions = self._generate_versions(normalized_text, cleaned_words)
            #step 6: calculate text statistics 
            stats = self._calculate_stats(raw_text, normalized_text, cleaned_words)
            result = {
                'original_text': raw_text,
                'cleaned_text': normalized_text,
                'processed_versions': processed_versions,
                'words': cleaned_words, 
                'stats': stats,
                'processing_status': 'success'
            }
            logger.info(f"Text processing successful. Original: {len(raw_text)} chars, " 
                        f"\nCleaned: {len(normalized_text)} chars")
            return result 
        except Exception as e: 
            logger.error(f"Error processing text: {str(e)}")
            if raw_text: 
                original_text = raw_text
            else: 
                original_text = ''
            return {
                'original_text': original_text,
                'cleaned_text': '',
                'processed_versions': {},
                'words': [], 
                'stats': {},
                'processing_status': 'failed',
                'error': str(e)
            }
    
    #perform basic text cleaning 
    def _basic_clean(self, text: str) -> str: 
        #normalize unicode characters 
        #'NFKD' = compatibility decomposition (break chars down into their basic parts)
        #^(e.x. The character “é” can be decomposed into “e” + “´” (accent).)
        text = unicodedata.normalize('NFKD', text)






    #note- underscore prefix denotes a private method 







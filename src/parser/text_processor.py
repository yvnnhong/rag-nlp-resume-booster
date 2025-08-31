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
    
    #note- underscore prefix denotes a private method 

    #perform basic text cleaning 
    def _basic_clean(self, text: str) -> str: 
        #normalize unicode characters 
        #'NFKD' = compatibility decomposition (break chars down into their basic parts)
        #^(e.x. The character “é” can be decomposed into “e” + “´” (accent).)
        text = unicodedata.normalize('NFKD', text)
        #remove null bytes and other control characters 
        new_text_chars = []
        for char in text: 
            #ord(char) gets the unicode code point of the char 
            code_point = ord(char)
            #the stuff below 32 isn't printable (controls)
            #code 10 = "\n"; code 9 = "\t" --we want these 
            if code_point >= 32 or char == '\n' or char == '\t':
                new_text_chars.append(char)
        text = ''.join(new_text_chars)
        #fix word breaks and hyphenated words across newlines 
        text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text) #fix hyphenated line breaks 
        text = re.sub(r'(\w)\s*\n\s*(\w)', r'\1 \2', text) #fix word breaks across lines 
        return text 
    
    #remove common resume formatting artifacts e.x. bullet points, excessive punctuation,
    #page numbers, etc. 
    def _remove_formatting_artifacts(self, text: str) -> str: 
        #return an empty string if input text is None, "", or otherwise empty 
        if not text:
            return ""
        #remove bullet points and formatting (replace w/ empty string aka delete them)
        for pattern in self.compiled_artifacts: 
            text = pattern.sub('', text)

        #remove excessive punctuation
        #1) replace 3 or more periods with just 3 periods. [.] denotes the period character class
        #note: the period is special (it is a wildcard that can match any character)
        #so we have to escape it either using \. or w a charater class like [.]
        text = re.sub(r'[.]{3,}', '...', text)
        #2) replace 3 or more hyphens with just 3 hyphens. [-] denotes the hyphen character class
        text = re.sub(r'-{3,}', '---', text)
        #3) replace 3 or more underscores with just 3 underscores. ^^
        text = re.sub(r'_{3,}', '___', text)

        #remove page numbers and headers/footers
        #Note: uses bitwise OR to combine multiple flags. 
        text = re.sub(r'^\s*Page\s+\d+.*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
        text = re.sub(r'^\s*\d+\s*/\s*\d+\s*$', '', text, flags=re.MULTILINE)
        return text 
    
    #Normalize whitespace and text structure 
    def _normalize_structure(self, text: str) -> str: 
        if not text: 
            return ""
        #normalize line breaks 
        text = re.sub(r'\n{3,}', '\n\n', text) #max 2 consecutive newlines 
        text = re.sub(r'\n\s+\n', '\n\n', text) #remove whitespace-only lines 

        #normalize spacing 
        text = re.sub(r'[ \t]{2,}', ' ', text) #multiple spaces to single space 
        text = re.sub(r'[ \t]*\n[ \t]*', '\n', text) #remove spaces below and above newlines
        
        #normalize punctuation spacing 
        text = re.sub(r'\s+([,.;:!?])', r'\1', text) #remove space before punctuation
        text = re.sub(r'([,.;:!?])\s*', r'\1 ', text) #ensure space after punctuation

        #remove duplicate punctuation/collapse repeated or mixed punctuation into one
        text = re.sub(r'([,.;:!?])([,.;:!?])', r'\1', text)
        
        return text.strip()
    
    #extract individual words from text 
    def _extract_words(self, text: str) -> List[str]:
        if not text:
            return []
        #extract words (including hyphenated words and acronyms)
        word_pattern = r'\b[a-zA-Z]+(?:[-\'][a-zA-Z]+)*\b|\b[A-Z]{2,}\b|\b\w+\b'
        words = re.findall(word_pattern, text)
        return words

    #clean and filter word list 
    def _clean_words(self, words: List[str]) -> List[str]:
        if not words:
            return []
        cleaned = []
        for word in words: 
            clean_word = word.lower().strip()
            if not clean_word: #skip empty words 
                continue 
            if len(clean_word) == 1 and clean_word not in {'c', 'r', 'a', 'i'}: 
                continue 
            if clean_word.isdigit(): #skip pure numbers 
                continue 
            if clean_word in self.resume_stopwords and not self._is_technical_term(clean_word): 
                continue
            cleaned.append(word)
        return cleaned 
    
    #helper method to check to see if a word is likely a technical term that we want to preserve 
    #note: we have to expand this definition later(add the list to /data)
    #this entire function is probably gonna be refactored later 
    #REFACTOR THISSS LATERRRRRRRR DONT FORGETTTT
    #note: technical_indicators looks something like [True, False, False] -- a list of bools
    def _is_technical_term(self, word: str) -> bool: 
        technical_indicators = [
            len(word) > 2 and word.isupper(), #e.x. acronymns like SQL, API 
            any(char.isdigit() for char in word), #version numbers like C#, HTML5
            word in {'c', 'r', 'go', 'rust'} #programming languages 
        ]
        return any(technical_indicators) #checks if any of these conditions are true

    #generate different processed versions of the text 
    def _generate_versions(self, cleaned_text: str, words: List[str]) -> Dict[str, str]: 
        versions = {}
        #all-lowercase version 
        versions['lowercase'] = cleaned_text.lower()
        #Words only (space-separated)
        versions['words_only'] = ' '.join(words)
        #no punctuation marks version
        translator = str.maketrans('', '', string.punctuation) #create translator object 
        '''
        '''


     
    
        





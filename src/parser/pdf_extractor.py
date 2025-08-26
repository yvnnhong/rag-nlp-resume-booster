import fitz #to handle opening PDF files and extracting text from them (aka PyMUPDF)
import logging 
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class PDFExtractor:
    def __init__(self): 
        self.supported_formats = ['.pdf']

    def extract_text(self, pdf_path: str) -> Optional[Dict[str, Any]]: 
        try:
            if not Path(pdf_path).exists(): 
                logger.error(f"File not found: {pdf_path}")
                return None
            if not pdf_path.lower().endswith('.pdf'):
                logger.error(f"This is unsupported file format: {pdf_path}")
                return None
            doc = fitz.open(pdf_path)
            #initialize variables for text extraction
            full_text = ""
            page_texts = [] 
            #^for entry level, resumes are usually only 1 page -- relevant for knowledge_base
            for page_num in range(doc.page_count): 
                page = doc[page_num]
                page_text = page.get_text()
                page_texts.append(page_text)
                full_text += page_text + "\n"
            #Close the document 
            doc.close()
            result = {
                'full_text': full_text.strip(), 
                #.strip() removes leading and trailing whitespace from text 
                'page_texts': page_texts,
                'page_count': len(page_texts),
                'char_count': len(full_text),
                'file_name': Path(pdf_path).name,
                'extraction_status': 'success'
            }
            logger.info(f"Successfully extracted text from {pdf_path}")
            logger.info(f"Pages: {result['page_count']}, Characters: {result['char_count']}")
            return result 

#test_text_processor.py is for testing src/parser/text_processor.py

import logging
import sys
sys.path.append('.')
from src.parser.text_processor import TextProcessor
from src.parser.pdf_extractor import PDFExtractor

#Test text processing using pdf files from root/data/sample_resumes
def test_text_processing_from_files():
    print("=" * 60)
    print("Testing text processing from PDF files.")
    print("=" * 60)
    test_processor = TextProcessor()
    pdf_extractor = PDFExtractor()
    pass #temp 







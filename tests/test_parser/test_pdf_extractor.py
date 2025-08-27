import logging
import sys
sys.path.append('../../src') #go up two levels 
from src.parser.pdf_extractor import PDFExtractor

def test_pdf_extraction():
    extractor = PDFExtractor()


import logging
import sys
sys.path.append('.')
from src.parser.pdf_extractor import PDFExtractor
from src.parser.text_processor import TextProcessor
from src.parser.section_parser import SectionParser

def test_section_parsing_full_pipeline(): 
    """Test section parser using the full pipeline: 
    PDF Extraction -> Text Processing -> Section Parsing"""
    print("=" * 70)
    print("Testing Section Parser -- Full Pipeline")
    print("=" * 70)
    #initialize all processors.
    pdf_extractor = PDFExtractor()
    text_processor = TextProcessor()
    section_parser = SectionParser()

    test_files = [
        ("data/sample_resumes/standard_1pg_resume.pdf", "Standard 1-Page Resume"),
        ("data/sample_resumes/long_resume_6pgs.pdf", "Long 6-Page Resume"),
        ("data/sample_resumes/sparse_resume.pdf", "Sparse 1-Page Resume")
    ]

    for file_path, test_name in test_files: 
        print(f"\n--- Testing {test_name} ---")
        try: 
            #Step 1: extract text from pdf 
            pdf_result = pdf_extractor.extract_text_disk(file_path)
            if not pdf_result or pdf_result['extractor_status'] != 'success':
                print(f"Failed to extract text from {file_path}")
                continue 
            #Step 2: Process the extracted text
            processing_result = text_processor.process_text(pdf_result['full_text'])
            if processing_result['processing_status'] != 'success': 
                print(f"Failed to process text: {processing_result.get('error', 'Unknown error')}")
                continue
            #Step 3: parse sections from processed text 
            section_result = section_parser.parse_sections(processing_result['cleaned_text'])
            #keep writingfrom here 
            pass #temp
        except Exception as e: 
            print(f"")
            pass

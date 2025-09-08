import logging
from typing import Dict, Any
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
            section_result: Dict[str, Any] = section_parser.parse_sections(processing_result['cleaned_text'])
            if section_result['parsing_status'] == 'success': 
                print(f"Section parsing successful.")
                print(f"Sections found: {section_result['total_sections']}")
                #show corresponding confidence scores.
                for section_name, section_obj in section_result['sections'].items():
                    print(f"{section_name.title()}: {len(section_obj.content)} "
                          f"total chars (confidence: {section_obj.confidence:.2f})")
                #Show contact info
                contact = section_result['contact_info']
                found_contact = []
                for k, v in contact.items(): 
                    if v: 
                        found_contact.append(f"{k}: {v}")
                if found_contact: 
                    print(f"Contact info: {', '.join(found_contact)}")
                else:
                    print("No contact info found.")
                #Show preview of each section: 
                print(f"\nSection content previews: ")
                for section_name, section_metadata in section_result['sections'].items(): 
                    preview = section_metadata.content[:100].replace('\n', ' ').strip()
                    if preview: 
                        print(f"{section_name}: {preview}...")
                    else:
                        print(f"{section_name}: [No content]")
            else: 
                print(f"Section parsing failed: {section_result.get('error', 'Unknown error')}")
        except Exception as e: 
            print(f"Pipeline test failed with error: {str(e)}")

def test_section_parsing_with_sample_text(): 
    pass
            
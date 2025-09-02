#test_text_processor.py is for testing src/parser/text_processor.py
import logging
import sys
sys.path.append('.')
from src.parser.text_processor import TextProcessor
from src.parser.pdf_extractor import PDFExtractor

#test a single PDF file from root/data/sample_resumes
def test_single_file_text_processing(pdf_extractor, text_processor, file_path, test_name): 
    print(f"\nTesting {test_name}: ")
    try: 
        #test pdf extraction: 
        pdf_result = pdf_extractor.extract_text_disk(file_path)
        if not pdf_result or pdf_result['extraction_status'] != 'success': 
            if pdf_result: 
                error_message = pdf_result.get('error', 'Unknown error')
            else: 
                error_msg = "No result"
            print(f"PDF extraction failed: {error_msg}.")
            return False
        #process extracted text: 
        processing_result = text_processor.process_text(pdf_result['full_text'])
        if processing_result['processing_status'] == 'success': 
            print("Test processing is successful.")
            summary = text_processor.get_summary
        
    except Exception as e: 
        pass #temp

#Test text processing using all pdf files from root/data/sample_resumes
def test_text_processing_all_pdfs_sample_resumes():
    print("=" * 60)
    print("Testing text processing from PDF files.")
    print("=" * 60)
    test_processor = TextProcessor()
    pdf_extractor = PDFExtractor()
    test_files = [
        (""),
        (""),
        ("")
    ]
    pass #temp 







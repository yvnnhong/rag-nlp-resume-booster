import logging
import sys
sys.path.append('../../src') #go up two levels 
from src.parser.pdf_extractor import PDFExtractor

def test_single_resume_file_disk(extractor, file_path, test_name):
    print(f"\nTesting {test_name}")
    result = extractor.extract_text_disk(file_path)
    if result and result['extraction_status'] == 'success': 
        print(f"Extraction is successful.")
        print(f"File name: {result['file_name']}")
        print(f"Total number of Pages: {result['page_count']}")
        print(f"Total number of characters: {result['char_count']}")
        print(f"First 150 chars: {result['full_text'][:150]}...")
        return True 
    else: 
        if result and 'error' in result:
            error_msg = result['error']
        else: 
            error_msg = 'Unknown error'
        print(f"(Disk) Extraction failed: {error_msg}")
        return False
    
def test_single_resume_file_bytes(extractor, file_path, test_name):
    print(f"\nTesting {test_name} using the bytes method.")
    try:
        with open(file_path, 'rb') as file: #open pdf in binary read mode ('rb')
            pdf_bytes = file.read()
        result = extractor.extract_from_bytes(pdf_bytes, filename=file_path.split('/')[-1])
        if result and result['extraction_status'] == 'success': 
            print(f"Bytes extraction is successful.")
            print(f"File name: {result['file_name']}")
            print(f"Total number of Pages: {result['page_count']}")
            print(f"Total number of characters: {result['char_count']}")
            print(f"First 150 chars: {result['full_text'][:150]}...")
            return True
        else: 
            if result and 'error' in result: 
                error_msg = result['error']
            else: 
                error_msg = 'Unknown error'
            print(f"Bytes Extraction failed: {error_msg}")
            return False
    except FileNotFoundError: 
        print(f"File not found: {file_path}")
        return False
    
def test_all_resumes():
    extractor = PDFExtractor()
    test_files = [
        
    ]




#This file, test_text_processor.py, tests text_processor.py.
#To run this file, ensure you are in the project root (ensure you are 
#using powershell for windows):
#cd C:\Users\yvonn\rag-nlp-resume-booster
#python tests/test_parser/test_text_processor.py
import logging
import sys
sys.path.append('.')
from src.parser.text_processor import TextProcessor
from src.parser.pdf_extractor import PDFExtractor

#test a single PDF file from root/data/sample_resumes
def test_single_file_text_processing(
        pdf_extractor: PDFExtractor,
        text_processor: TextProcessor,
        file_path: str,
        test_name: str
    ) -> bool: 
    print(f"\nTesting {test_name}: ")
    try: 
        #test pdf extraction: 
        pdf_result = pdf_extractor.extract_text_disk(file_path)
        if not pdf_result or pdf_result['extraction_status'] != 'success': 
            if pdf_result: 
                error_msg = pdf_result.get('error', 'Unknown error')
            else: 
                error_msg = "No result"
            print(f"PDF extraction failed: {error_msg}.")
            return False
        #process extracted text: 
        processing_result = text_processor.process_text(pdf_result['full_text'])
        if processing_result['processing_status'] == 'success': 
            print("Test processing is successful.")
            summary = text_processor.get_processing_summary(processing_result)
            print(f"Original length: {summary['original_length']} chars")
            print(f"Cleaned length: {summary['cleaned_length']} chars")
            print(f"Compression percentage: {summary['compression_percentage']}")
            print(f"Total number of words: {summary['word_count']}")
            print(f"Unique word count: {summary['unique_word_count']}")
            print(f"Average word length: {summary['avg_word_length']} chars")
            print(f"Sentences: {summary['sentence_count']}")
            print(f"Total number of lines: {summary['line_count']}")

            #show text preview 
            cleaned_preview = processing_result['cleaned_text'][:200].replace('\n', ' ')
            print(f"Cleaned text preview: {cleaned_preview}...")
            #show word extraction sample (first 10 words)
            words_sample = processing_result['words'][:10]
            print(f"Sample words extracted: {words_sample}")
            return True
        else: 
            print(f"Text processing failed: {processing_result.get('error', 'Unknown error')}")
            return False
    except Exception as e: 
        print(f"Test failed with error: {str(e)} ")
        return False

#Test text processing using all pdf files from root/data/sample_resumes
def test_text_processing_all_pdfs_sample_resumes() -> None:
    print("=" * 60)
    print("Testing text_processor.py using all pdf files in " 
          "'data/sample_resumes'(disk testing).")
    print("=" * 60)
    text_processor = TextProcessor()
    pdf_extractor = PDFExtractor()
    test_files = [
        ("data/sample_resumes/standard_1pg_resume.pdf", "Standard 1-Page Resume"),
        ("data/sample_resumes/long_resume_6pgs.pdf", "Long 6-Page Resume"),
        ("data/sample_resumes/sparse_resume.pdf", "Sparse 1-Page Resume")
    ]
    results = []
    for file_path, file_test_name in test_files: 
        success_status_bool = test_single_file_text_processing(
            pdf_extractor, text_processor, file_path, file_test_name
        )
        results.append((file_test_name, success_status_bool))
    #Summary
    print("\n" + "=" * 60)
    print("Results of testing text_processor.py: ")
    print("\n" + "=" * 60)
    print("\nResults: ")
    for file_test_name, success_status_bool in results: 
        if success_status_bool: 
            status = "Pass"
        else: 
            status = "Fail"
        print(f"{file_test_name}: {status} ")
    #compute total number passed: 
    passed = 0
    for file_test_name, success_status_bool in results: 
        if success_status_bool: 
            passed += 1 
    total_tests = len(test_files)
    print(f"\nOverall passed: {passed}/{total_tests} files processed successfully.")

#try testing with edge cases (sanity check hehe)
def test_text_processing_edge_cases() -> None: 
    print("=" * 60)
    print("Testing text_processor.py with edge cases (NOT pdfs).")
    print("=" * 60)
    text_processor = TextProcessor()
    #1). Test empty text: 
    print("Testing empty text: ")
    result = text_processor.process_text("")
    print(f"Empty text result (aka empty string): {result['processing_status']}")


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # Run the tests
    test_text_processing_all_pdfs_sample_resumes()
    test_text_processing_edge_cases()





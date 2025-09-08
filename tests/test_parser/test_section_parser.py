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
                #note: section_metadata is a ResumeSection object 
                for section_name, section_metadata in section_result['sections'].items():
                    print(f"{section_name.title()}: {len(section_metadata.content)} "
                          f"total chars (confidence: {section_metadata.confidence:.2f})")
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
    """Test section parsing with known sample resume text."""
    print("\n" + "=" * 70)
    print("Testing section parsing with sample text: ")
    print("=" * 70)
    sample_resume_text = """
    Marcus Rodriguez
    Software Engineer
    marcus.rodriguez@email.com | (555) 123-4567 | linkedin.com/in/marcus-rodriguez | github.com/marcus-dev
    
    PROFESSIONAL SUMMARY
    Experienced software engineer with 5+ years developing scalable web applications and machine learning systems.
    Passionate about clean code and innovative solutions.
    
    EXPERIENCE
    Senior Software Engineer - TechCorp Inc (2020-Present)
    - Built scalable web applications using Python, React, and AWS
    - Led team of 4 engineers on major product features
    - Improved system performance by 40% through optimization
    
    Software Engineer - StartupXYZ (2018-2020)
    - Developed REST APIs and microservices architecture
    - Implemented CI/CD pipelines reducing deployment time by 60%
    - Collaborated with cross-functional teams on product development
    
    EDUCATION
    Bachelor of Science in Computer Science
    Massachusetts Institute of Technology (2014-2018)
    GPA: 3.8/4.0
    Relevant Coursework: Data Structures, Algorithms, Machine Learning, Databases
    
    SKILLS
    Programming Languages: Python, JavaScript, Java, C++, SQL
    Frameworks & Tools: React, Django, Flask, Node.js, Docker, Kubernetes
    Databases: PostgreSQL, MongoDB, Redis
    Cloud Platforms: AWS, Google Cloud Platform, Azure
    
    PROJECTS
    Resume Analyzer Tool (2024)
    - Built ML-powered resume analysis system using NLP and RAG architecture
    - Deployed on AWS with Docker containerization and CI/CD pipeline
    - Technologies: Python, PyTorch, FastAPI, ChromaDB
    
    E-commerce Platform (2023)
    - Developed full-stack e-commerce application with payment integration
    - Implemented real-time inventory management and analytics dashboard
    - Technologies: React, Node.js, PostgreSQL, Stripe API
    
    CERTIFICATIONS
    AWS Certified Solutions Architect - Associate (2023)
    Google Cloud Professional Developer (2022)
    Certified Kubernetes Administrator (2021)
    """
    parser = SectionParser()
    result = parser.parse_sections(sample_resume_text)
    if result['parsing_status'] == 'success': 
        print(f"Sample text parsing successful.")
        print(f"Total number of sections found: {result['total_sections']}")
        #Show detailed section analysis
        print(f"\nDetailed section analysis: ")
        #note: section_metadata is a ResumeSection object. 
        for section_name, section_metadata in result['sections'].items(): 
            print(f"\n{section_name.upper()}:")
            print(f"Confidence: {section_metadata.confidence:.2f}")
            print(f"Length: {len(section_metadata.content)} characters long")
            print(f"Start index: {section_metadata.start_index}-{section_metadata.end_index}")
            #Show first few lines of content: 
            lines = section_metadata.content.split('\n')[:3]
            for line in lines: 
                if line.strip():
                    print(f"{line.strip()}")
        #show contact info extraction: 
        print(f"\nContact info extracted: ")
        for k, v in result['contact_info'].items(): 
            if v: 
                print(f"{k.title()}: {v}")
    else: 
        print(f"Sample text parsing failed: {result.get('error', 'Unknown error')}")

def test_edge_cases(): 
    """Test edge cases and error handling for section parsing."""
    print("\n" + "=" * 70)
    print("Testing edge cases and error handling for section parsing.")
    print("=" * 70)
    parser = SectionParser()
    #1) Test empty text 
    print("\n 1) Testing empty text ")
    result = parser.parse_sections("")
    print(f"Empty text result: {result['parsing_status']}")
    #2) Test text with no sections 
    print("\n 2) Testing text with no recognizable sections ")
    no_sections_text = "This is just some random text with no resume" 
    + "sections at all. Just words and sentences."
    result = parser.parse_sections(no_sections_text)
    print(f"No sections result: {result['parsing_status']}, " 
          f"number of sections found: {result['total_sections']}")
    #Test None input 
    print("\n 1) Testing None input: ")
    result = parser.parse_sections(None)
    print(f"None input result: {result['parsing_status']}")
    #Testing text with only contact info 
    print("\n 1) Testing text with only contact info: ")
    contact_only_text = "John Doe\njohn.doe@email.com\n(555)" 
    + "123-4567\nlinkedin.com/in/johndoe"
    result = parser.parse_sections(contact_only_text)
    if result['parsing_status'] == 'success': 
        
    

    
    pass #temp 
            
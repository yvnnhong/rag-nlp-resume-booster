#section_parser.py is step 3 to parse individual sections (e.x education, work history, etc)
import re
import logging
from typing import Dict, List, Optional, Any 

logger = logging.getLogger(__name__)

class ResumeSection: 
    def __init__(self, name, content, start_index, end_index, confidence) -> None: 
        self.name = name
        self.content = content
        self.start_index = start_index
        self.end_index = end_index
        self.confidence = confidence
from abc import ABC, abstractmethod
from models.resume import Resume 
from typing import Dict, List 
from dataclasses import dataclass

@dataclass
class SectionData:
    titles    : List[str]
    paragraphs: List[str]

class ParserInterface(ABC):
    
    def parse(self, file_stream) -> Resume:
        """Main parsing pipeline"""
        # Step 1: Validate and preprocess
        validated_stream = self.validate_and_preprocess(file_stream)
        # Step 2: Extract raw content
        raw_text = self.extract_raw_content(validated_stream)
        
        # Step 3: Preprocess text
        cleaned_text = self.preprocess_text(raw_text)
        
        # Step 4: Identify sections
        sections = self.identify_sections(cleaned_text)
        
        # Step 5: Extract structured data
        structured_data = self.extract_structured_data(sections)
        
        # Step 6: Create Resume object
        return self.create_resume_object(structured_data)
    

    
    @abstractmethod
    def validate_and_preprocess(self, file_stream):
        """Validate file and preprocess stream"""
        raise NotImplementedError("Subclasses must implement validate_and_preprocess")
    
    @abstractmethod
    def extract_raw_content(self, file_stream) -> str:
        """Extract raw text from file - implementation specific"""
        raise NotImplementedError("Subclasses must implement extract_raw_content")
    
    @abstractmethod
    def preprocess_text(self, raw_text: str) -> str:
        """Clean and preprocess extracted text"""
        raise NotImplementedError("Subclasses must implement preprocess_text")
    
    @abstractmethod
    def identify_sections(self, text: str) -> SectionData:
        """Identify different sections in the resume text"""
        raise NotImplementedError("Subclasses must implement identify_sections")
    
    @abstractmethod
    def extract_structured_data(self, sections: Dict[str, str]) -> Dict:
        """Extract structured data from identified sections"""
        raise NotImplementedError("Subclasses must implement extract_structured_data")

    @abstractmethod
    def create_resume_object(self, data: Dict) -> Resume:
        """Create Resume object from extracted data"""
        raise NotImplementedError("Subclasses must implement create_resume_object")
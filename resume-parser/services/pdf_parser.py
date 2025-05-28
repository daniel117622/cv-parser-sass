from services.parser_interface import ParserInterface
from models.resume import Resume

class PDFParser(ParserInterface):
    supported_types = ['application/pdf', 'pdf']
    @classmethod
    def get_supported_types(cls):
        return cls.supported_types
    
    def parse(self, file_stream):
        # Dummy PDF parsing logic for demonstration
        # In a real implementation, you would extract data from the PDF here
        resume = Resume(
            name         = "John Doe",
            email        = "john.doe@example.com",
            phone        = "+1234567890",
            education    = ["B.Sc. Computer Science"],
            experience   = ["Software Engineer at ExampleCorp"],
            skills       = ["Python", "Flask", "PDF Parsing"],
            introduction = "Experienced software engineer.",
            technologies = ["Python", "Flask"],
            hyperlinks   = ["https://linkedin.com/in/johndoe"]
        )
        return resume.get()

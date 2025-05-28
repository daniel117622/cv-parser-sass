from services.pdf_parser import PDFParser

class ParserFactory:
    _parsers = [PDFParser]

    @classmethod
    def get_parser(cls, file_mime_type=None, file_extension=None):
        """
        Returns an instance of the appropriate parser based on MIME type or file extension.

        Args:
            file_mime_type (str): The MIME type of the file (e.g., 'application/pdf').
            file_extension (str): The file extension (e.g., 'pdf', 'docx').

        Returns:
            ParserInterface: An instance of the appropriate parser.

        Raises:
            ValueError: If no suitable parser is found.
        """
        for parser_cls in cls._parsers:
            supported = parser_cls.get_supported_types()
            if file_mime_type and file_mime_type in supported:
                return parser_cls()
            if file_extension and file_extension.lower() in supported:
                return parser_cls()
        raise ValueError("No parser available for the given file type.")

    @classmethod
    def register_parser(cls, parser_cls):
        """
        Register a new parser class.

        Args:
            parser_cls (type): The parser class to register.
        """
        cls._parsers.append(parser_cls)

from typing import Literal, Optional, Dict, Type
from services.pdf_parser import PDFParser
from services.parser_interface import ParserInterface

FileType = Literal['pdf', 'docx', 'xlsx', 'pptx', 'zip', 'doc', 'unknown']

class ParserFactory:
    # Map file types to their corresponding parser classes
    _parser_map: Dict[FileType, Optional[Type]] = {
        'pdf': PDFParser,
        'docx'   : None,
        'xlsx'   : None,
        'pptx'   : None,
        'zip'    : None,
        'doc'    : None,
        'unknown': None
    }

    @classmethod
    def get_parser(cls, file_type: FileType) -> Optional[ParserInterface]:
        """
        Returns an instance of the appropriate parser based on file type.

        Args:
            file_type (FileType): The detected file type (e.g., 'pdf', 'docx').

        Returns:
            Optional[ParserInterface]: An instance of the appropriate parser, 
                                     or None if no parser is available.
        """
        parser_cls = cls._parser_map.get(file_type)
        
        if parser_cls is None:
            return None
        
        return parser_cls()

    @classmethod
    def register_parser(cls, file_type: FileType, parser_cls: Type):
        """
        Register a new parser class for a specific file type.

        Args:
            file_type (FileType): The file type to associate with the parser.
            parser_cls (Type): The parser class to register.
        """
        cls._parser_map[file_type] = parser_cls

    @classmethod
    def get_supported_file_types(cls) -> list[FileType]:
        """
        Returns a list of file types that have available parsers.

        Returns:
            list[FileType]: List of supported file types.
        """
        return [file_type for file_type, parser_cls in cls._parser_map.items() 
                if parser_cls is not None]
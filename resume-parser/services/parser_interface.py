from abc import ABC, abstractmethod

class ParserInterface(ABC):
    @abstractmethod
    def parse(self, file_stream):
        """
        Parse the given file stream and return structured resume data.

        Args:
            file_stream (file-like object): The file to parse.

        Returns:
            dict: Parsed resume data (e.g., name, contact, experience, etc.)
        """
        pass

    @staticmethod
    def supported_types(self):
        """
        Return a list of supported MIME types or file extensions.

        Returns:
            list: Supported types (e.g., ['application/pdf', 'pdf'])
        """
        pass

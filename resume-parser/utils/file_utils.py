
from typing import Literal


def allowed_file(filename):
    return True

def get_file_extension(filename):
    return 'pdf'


def detect_file_type_by_magic_bytes(file_stream) -> Literal['pdf', 'docx', 'xlsx', 'pptx', 'zip', 'doc', 'unknown']:
    """Detect file type using magic bytes"""
    # Save current position
    current_pos = file_stream.tell()
    
    # Read first few bytes
    file_stream.seek(0)
    magic_bytes = file_stream.read(8)
    
    # Reset to original position
    file_stream.seek(current_pos)
    
    # PDF magic bytes: %PDF
    if magic_bytes.startswith(b'%PDF'):
        return 'pdf'
    
    # DOCX magic bytes: PK (ZIP signature, since DOCX is a ZIP archive)
    # We need to read more bytes to distinguish DOCX from regular ZIP
    if magic_bytes.startswith(b'PK\x03\x04'):
        # Read more bytes to check for DOCX-specific content
        file_stream.seek(0)
        chunk = file_stream.read(1024)
        file_stream.seek(current_pos)
        
        # Look for DOCX-specific strings in the ZIP structure
        if b'word/' in chunk or b'[Content_Types].xml' in chunk:
            return 'docx'
        elif b'xl/' in chunk:
            return 'xlsx'  # Excel file
        elif b'ppt/' in chunk:
            return 'pptx'  # PowerPoint file
        else:
            return 'zip'   # Generic ZIP file
    
    # DOC magic bytes: D0CF11E0A1B11AE1 (OLE2 signature)
    if magic_bytes.startswith(b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'):
        return 'doc'
    
    return 'unknown'
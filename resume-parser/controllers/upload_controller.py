from flask import Blueprint, request, jsonify
from utils.file_utils import allowed_file, get_file_extension, get_mime_type
from services.parser_factory import ParserFactory
from utils.exception_handling import handle_exceptions_unsafe

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
@handle_exceptions_unsafe
def upload():
    if 'file' not in request.files:
        raise ValueError('No file part in the request')

    file = request.files['file']
    if file.filename == '':
        raise ValueError('No selected file')

    if not allowed_file(file.filename):
        raise ValueError('Unsupported file type')

    file_extension = get_file_extension(file.filename)
    mime_type      = get_mime_type(file)
    parser         = ParserFactory.get_parser(file_mime_type=mime_type, file_extension=file_extension)
    parsed_data    = parser.parse(file)

    return jsonify({
        'message': 'File parsed successfully',
        'parsed_data': parsed_data
    }), 201

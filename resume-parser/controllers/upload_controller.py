from flask import Blueprint, request, jsonify
from utils.file_utils import allowed_file, detect_file_type_by_magic_bytes, get_file_extension
from services.parser_factory import ParserFactory
from utils.exception_handling import handle_exceptions_unsafe
import time

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/upload', methods=['POST'])
@handle_exceptions_unsafe
def upload():
    start = time.perf_counter()
    if 'file' not in request.files:
        raise ValueError('No file part in the request')

    file = request.files['file']
    file_type = detect_file_type_by_magic_bytes(file)

    if file.filename == '':
        raise ValueError('No selected file')

    if not allowed_file(file.filename):
        raise ValueError('Unsupported file type')

    parser = ParserFactory.get_parser(file_type=file_type)
    if not parser:
        elapsed = time.perf_counter() - start
        return jsonify({
            'file_type': file_type,
            'message': f'ERROR: No parser for {file_type}',
            'processing_time': elapsed
        }), 400

    parsed_data = parser.parse(file)
    elapsed = time.perf_counter() - start

    return jsonify({
        'file_type': file_type,
        'message': 'File parsed successfully',
        'parsed_data': parsed_data,
        'processing_time': elapsed
    }), 201
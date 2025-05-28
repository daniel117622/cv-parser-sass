from functools import wraps
from flask import jsonify
import traceback

def handle_exceptions_unsafe(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            tb = e.__traceback__
            # Get the last traceback frame
            while tb.tb_next:
                tb = tb.tb_next
            filename = tb.tb_frame.f_code.co_filename
            lineno = tb.tb_lineno
            return jsonify({
                'error': str(e),
                'file': filename,
                'line': lineno
            }), 500
    return wrapper

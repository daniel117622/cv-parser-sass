import traceback
from flask import Flask, jsonify
from controllers.upload_controller import upload_bp
from models.resume import Resume
import nltk
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_nltk():
    """
    Ensure all required NLTK resources are present:
      – punkt (sentence tokenizer)
      – averaged_perceptron_tagger (POS tagger)
      – maxent_ne_chunker (named‐entity chunker)
      – words (lexicon for NE chunker)
    """
    resources = {
        "tokenizers/punkt"                  : "punkt",
        "taggers/averaged_perceptron_tagger": "averaged_perceptron_tagger",
        "chunkers/maxent_ne_chunker"        : "maxent_ne_chunker",
        "corpora/words"                     : "words",
    }

    for path, pkg in resources.items():
        try:
            nltk.data.find(path)
            logger.info(f"NLTK resource '{pkg}' already available.")
        except LookupError:
            logger.info(f"Downloading NLTK resource '{pkg}' …")
            try:
                nltk.download(pkg, quiet=True)
                logger.info(f"Successfully downloaded '{pkg}'.")
            except Exception as e:
                logger.warning(f"Failed to download '{pkg}': {e}")
                logger.warning(traceback.format_exc())
                logger.warning("Continuing without this resource—some features may break.")

# Initialize NLTK when module loads
initialize_nltk()

def create_app():
    app = Flask(__name__)

    app.register_blueprint(upload_bp)

    @app.route("/", methods=["GET"])
    def empty_resume():
        empty = Resume()
        return jsonify(empty.get())
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)



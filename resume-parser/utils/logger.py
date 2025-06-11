import logging

# Configure the logger
logger = logging.getLogger("cv_parsing_saas")
logger.setLevel(logging.INFO)

# Create console handler with a custom format
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
ch.setFormatter(formatter)

# Avoid adding multiple handlers if this module is imported multiple times
if not logger.hasHandlers():
    logger.addHandler(ch)

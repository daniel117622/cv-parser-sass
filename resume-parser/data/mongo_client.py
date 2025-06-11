import os
from pymongo import MongoClient, errors
from utils.logger import logger

class MongoConnector:
    _client = None

    def __init__(self):
        if MongoConnector._client is None:
            mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
            try:
                MongoConnector._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
                MongoConnector._client.admin.command('ping')
                logger.info(f"Successfully connected to MongoDB at {mongo_uri}")
            except errors.ServerSelectionTimeoutError as e:
                logger.error(f"Failed to connect to MongoDB at {mongo_uri}: {e}")
                raise
        self.client = MongoConnector._client
        self.db = self.client["resume_parser_db"]

    def get_db(self):
        return self.db

    def get_uploads_collection(self):
        return self.db["uploads"]

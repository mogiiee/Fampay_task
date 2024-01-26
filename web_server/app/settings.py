from decouple import config

# database credentials exporting from .env file

MONGO_DETAILS = config("MONGO_DB_CREDENTIALS")
MONGO_DB_NAME = config("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = config("MONGO_COLLECTION_NAME")
LAST_UPDATED_TIME_COLLECTION_NAME = config("LAST_UPDATED_TIME_COLLECTION")

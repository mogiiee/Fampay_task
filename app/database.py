from pymongo import MongoClient
from . import settings

client = MongoClient(settings.MONGO_DETAILS)
db = client[settings.MONGO_DB_NAME]
collection = db[settings.MONGO_COLLECTION_NAME]
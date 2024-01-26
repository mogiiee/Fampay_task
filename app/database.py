from pymongo import MongoClient
from . import settings


client = MongoClient(settings.MONGO_DETAILS)
db = client[settings.MONGO_DB_NAME]
collection = db[settings.MONGO_COLLECTION_NAME]
collection2 = db[settings.MONGO_COLLECTION_NAME_2]
collection3 = db[settings.MONGO_COLLECTION_NAME_3]
time_updater_collection = db[settings.LAST_UPDATED_TIME_COLLECTION_NAME]

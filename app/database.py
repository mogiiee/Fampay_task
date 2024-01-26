from pymongo import MongoClient
from web_server.app import settings


client = MongoClient(settings.MONGO_DETAILS)
db = client[settings.MONGO_DB_NAME]
collection = db[settings.MONGO_COLLECTION_NAME]
time_updater_collection = db[settings.LAST_UPDATED_TIME_COLLECTION_NAME]

from dotenv import load_dotenv
import os

load_dotenv()

#youtube API credentials
API_KEY_1 = os.environ.get("YOUTUBE_API_KEY1")
API_KEY_2 = os.environ.get("YOUTUBE_API_KEY2")

#database credentials

MONGO_DETAILS = os.environ.get("MONGO_DB_CREDENTIALS")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.environ.get("MONGO_COLLECTION_NAME")
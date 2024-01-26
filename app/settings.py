from decouple import config


# youtube API credentials
API_KEY_1 = config("YOUTUBE_API_KEY1")
API_KEY_2 = config("YOUTUBE_API_KEY2")
API_KEY_3 = config("YOUTUBE_API_KEY3")

# database credentials

MONGO_DETAILS = config("MONGO_DB_CREDENTIALS")
MONGO_DB_NAME = config("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = config("MONGO_COLLECTION_NAME")
LAST_UPDATED_TIME_COLLECTION_NAME = config("LAST_UPDATED_TIME_COLLECTION")

# Redis credentials

# REDIS_DB_CRED = config('REDIS_DB_CRED')

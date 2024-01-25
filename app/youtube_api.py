from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from . import settings, operations, database  # Assuming settings contains your API keys

# List of API keys
API_KEYS = [settings.API_KEY_1, settings.API_KEY_2, settings.API_KEY_3]


def get_last_fetch_time():
    metadata = database.time_updater_collection.find_one(
        {"metadata": "last_fetch_time"}
    )
    return metadata["timestamp"] if metadata else None


def update_last_fetch_time(timestamp):
    database.time_updater_collection.update_one(
        {"metadata": "last_fetch_time"}, {"$set": {"timestamp": timestamp}}, upsert=True
    )


def youtube_caller(number, insert_query):
    last_fetch_time = get_last_fetch_time()
    if not last_fetch_time:
        last_fetch_time = datetime.now() - timedelta(minutes=1)
    for api_key in API_KEYS:
        try:
            service = build("youtube", "v3", developerKey=api_key)
            timern = last_fetch_time.isoformat() + "Z"
            query = str(insert_query)
            req = service.search().list(
                part="snippet",
                q=query,
                maxResults=number,
                type="video",
                order="date",
                publishedAfter=timern,
            )
            response = req.execute()

            items = response["items"]
            mongo_list = []

            for i in items:
                thumbnail_urls = []
                mongo_input = {
                    "video_id": i["id"]["videoId"],
                    "channel_title": i["snippet"]["channelTitle"],
                    "description": i["snippet"]["description"],
                    "title": i["snippet"]["title"],
                    "publishing_datetime": i["snippet"]["publishTime"],
                    "timestamp": datetime.now(),
                }

                for j in ["default", "high", "medium"]:
                    thumbnail_urls.append(i["snippet"]["thumbnails"][j]["url"])
                mongo_input["thumbnail_urls"] = thumbnail_urls
                mongo_list.append(mongo_input)

            return mongo_list

        except HttpError as e:
            if e.resp.status in [403, 429]:  # Quota exceeded error codes
                print(
                    f"Quota exceeded or access denied for API Key: {api_key}. Trying next key..."
                )
                continue  # Try the next API key
            else:
                raise  # Re-raise the exception if it's not a quota error

    raise Exception("All API keys have exceeded their quota or are invalid.")


# Example usage
# results = youtube_caller(10, "your_search_query")

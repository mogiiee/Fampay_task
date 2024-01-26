from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta, timezone

from . import database

from . import settings

# Assuming settings contains your API keys

# List of API keys
API_KEYS = [settings.API_KEY_1, settings.API_KEY_2, settings.API_KEY_3]


def get_last_call_time():
    # Get the last call time document from the collection 'last_call_time_collection'
    last_call_time_doc = database.time_updater_collection.find_one(
        {"name": "last_call_time"}
    )
    # If the document is not found, it means this is the first time the function is called
    if last_call_time_doc is None:
        # Set the last call time to 1 minute ago to avoid missing recent videos
        last_call_time = datetime.now() - timedelta(minutes=1)
        # Insert a new document with the last call time
        database.time_updater_collection.insert_one(
            {"name": "last_call_time", "timestamp": last_call_time}
        )
        return last_call_time
    else:
        # If found, return the stored last call time
        return last_call_time_doc["timestamp"]


def update_last_fetch_time(timestamp):
    # Ensure the 'time_updater_collection' exists (implicitly created on upsert)
    database.time_updater_collection.update_one(
        {"metadata": "last_fetch_time"},
        {"$set": {"timestamp": timestamp}},
        upsert=True,  # Create the document if it doesn't exist
    )


def youtube_caller(number, insert_query):
    last_fetch_time = get_last_call_time()
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

            if mongo_list:
                # Use the publishing time of the most recent video fetched as the new last call time
                last_video_publish_time = max(
                    item["publishing_datetime"] for item in mongo_list
                )

                # When converting back to datetime, remove the 'Z' and specify the UTC timezone
                last_video_publish_time = datetime.fromisoformat(
                    last_video_publish_time.replace("Z", "")
                )
                last_video_publish_time = last_video_publish_time.replace(
                    tzinfo=timezone.utc
                )

                update_last_fetch_time(last_video_publish_time)

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

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
from . import settings, operations  # Assuming settings contains your API keys

# List of API keys
API_KEYS = [settings.API_KEY_1, settings.API_KEY_2, settings.API_KEY_3]

def YoutubeCaller(number, insert_query):
    for api_key in API_KEYS:
        try:
            service = build('youtube', 'v3', developerKey=api_key)
            timern = operations.get_yt_datetime()
            query = str(insert_query)
            req = service.search().list(part='snippet', q=query, maxResults=number, type='video', order='date', publishedAfter=timern)
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
                    "timestamp": datetime.now()
                }
                
                for j in ["default", "high", "medium"]:
                    thumbnail_urls.append(i["snippet"]["thumbnails"][j]["url"])
                mongo_input['thumbnail_urls'] = thumbnail_urls
                mongo_list.append(mongo_input)

            return mongo_list

        except HttpError as e:
            if e.resp.status in [403, 429]:  # Quota exceeded error codes
                print(f"Quota exceeded or access denied for API Key: {api_key}. Trying next key...")
                continue  # Try the next API key
            else:
                raise  # Re-raise the exception if it's not a quota error

    raise Exception("All API keys have exceeded their quota or are invalid.")

# Example usage
# results = YoutubeCaller(10, "your_search_query")

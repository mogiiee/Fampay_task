from . import settings, operations
from datetime import datetime
from googleapiclient.discovery import build



def YoutubeCaller(number, insert_query):
    try:
        service = build('youtube', 'v3', developerKey= settings.API_KEY_1) 
        #put in your own api key from the .env file
    except:
        service = build('youtube', 'v3', developerKey= settings.API_KEY_2) 
        print("used api key 2")
        #put in your own api key2 from the .env file
        #api_key2 will only kick in when api_key 1 fails
    timern = operations.get_yt_datetime()
    query = str(insert_query)
    req = service.search().list(part = 'snippet', q = query, maxResults= number, type='video', order= 'date', publishedAfter= timern)
    response = req.execute()
    items = response["items"]
    mongo_list = []
    #looping through the dict to find the required values
    for i in items:
        thumbnail_urls = []
        mongo_input = {}
        mongo_input["video_id"] = i["id"]["videoId"]
        mongo_input["channel_title"] = i["snippet"]["channelTitle"]
        mongo_input["description"] = i["snippet"]["description"]
        mongo_input["title"] = i["snippet"]["title"]
        mongo_input['publishing_datetime'] = i["snippet"]["publishTime"] 
        mongo_input["timestamp"] = datetime.now()
        for j in ["default", "high", "medium"]:
            thumbnail_urls.append(i["snippet"]["thumbnails"][j]["url"])
        mongo_input['thumbnail_urls'] = thumbnail_urls
        mongo_list.append(mongo_input)
    
    return mongo_list, items
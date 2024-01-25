from . import database, responses,youtube_api
from datetime import datetime, timedelta
from pymongo import DESCENDING


def Inserter(number_of_inserts, insert_query):
    list_of_entries = youtube_api.YoutubeCaller(number_of_inserts, insert_query)
    if len(list_of_entries) == 0:
        return responses.response(False, "No videos found", None)
    else:
        database.collection.insert_many(list_of_entries)
    return responses.response(True, None, {
        "inserted_count": int(len(list_of_entries)),
        # "inserted_data": list_of_entries
    })


def get_data(limit, page):
    page = int(page)
    limit = int(limit)

    if page <= 0:
        return responses.response(False, "page cannot be less than 1", None)

    skip = (page - 1) * limit 

    try:
        # Count total documents for pagination metadata
        total_videos = database.collection.count_documents({})
        total_pages = (total_videos + limit - 1) // limit  # Ceiling division

        # Fetching data with sorting and pagination
        results = database.collection.find({}, {"_id": 0}).sort("publishing_datetime", DESCENDING).limit(limit).skip(skip)

        # Creating the response with metadata
        response_data = {
            "videos": list(results),
            "total_videos": total_videos,
            "current_page": page,
            "total_pages": total_pages
        }
        return responses.response(True, "Results fetched", response_data)
    except Exception as e:
        return responses.response(False, str(e), None)


#gives the current time for the getting information from youtube API
def get_yt_datetime():
    d = datetime.now() - timedelta(0, 1080)
    timern = d.isoformat('T')+"Z"
    return timern

#inserts the videos into the database

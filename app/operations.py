from . import database, responses
from datetime import datetime, timedelta
from pymongo import DESCENDING

def GetData(limit, page):
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
# def insert_videos(doc):
#     p
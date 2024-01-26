from . import database, responses
from pymongo import DESCENDING


def get_data(limit, page):
    page = int(page)
    limit = int(limit)

    if page <= 0:
        return responses.response(False, "Page cannot be less than 1", None)

    skip = (page - 1) * limit

    try:
        # Pipeline to count the total unique videos
        count_pipeline = [
            {"$group": {"_id": "$video_id"}},
            {"$count": "total_unique_videos"},
        ]

        # Execute the count pipeline
        count_results = list(database.collection.aggregate(count_pipeline))
        total_videos = count_results[0]["total_unique_videos"] if count_results else 0
        total_pages = (total_videos + limit - 1) // limit

        # Pipeline to fetch paginated videos
        data_pipeline = [
            {"$sort": {"publishing_datetime": DESCENDING}},
            {
                "$group": {
                    "_id": "$video_id",
                    "channel_title": {"$first": "$channel_title"},
                    "description": {"$first": "$description"},
                    "title": {"$first": "$title"},
                    "publishing_datetime": {"$first": "$publishing_datetime"},
                    "timestamp": {"$max": "$timestamp"},
                    "thumbnail_urls": {"$first": "$thumbnail_urls"},
                }
            },
            {"$sort": {"publishing_datetime": DESCENDING}},
            {"$skip": skip},
            {"$limit": limit},
        ]

        # Execute the data pipeline
        results = database.collection.aggregate(data_pipeline)

        # Creating the response with metadata
        response_data = {
            "videos": list(results),
            "total_unique_videos": total_videos,
            "current_page": page,
            "total_pages": total_pages,
        }

        return responses.response(True, "Results fetched", response_data)

    except Exception as e:
        return responses.response(False, str(e), None)


# inserts the videos into the database

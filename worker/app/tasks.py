from . import youtube_api, responses, database
from .celery_config import app


@app.task(name="app.tasks.fetch_and_store_youtube_data")
def fetch_and_store_youtube_data(number, query):
    # Use youtube_caller function
    youtube_data = youtube_api.youtube_caller(number, query)
    if len(youtube_data) == 0:
        return responses.response(False, "No videos found", None)
    else:
        database.collection.insert_many(youtube_data)
    return responses.response(
        True,
        None,
        {
            "inserted_count": int(len(youtube_data)),
            # "inserted_data": list_of_entries
        },
    )

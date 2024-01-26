from celery import Celery
from datetime import timedelta

# Configure Celery to use Redis as the broker
app = Celery("tasks", broker="redis://redis:6379/0", include=["app.tasks"])


app.conf.beat_schedule = {
    "fetch_and_store_youtube_data_every_10_seconds": {
        "task": "app.tasks.fetch_and_store_youtube_data",
        "schedule": timedelta(seconds=10),
        "args": (5, "music"),  # Number of videos and query
    },
}
# app.autodiscover_tasks(["app"])

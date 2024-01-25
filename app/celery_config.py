from celery import Celery
from datetime import timedelta

# Configure Celery to use Redis as the broker
app = Celery('tasks', broker='redis://localhost:6379/0', include=['app.tasks'])


app.conf.beat_schedule = {
    'fetch_and_store_youtube_data': {
        'task': 'app.tasks.fetch_and_store_youtube_data',
        'schedule': timedelta(seconds=10),
        'args': (10, 'music')  # Number of videos and query
    },
}


app.autodiscover_tasks(['app'])

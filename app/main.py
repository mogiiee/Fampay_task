from fastapi import FastAPI
from . import tasks, responses

app = FastAPI()


# Define your API routes here
@app.get("/")
async def root():
    return responses.response(True, "Hello Fampay", None)


@app.post("/insert_videos")
async def insert_videos():
    pass


from fastapi import FastAPI
from . import operations, responses, database, youtube_api

app = FastAPI()


# Define your API routes here
@app.get("/")
async def root():
    return responses.response(True, "Hello Fampay", None)



# @app.post("/insert_videos")
# async def insert_videos(metadata: information):

#     result  = database.collection.insert_one(metadata.model_dump())

#     return responses.response(True,None,str(result))

@app.get("/get_videos")
async def get_videos(number, insert_query):
    result = youtube_api.YoutubeCaller(number, insert_query)
    return responses.response(True,None,result)


@app.get('/get_all_data')
async def get_all_data(limit, page):
    try:
        result = operations.GetData(limit, page)
        return result
    except Exception as e:
        return responses.response(False, str(e), None)
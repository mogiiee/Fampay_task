from fastapi import FastAPI
from . import operations, responses, database, youtube_api

app = FastAPI()


# Define your API routes here
@app.get("/")
async def root():
    return responses.response(True, "Hello Fampay", None)



@app.get('/fetch_and_insert')
async def fetch_and_insert(number_of_inserts, insert_query):
    try:
        result = operations.Inserter(number_of_inserts, insert_query)
        return responses.response(True, "Data inserted", result)
    except Exception as e:
        return responses.response(False, str(e), None)


@app.get('/get_all_data')
async def get_all_data(limit, page):
    try:
        result = await operations.get_data(limit, page)
        return result
    except Exception as e:
        return responses.response(False, str(e), None)
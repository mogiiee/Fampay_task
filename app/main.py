from fastapi import FastAPI
from app import operations
from app import responses

app = FastAPI()


# Define your API routes here
@app.get("/")
async def root():
    return responses.response(True, "Hello Fampay", None)


@app.get("/fetch_and_insert")
async def fetch_and_insert(number_of_inserts, insert_query):
    try:
        result = operations.inserter(number_of_inserts, insert_query)
        return responses.response(True, "Data inserted", result)
    except Exception as e:
        return responses.response(False, str(e), None)


@app.get("/get_unique_data")
async def get_unique_data(limit, page):
    try:
        result = operations.get_data(limit, page)
        return result
    except Exception as e:
        return responses.response(False, str(e), None)

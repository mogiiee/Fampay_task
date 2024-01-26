from fastapi import FastAPI
from . import operations, responses

app = FastAPI()


# Define your API routes here
@app.get("/")
async def root():
    return responses.response(True, "Hello Fampay", None)


@app.get("/get_unique_data")
async def get_unique_data(limit, page):
    try:
        result = operations.get_data(limit, page)
        return result
    except Exception as e:
        return responses.response(False, str(e), None)


# Fampay Youtube API task


## Project Goal

To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

## Basic Requirements:

- Server should call the YouTube API continuously in background (async) with some interval (say 15 seconds) for fetching the latest videos for a predefined search query and should store the data of videos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes.
- A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
- It should be scalable and optimised. 

## Factors taken into consideration for the task

The whole project consists of 4 containers practically one for each service (redis, fastapi, celery worker and celery beat)

![architechture diagram](https://cdn.discordapp.com/attachments/991052554802712586/1200430324371431454/Screenshot_2024-01-26_at_6.50.34_PM.png?ex=65c626dc&is=65b3b1dc&hm=93e4e772b57371a7c1ea51b57bd2b5ab6c0fb5a9dc3b87e3349a172a6b1f3ba9&)

API tokens are kept in a list and are rotated through. when a token expires, the next token is used 

![token expiration pic](https://cdn.discordapp.com/attachments/991052554802712586/1200430690207027252/PHOTO-2024-01-26-12-27-18.jpg?ex=65c62733&is=65b3b233&hm=95c42b5b533feecb66f05c55ad993f5bfc97fccc16ab32593809ab2e8caf7158&)





## Environment Variables In web_server/app

To run this project, you will need to add the following environment variables to your .env file




`MONGO_DB_CREDENTIALS=`= 

`MONGO_DB_NAME`=

`MONGO_COLLECTION_NAME`=

`LAST_UPDATED_TIME_COLLECTION`=


## Environment Variables In Worker

`YOUTUBE_API_KEY1` = 

`YOUTUBE_API_KEY2` = 

`YOUTUBE_API_KEY3` =

`MONGO_DB_CREDENTIALS`= 

`MONGO_DB_NAME`=

`MONGO_COLLECTION_NAME`=

`LAST_UPDATED_TIME_COLLECTION`=

## BUILD INSTRUCTIONS

The project has a docker-compose file which can start the server and the cron job at the same time.

* Redis
* Celery Worker
* Celery Beat
* FastAPI web application

```bash
  docker-compose up --build
```

## Suggestions incorporated from last time

- I was told that thumbnails had had 3 fields to store them, has been rectified now
- Code quality was bad because there database.py was duplicated in both the apps, but this is a necessity as both the apps are talking to the same database. As far as the other files, they are different and have the content absolutely required for the scalability of individual containers.
- Video retrival time was not taken into consideration while requesting for the next video. This time I have created an extra function which will take videos only after the last successful fetch of a video so that none of the videos are missed.
- Duplicated responses were being shown. I have created a function which shows only unique responses in the reverse chronological order of their publishing date-time 


    
## Run Locally

Clone the project

```
  git clone https://github.com/mogiiee/Fampay_task.git
```

Go to the project directory

```
  cd Fampay_task

```
Set up a virtual environment for the project:
```
python3 -m venv virtualenv
```

Go to the web_server

```
    cd web-server
```

Install dependencies

```
  pip3 install requirements.txt
```

Start the server

```bash
uvicorn app.main:app --reload
```

Go to the url 

```bash
http://localhost:8000/docs or http://127.0.0.1:8000/docs
```


## Operating Swagger

Be greeted with 2 different endpoints 

![alt text](https://cdn.discordapp.com/attachments/991052554802712586/1200435255958573086/Screenshot_2024-01-26_at_7.10.59_PM.png?ex=65c62b74&is=65b3b674&hm=1c3c5d9c2d2e963db6754403fafc419ab42050da55e08a76fe53a8ca15027c35&)


* root endpoint just greets you in a wonderful way


## Get Unique Data

* Gets the unique data from the database in a paginated response. It also shows the current page and the total pages in which the data would fit in.

![alt text](https://cdn.discordapp.com/attachments/991052554802712586/1200436083498963036/Screenshot_2024-01-26_at_7.14.16_PM.png?ex=65c62c39&is=65b3b739&hm=40f4bcddfdbdb387b2dff2239d91519b527347505ec594cd90b2ed83c4fa044d&)

## Default Options

- celery beat operates at every 10 seconds, can be changed
- The insert query has been set to music can be changed in worker/app/celery_config
- Get your Youtube API credentials from [here](https://console.cloud.google.com/apis/credentials?project=august-shield-332408)
- Have 3 tokens in order to minimise risk of error incase of quota completion

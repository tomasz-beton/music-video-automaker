from typing import Literal

from fastapi import FastAPI, Body

from src.media_manager import media_manager, MediaType
from src.movie_making import movie_maker

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello mvam!"}


@app.get("/media")
async def get_media(type: MediaType | None = None):
    return media_manager.media_list(type)


@app.post("/media/upload")
async def media_upload():
    raise NotImplementedError


@app.post("/media/from_youtube", status_code=201)
async def video_from_youtube(body=Body()):
    # TODO check if url is valid

    media = media_manager.download_from_youtube(body['url'], body['type'])

    return {
        "message": "Download started.",
        "type": media.type,
        "id": media.id,
        "name": media.name,
    }

@app.get("/movie_making")
async def get_movie_making_status():
    return {
        "status": movie_maker.status,
        "music_video_script": movie_maker.music_video_script,
        "music_video": movie_maker.music_video,
    }


@app.post("/movie_making", status_code=202)
async def post_movie_making(body=Body()):
    # TODO check if video_ids and audio_id are valid

    movie_maker.start(body["video_ids"], body["audio_id"])

    return {"message": "Movie making started."}

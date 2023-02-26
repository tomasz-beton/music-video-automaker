import os
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Literal

import pytube

from src.utils import threaded

from moviepy.editor import AudioFileClip


class Status(Enum):
    """Enum for the status of the movie making process."""

    INIT = 1
    LOADING = 2
    ANALYZING = 3  # future use - analysis straight after download
    READY = 4

MediaType = Literal["video", "audio"]


@dataclass
class MediaFile:
    """Media file. Either video or audio.

    Fields:
        id (str): Unique identifier
        path (str): Path to file
        source (str): Source of file. Can be 'youtube' or 'upload'.
        status (Status): Status of file.
    """

    path: str
    name: str

    source: Literal["youtube", "upload"]
    type: Literal["video", "audio"]

    status: Status = Status.INIT
    id: str = None

    def ready(self):
        return self.status == Status.READY

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())


class MediaManager:
    """Manages media files."""

    def __init__(self, path):
        self.path = path

        self.media: dict[str, MediaFile] = {}

    def media_list(self, type: MediaType | None = None):
        if type is None:
            return list(self.media.values())
        else:
            return [media for media in self.media.values() if media.type == type]

    def download_from_youtube(self, url, type: MediaType):
        new_media = MediaFile(
            path=None,
            name=None,
            type=type,
            source="youtube"
        )

        self.media[new_media.id] = new_media

        def on_complete(stream, path):
            setattr(new_media, "status", Status.READY)
            setattr(new_media, "path", path)

        yt = pytube.YouTube(url, on_complete_callback=on_complete)
        new_media.name = yt.title
        new_media.status = Status.LOADING

        @threaded
        def download():
            # TODO resolution when downloading video
            out_file = (
                yt.streams.filter(only_audio=(type == "audio"), only_video=(type != "audio"))
                .first()
                .download(
                    output_path=self.path + "/" + new_media.type,
                    filename=new_media.name + (".mp4" if type == "video" else ".wav"),
                    filename_prefix=new_media.id + "_"
                )
            )

            if type == "audio":
                # Convert to wav
                audio = AudioFileClip(out_file)
                audio.write_audiofile(out_file)
                audio.close()

        download()

        return new_media

    def get(self, id):
        return self.media[id]


media_manager = MediaManager(os.getenv("MEDIA_DIR"))

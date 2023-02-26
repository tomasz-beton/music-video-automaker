import time
from enum import Enum
from typing import List

from src.audio_analysis import get_audio_features
from src.generating_script import generate_script
from src.media_manager import media_manager
from src.utils import threaded
from src.video_analysis import get_video_features


class Status(Enum):
    """Enum for the status of the movie making process."""

    INIT = 1
    LOADING_MEDIA = 2
    ANALYZING_MEDIA = 3
    GENERATING_SCRIPT = 4
    RENDERING_VIDEO = 5
    FINISHED = 6
    STOPPED = 7


class MovieMaker:
    def __init__(self):
        self.status = Status.INIT
        self.music_video_script = None
        self.music_video = None

    @threaded
    def start(self, video_ids: List[str], audio_id: str):
        """Starts the movie making process.

        Args:
            video_ids (list of str): IDs of the videos.
            audio_id (str): ID of the audio

        Note: The video and audio ID should be checked against the media manager.
        """
        # Get files from media manager. Wait for download if necessary.
        self.status = Status.LOADING_MEDIA
        while not all([media_manager.get(id).ready() for id in video_ids + [audio_id]]):
            time.sleep(0.2)

        videos = [media_manager.get(video_id) for video_id in video_ids]
        audio = media_manager.get(audio_id)

        # Get audio and video features. Try to get them from cache if possible. Wait for analysis if necessary.
        self.status = Status.ANALYZING_MEDIA
        video_features = [get_video_features(video) for video in videos]
        audio_features = get_audio_features(audio)

        # Generate script. Specify the method or something.
        self.status = Status.GENERATING_SCRIPT
        self.music_video_script = generate_script(video_features, audio_features)

        # Render video. Maybe optional?
        self.status = Status.RENDERING_VIDEO
        pass

        self.status = Status.FINISHED


movie_maker = MovieMaker()

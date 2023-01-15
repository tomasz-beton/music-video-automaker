import os

from scenedetect import SceneManager
from scenedetect import VideoManager
from scenedetect.detectors import AdaptiveDetector
# For caching detection metrics and saving/loading to a stats file
from scenedetect.stats_manager import StatsManager


def get_scene_list(
        filename, adaptive_threshold=3.0, luma_only=False, min_scene_len=15, min_delta_hsv=15.0, window_width=2
):
    """Detects scenes in a file

    Arguments:
        filename (str): Path to video file
        adaptive_threshold (float): Threshold for adaptive scene detection
        luma_only (bool): If true, only luma values are used for scene detection
        min_scene_len (int/FrameTimecode): Minimum length of scene in frames/seconds
        min_delta_hsv (float): Minimum delta between scene frames in HSV color space
        window_width (int): Width of rolling average window for scene detection

    Returns:
        list: List of scene start and end times in seconds
    """

    video_manager = VideoManager([filename])
    stats_manager = StatsManager()
    scene_manager = SceneManager(stats_manager)

    scene_manager.add_detector(
        AdaptiveDetector(video_manager, adaptive_threshold, luma_only, min_scene_len, min_delta_hsv, window_width)
    )

    stats_path = f"{filename}.stats.csv"

    try:
        if os.path.exists(stats_path):
            with open(stats_path, "r") as stats_file:
                stats_manager.load_from_csv(stats_file)

        video_manager.set_downscale_factor()
        video_manager.start()

        scene_manager.detect_scenes(frame_source=video_manager)

        scene_list = scene_manager.get_scene_list()

        if stats_manager.is_save_required():
            base_timecode = video_manager.get_base_timecode()
            with open(stats_path, "w") as stats_file:
                stats_manager.save_to_csv(stats_file, base_timecode)

    finally:
        video_manager.release()

    return scene_list

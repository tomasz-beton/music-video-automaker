from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect.detectors import AdaptiveDetector

from scenedetect import video_splitter


def get_scene_list(filename, adaptive_threshold=3.0, luma_only=False, 
        min_scene_len=15, min_delta_hsv=15.0, window_width=2):
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
    scene_manager = SceneManager()

    scene_manager.add_detector(AdaptiveDetector(video_manager, adaptive_threshold, luma_only, 
        min_scene_len, min_delta_hsv, window_width))

    video_manager.set_downscale_factor()
    video_manager.start()

    scene_manager.detect_scenes(frame_source=video_manager)

    video_manager.release()

    return scene_manager.get_scene_list()

def split_scene(filename, out_dir):
    """Splits video file on detected cuts, saves in separate files"""

    scene_list = get_scene_list(filename)
    print(scene_list)

    filename_no_path = filename.split('/')[-1]
    filename_no_ext = filename_no_path.split('.')[0]

    if video_splitter.is_ffmpeg_available():
        video_splitter.split_video_ffmpeg([filename], scene_list, f'{out_dir}$VIDEO_NAME-$SCENE_NUMBER.mp4', filename_no_ext)
    else:
        print('ffmpeg not available')
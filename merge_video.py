import ffmpeg
from scenedetect import FrameTimecode

def merge_video(video_path, audio_path, output_path, cut_list):
    """ Merges a video with an audio file depending on the cut list

    Args:
        video_path (str): Path to video file
        audio_path (str): Path to audio file
        output_path (str): Path to output file
        cut_list (list): List of tuples (start, end)

    Returns:
        None
    """

    select_list = [f'between(t,{cut[0].get_seconds()},{cut[1].get_seconds()})' for cut in cut_list]

    # Trim audio to match video length if needed    
    length = sum([cut[1].get_seconds() - cut[0].get_seconds() for cut in cut_list])
    audio = ffmpeg.input(audio_path)
    audio = ffmpeg.filter(audio, 'aselect', f'between(t,0,{length})')

    (
        ffmpeg
        .input(video_path)
        .filter('select', '+'.join(select_list))
        .setpts('N/FRAME_RATE/TB')
        .concat(audio, a=1)
        .output(output_path)
        .overwrite_output()
        .run()
    )
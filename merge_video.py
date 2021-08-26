from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

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
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    clips = [video.subclip(start, end) for start, end in cut_list]
    video = concatenate_videoclips(clips)
    video = video.set_audio(audio)

    video.write_videofile(output_path)


def get_cut_list(cut_times, tempo, first_beat, audio_len):
    """
    Makes cut list using simple methods. Assumes constant tempo.

    Args:
        cut_times (list): List of cuts in a original video
        tempo (float): Tempo of the song
        first_beat (float): Time of first beat
        audio_len (float): Length of an audio file

    Returns:
        cut_list (list of (float, float)) : List of cuts to be glued into a video
    """
    four_beat = 4*60/tempo

    cut_list = []
    total_len = 0

    # initial, before beat starts
    cut_list.append( (0, first_beat) ) 
    total_len+= first_beat

    i = 0
    while i<len(cut_times)-1 and total_len<audio_len:
        cut_len = (cut_times[i+1]-cut_times[i])//four_beat
        if cut_len>0:
            cut_list.append( (cut_times[i], cut_times[i] + cut_len ) )
            total_len+=first_beat
        i+=1

    # reducing last cut so it ends when audio does
    if total_len>audio_len:
        cut_len[-1][1] -= total_len-audio_len

    return cut_list

def ts_to_frame(cut_list, fps):
    """Converts cut_list from float timestamps to frame numbers assuming constant fps"""
    time_sum = 0
    frame_sum = 0
    for cut in cut_list:
        time_sum += cut[1] - cut[0]
        a, b = int(cut[0]*fps), int(cut[0]*fps) + int(time_sum*fps- frame_sum)
        frame_sum += b - a
        yield a, b

from scenedetect.frame_timecode import FrameTimecode
def ts_to_FrameTimecode(cut_list, fps):
    """Converts cut_list from float timestamps to FrameTimecode objects assuming constant fps"""
    time_sum = 0
    frame_sum = 0
    for cut in cut_list:
        time_sum += cut[1] - cut[0]
        a, b = int(cut[0]*fps), int(cut[0]*fps) + int(time_sum*fps- frame_sum)
        frame_sum += b - a
        yield FrameTimecode(a, fps), FrameTimecode(b, fps)

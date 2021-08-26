from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from random import shuffle

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


def get_cut_list(cut_times, tempo, first_beat, audio_len, method='delay'):
    """
    Makes cut list using simple methods. Assumes constant tempo.

    Args:
        cut_times (list): List of cuts in a original video
        tempo (float): Tempo of the song
        first_beat (float): Time of first beat
        audio_len (float): Length of an audio file
        method (str): method

    Returns:
        cut_list (list of (float, float)) : List of cuts to be glued into a video
    """
    bar = 4*60/tempo # bar in this case lasts four beats

    cut_list = []

    # initial, before beat starts
    cut_list.append( (0, first_beat) ) 

    # we need not to repeat the begining
    i = 0
    while cut_times[i] < first_beat:
        i+=1

    # cutting up everything into bar length cuts
    all_cuts = []
    if method == 'delay':
        delay = 1
        while i<len(cut_times)-1:
            cut = cut_times[i], cut_times[i+1]
            all_cuts += [ (cut[0]+n*(bar+delay), cut[0]+n*(bar+delay) + bar) for n in range( int((cut[1]-cut[0])/(bar+delay)) )]
            i+=1

    elif method == 'pseudochrono':
        while i<len(cut_times)-1:
            cut = cut_times[i], cut_times[i+1]
            all_cuts += [ (cut[0]+n*bar, cut[0]+(n+1)*bar) for n in range( int((cut[1]-cut[0])/bar) )]
            i+=1

        for i in range( (len(all_cuts)+1)//4 ):
            all_cuts[4*i+1], all_cuts[4*i+2] = all_cuts[4*i+2], all_cuts[4*i+1]

    elif method == 'random':
        while i<len(cut_times)-1:
            cut = cut_times[i], cut_times[i+1]
            all_cuts += [ (cut[0]+n*bar, cut[0]+(n+1)*bar) for n in range( int((cut[1]-cut[0])/bar) )]
            i+=1

        shuffle(all_cuts)

    n_cuts = int( (audio_len-first_beat)/bar + 1)
    cut_list += all_cuts[:n_cuts]

    return cut_list

def fix_ts(cut_list, fps):
    """Converts cut_list from float timestamps to frame numbers assuming constant fps"""
    fixed_cut_list = []

    time_sum = 0
    frame_sum = 0
    for cut in cut_list:
        time_sum += cut[1] - cut[0]
        a, b = int(cut[0]*fps), int(cut[0]*fps) + int(time_sum*fps- frame_sum)
        frame_sum += b - a
        fixed_cut_list.append( (a/fps, b/fps) )

    return fixed_cut_list
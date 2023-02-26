from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips


def merge_video(video_path, audio_path, output_path, cut_list):
    """Merges a video with an audio file depending on the cut list

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

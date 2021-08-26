from librosa.core import get_duration
from beat_detect import get_beat_times
from scene_detect import get_scene_list
from merge_video import merge_video, get_cut_list

from sys import argv

if __name__ == '__main__':
    if len(argv) < 4:
        print('Usage: python merge_testing.py <video_path> <audio_path> <output_path>')
    else:
        video_path = argv[1]
        audio_path = argv[2]
        output_path = argv[3]

        scene_list = get_scene_list(video_path)
        beat_times, tempo = get_beat_times(audio_path)
        audio_length = get_duration(filename=audio_path)

        scene_cuts = [scene[1].get_seconds() for scene in scene_list]
        cut_list = get_cut_list(scene_cuts, tempo, beat_times[0], audio_length)

        merge_video(video_path, audio_path, output_path, cut_list)

from pydub import AudioSegment # to read mp3s 
import librosa # audio analysis 

from sys import argv
import numpy as np
from time import sleep, time

def read_mp3(filename):
    """MP3 to numpy array"""
    a = AudioSegment.from_mp3(filename)
    y = np.array(a.get_array_of_samples(), dtype=np.float32) / 2**15
    
    if a.channels == 2:
        y = y.reshape((-1, 2))
        y = y.mean(axis=1) # stripping to mono

    # reducing sample rate (div by 2)
    y = y[::2]
    sr = a.frame_rate//2
      
    return y, sr
    
def read_wav(filename):
    """WAV to numpy array"""
    y, sr = librosa.load(filename)
    return y, sr

def read_any(filename):
    """WAV or MP3 to numpy array"""
    if filename.endswith('.mp3'):
        return read_mp3(filename)
    elif filename.endswith('.wav'):
        return read_wav(filename)
    else:
        print("Unknown file extension")
        # exception or sth
        return 
    
def mp3_to_wav(src, dst=None):
    """Exports mp3 file to wav"""
    dst = dst or src.replace('.mp3', '.wav')
    audio = AudioSegment.from_mp3(src)
    audio.export(dst, format="wav")

def get_beat_times(filename=None, y=None, sr=None):
    """Detects beat times from filename or np.arrray"""
    if filename is not None:
        y, sr = read_any(filename)
    if y is not None and sr is not None:
        pass # y, sr already loaded
    else:
        print("Something wrong with the arguments")
        return
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    return beat_times, tempo

from pydub import AudioSegment # to read mp3s 
import librosa # audio analysis 

from sys import argv
import numpy as np
from time import sleep, time

from scipy.stats import lognorm, uniform

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

def get_beat(y, sr, full=False):
    """
    Info bout beat.

    Args:
        y (np.array): audio
        sr (int): sampling rate
        full (bool): If true, returns full beat times instead of first beat

    Returns:
        tempo (float)
        first_beat (float) (or beat_times (np.array))
    """
    onset_env = librosa.onset.onset_strength(y, sr=sr)
    prior = uniform(30, 300)  # uniform over 30-300 BPM
    utempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, prior=prior)[0]

    _, beat_times = librosa.beat.beat_track(y=y, sr=sr, units='time', bpm=utempo)
    return utempo, beat_times[0] if not full else beat_times

def get_audio_len(y, sr):
    """Returns audio length"""
    return librosa.get_duration(y=y, sr=sr)

def get_energy(y, sr, window=None):
    """
    Energy of the song.

    Args:
        y (np.array): audio
        sr (int): sampling rate
        window (float):  length of window for a moving average, 
            best if multiple of a bar length (2 bars by default)

    Returns:
        energy (np.array): array with values 0,1,2 describing energy level,
            len of array equal to len of audio in full seconds
    """
    
    onset_env = librosa.onset.onset_strength(y, sr=sr)
    times = librosa.times_like(onset_env)
    rate = 1/times[1]

    window = int(window*rate) if window else int(4*60/get_beat(y, sr)[0]*rate)

    onset_env = np.convolve(onset_env, np.ones(window), 'same') / window
    energy = np.array([onset_env[times==i].mean() for i in range(int(get_audio_len(y, sr))+1)])

    # scaling energy: 0, 1, 2 - 0 being the fastest
    # this need more work
    energy = np.trunc( 3 - 2.9*energy/np.max(energy) )

    return energy
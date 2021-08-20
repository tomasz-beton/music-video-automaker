from pydub import AudioSegment # to read mp3s 
import librosa # audio analysis 
import simpleaudio as sa # to play

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
      
    return y, a.frame_rate
    
def read_wav(filename):
    """WAV to numpy array"""
    return librosa.load(filename)

def read_any(filename):
    """WAV or MP3 to numpy array"""
    if filename.endswith('.mp3'):
        return read_mp3(filename)
    elif filename.endswith('.wav'):
        return read_wav(filename)
    else:
        print("nieznany format")
        # exception
        return (None, None)
    
def mp3_to_wav(src, dst=None):
    """Exports mp3 file to wav"""
    dst = dst or src.replace('.mp3', '.wav')
    audio = AudioSegment.from_mp3(src)
    audio.export(dst, format="wav")
    
def play(filename=None, y=None, sr=None):
    """Plays from filename or np.arrray"""
    if filename is not None:
        return sa.WaveObject.from_wave_file(filename).play()
    if y is not None and sr is not None:
        y = y * (2**15 - 1) / np.max(np.abs(y))
        return sa.WaveObject(y.astype(np.int16), 1, 2, sr).play()

def get_beat_times(filename=None, y=None, sr=None):
    """Detects beat times from filename or np.arrray"""
    if filename is not None:
        y, sr = read_any(filename)
    if y is not None and sr is not None:
        pass # czyli już git jest
    else:
        print("zle podano cos")
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    return beat_times, tempo

def visualise_beats(filename, playtime=15):
    """Prints beat markers on beat"""

    print("reading... ", end="")
    y, sr = read_any(filename)
    print(f"done, sr={sr}")
    
    print("getting beat times... ", end="")
    beat_times, tempo = get_beat_times(y=y, sr=sr)
    print(f"done, tempo={tempo}")
    
    print('playing... ')
    play_obj = play(y=y, sr=sr)
    
    start_t=time()
    i=0
    
    def print_beat(i):
        print((' '*10).join(['X' if i%n==0 else '-' for n in [1, 2, 4, 8, 3, 5]]) )
    print("\nEvery n'th beat markers: ")
    print((' '*10).join([str(n) for n in[1, 2, 4, 8, 3, 5]]))

    while True:
        t = time() - start_t
        if t>playtime:
            break
        if i<len(beat_times) and beat_times[i]<t:
            print_beat(i)
            i+=1
        sleep(0.001)
        
    play_obj.stop()

if __name__ == '__main__':
    if len(argv) < 2:
        print("Usage: 'python beat_detect.py <song_file> [<playback_length>]")
    elif len(argv) == 2:
        visualise_beats(argv[1], 20)
    else:
        visualise_beats(argv[1], float(argv[2]))
from beat_detect import get_beat_times, read_any
from scene_detect import get_scene_info

import cv2
import numpy as np
import simpleaudio as sa
from time import sleep, time
from sys import argv

def visualise_cuts(filename, sensitivity):
    """Prints markers on video cuts"""

    print("Visualising cuts")
    print("getting cut times... ", end="")
    cut_times = get_scene_info(filename, sensitivity)
    print(f"done, n={len(cut_times)-1}")

    print("Playing video (press q to stop)")
    cap = cv2.VideoCapture(filename)
    if (cap.isOpened()== False): 
        print("Error opening video file")
        return

    delay = 1/cap.get( cv2.CAP_PROP_FPS )
    frame_n= 1
    start_t=time()
    i=1

    while(cap.isOpened()):
        ret, frame = cap.read()
        if cv2.waitKey(1) & 0xFF == ord('q') or ret==False:
            break

        cv2.imshow('Video', frame)

        t = time() - start_t
        if i<len(cut_times) and cut_times[i]<t:
            print(f"CUT #{i}", '-'*(1+i%3))
            i+=1

        sleep( max(frame_n*delay-t, 0) )
        frame_n+=1
        
    cap.release()
    cv2.destroyAllWindows()


def play_audio(filename=None, y=None, sr=None):
    """Plays from filename or np.arrray"""
    if filename is not None:
        return sa.WaveObject.from_wave_file(filename).play()
    if y is not None and sr is not None:
        y = y * (2**15 - 1) / np.max(np.abs(y))
        return sa.WaveObject(y.astype(np.int16), 1, 2, sr).play()

def visualise_beats(filename, playtime=15):
    """Prints beat markers on beat"""

    print("Visualising beats")
    print("reading audio... ", end="")
    y, sr = read_any(filename)
    print(f"done, sr={sr}")
    
    print("getting beat times... ", end="")
    beat_times, tempo = get_beat_times(y=y, sr=sr)
    print(f"done, tempo={tempo}")
    
    print('playing... (Ctrl+C to stop)')
    play_obj = play_audio(y=y, sr=sr)
    
    start_t=time()
    i=0
    
    def print_beat(i):
        print((' '*10).join(['X' if i%n==0 else '-' for n in [1, 2, 4, 8, 3, 5]]) )
    print("\nEvery n'th beat markers: ")
    print((' '*10).join([str(n) for n in[1, 2, 4, 8, 3, 5]]))

    while True:
        t = time() - start_t
        if i<len(beat_times) and beat_times[i]<t:
            print_beat(i)
            i+=1

        sleep(0.01)
        
    play_obj.stop()


if __name__ == '__main__':
    if len(argv) < 2:
        print("Usage: 'python testing.py <filename> [other params]")
    else:
        if argv[1].endswith('.mp4') or argv[1].endswith('.avi'):
            visualise_cuts(argv[1], argv[2] if len(argv)>2 else 0.4)

        elif argv[1].endswith('.mp3') or argv[1].endswith('.wav'):
            visualise_beats(argv[1])

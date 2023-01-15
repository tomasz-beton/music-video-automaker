from sys import argv
from time import sleep, time

import cv2
import numpy as np
import simpleaudio as sa

from beat_detect import get_beat_times, read_any, get_beat_times_plp
from scene_detect import get_scene_list


def visualise_cuts(filename, threshold):
    """Prints markers on video cuts"""

    print("Visualising cuts")
    print("getting cut times... ", end="")
    scene_list = get_scene_list(filename, threshold)
    cut_times = [scene[0].get_seconds() for scene in scene_list]
    print(f"done, n={len(cut_times) - 1}")

    print("Playing video (press q to stop)")
    cap = cv2.VideoCapture(filename)
    if cap.isOpened() == False:
        print("Error opening video file")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    delay = 1 / cap.get(cv2.CAP_PROP_FPS)

    frame_n = 1
    start_t = time()
    i = 1

    while cap.isOpened():
        ret, frame = cap.read()
        if cv2.waitKey(1) & 0xFF == ord("q") or ret == False:
            break

        t = time() - start_t
        if i < len(cut_times) and cut_times[i] < t:
            print(f"CUT #{i}", "-" * (1 + i % 3))
            frame = cv2.rectangle(frame, (50, 50), (width - 50, height - 50), (0, 0, 255), 15)
            frame = cv2.rectangle(frame, (50, 50), (width - 50, height - 50), (255, 255, 0), 3)
            i += 1

        frame = cv2.putText(frame, f"{i - 1}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Video", frame)

        t = time() - start_t
        sleep(max(frame_n * delay - t, 0))
        frame_n += 1

    cap.release()
    cv2.destroyAllWindows()


def play_audio(filename=None, y=None, sr=None):
    """Plays from filename or np.arrray"""
    if filename is not None:
        return sa.WaveObject.from_wave_file(filename).play()
    if y is not None and sr is not None:
        y = y * (2 ** 15 - 1) / np.max(np.abs(y))
        return sa.WaveObject(y.astype(np.int16), 1, 2, sr).play()


def visualise_beats(filename, plp):
    """Prints beat markers on beat"""

    print("Visualising beats")
    print("reading audio... ", end="")
    y, sr = read_any(filename)
    print(f"done, sr={sr}")

    print("getting beat times... ", end="")
    if plp == "plp":
        beat_times, tempo = get_beat_times_plp(y=y, sr=sr)
    elif plp:
        beat_times, tempo = get_beat_times_plp(y=y, sr=sr, lognorm_val=int(plp))
    else:
        beat_times, tempo = get_beat_times(y=y, sr=sr)
    print(f"done, tempo={np.around(tempo, 3)}, first beat at {np.around(beat_times[0], 2)}")

    print("playing... (Ctrl+C to stop)")
    play_obj = play_audio(y=y, sr=sr)

    start_t = time()
    i = 0

    def print_beat(i):
        print((" " * 10).join(["X" if i % n == 0 else "-" for n in [1, 2, 4, 8, 3, 5]]))

    print("\nEvery n'th beat markers: ")
    print((" " * 10).join([str(n) for n in [1, 2, 4, 8, 3, 5]]))

    while True:
        t = time() - start_t
        if i < len(beat_times) and beat_times[i] < t:
            print_beat(i)
            i += 1

        sleep(0.01)

    play_obj.stop()


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: 'python testing.py <filename> [other params like threshold]")
    else:
        if argv[1].endswith(".mp4") or argv[1].endswith(".avi"):
            visualise_cuts(argv[1], argv[2] if len(argv) > 2 else 3.0)

        elif argv[1].endswith(".mp3") or argv[1].endswith(".wav"):
            visualise_beats(argv[1], argv[2] if len(argv) > 2 else None)
        else:
            print("Unknown file extension")

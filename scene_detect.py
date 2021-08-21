import ffmpeg
import re

def get_scene_info(filename):
    _, info = (
        ffmpeg
        .input(filename)
        .filter('select', 'gt(scene, 0.4)')
        .filter('showinfo')
        .output('pipe:', format='null')
        .run(capture_stderr=True, quiet=True)
    )

    info = re.findall(r'pts_time:[0-9.]*', str(info))
    info = [float(x.split(':')[1]) for x in info]
    info.insert(0, 0.0)

    return info

def split_scene(filename, out_dir):
    info = get_scene_info(filename)
    for i in range(len(info) - 1):
        start = info[i]
        end = info[i + 1]
        out_filename = '{}/{:06d}.mp4'.format(out_dir, i)
        print('Splitting {} from {} to {}'.format(filename, start, end))
        (
            ffmpeg
            .input(filename, ss=start, to=end)
            .output(out_filename)
            .run()
        )

split_scene('./test-data/short.mp4', './test-data/split/short')
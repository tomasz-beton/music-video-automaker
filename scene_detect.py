import ffmpeg
import re

def get_scene_info(filename, sensitivity):
    """Returns timestamps of cuts"""
    _, info = (
        ffmpeg
        .input(filename)
        .filter('select', f'gt(scene, {sensitivity})')
        .filter('showinfo')
        .output('pipe:', format='null')
        .run(capture_stderr=True, quiet=True)
    )

    info = re.findall(r'pts_time:[0-9.]*', str(info))
    info = [float(x.split(':')[1]) for x in info]
    info.insert(0, 0.0)

    return info

def split_scene(filename, out_dir, sensitivity=0.4):
    """Splits video file on detected cuts, saves in separate files"""

    info = get_scene_info(filename, sensitivity)
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

if __name__ == '__main__':
    split_scene('./cats.mp4', './split/')
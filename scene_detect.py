import ffmpeg
import re

_, info = (
    ffmpeg
    .input('test-data/short.mp4')
    .filter('select', 'gt(scene, 0.4)')
    .filter('showinfo')
    .output('pipe:', format='null')
    .run(capture_stderr=True, quiet=True)
)

info = re.findall(r'pts_time:[0-9.]*', str(info))
info = [float(x.split(':')[1]) for x in info]
info.insert(0, 0.0)

print(info)

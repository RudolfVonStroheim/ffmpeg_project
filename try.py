import ffmpeg
from json import dump

probe = ffmpeg.probe('input/inp.mkv')
with open('out.json', 'w') as f:
    dump(probe, f)

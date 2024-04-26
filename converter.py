import ffmpeg
from subprocess import run


class Converter:
    def __init__(self, filename):
        probe = ffmpeg.probe(f'input/{filename}')
        self.file_data = probe["format"]
        streams = probe["streams"]
        self.video = []
        self.audio = []
        self.sub = []
        for stream in streams:
            st_type = stream["codec_type"]
            match st_type:
                case "video":
                    info = {"index": stream["index"], "codec_name": stream["codec_name"]}
                    self.video.append(stream)
                case "audio":
                    self.audio.append(stream)
                case "subtitle":
                    self.sub.append(stream)
        self.update_codecs(filename.split('.')[-1])
        self.orig_form = filename.split('.')[-1]

    def update_codecs(filename):
        self.audio_codecs = self.get_audio_codecs(filename)
        self.video_codecs = self.get_video_codecs(filename)
        self.sub_codecs = self.get_sub_codecs(filename)

    def get_audio_codecs(filename):
        cm

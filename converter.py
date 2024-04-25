import ffmpeg


class Converter:
    def __init__(self, filename):
        probe = ffmpeg.probe(filename)
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
                case

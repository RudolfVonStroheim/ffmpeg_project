import ffmpeg
from subprocess import run


class Converter:

    formats = { 
        'matroska': 'mkv',
    }

    def __init__(self, filename):
        probe = ffmpeg.probe(f'input/{filename}')
        self.file_data = probe["format"]
        streams = probe["streams"]
        self.streams_changed = False
        self.video = []
        self.audio = []
        self.vcodec = "copy"
        self.acodec = "copy"
        self.scodec = "copy"
        self.sub = []
        for stream in streams:
            st_type = stream["codec_type"]
            match st_type:
                case "video":
                    self.video.append(stream)
                case "audio":
                    self.audio.append(stream)
                case "subtitle":
                    self.sub.append(stream)
        self.update_codecs(filename.split('.')[-1])
        self.filename_old = filename

    def update_codecs(self, filename):
        self.audio_codecs = self.get_audio_codecs(filename)
        self.video_codecs = self.get_video_codecs(filename)
        self.sub_codecs = self.get_sub_codecs(filename)

    def get_audio_codecs(self, filename):
        command = ['ffmpeg', '-codecs', "-f", filename, '-hide_banner']
        result = run(command, capture_output=True, text=True)
        output = result.stdout
        codecs = []
        for line in output.split('\n'):
            if line.startswith(' D.A') or line.startswith(".D.A") or line.startswith(" D A"):
                parts = line.split()
                codec = parts[1]
                codecs.append(codec)
        return codecs

    def get_video_codecs(self, filename):
        command = ['ffmpeg', '-codecs', "f", filename, '-hide_banner']
        result = run(command, capture_output=True, text=True)
        output = result.stdout
        codecs = []
        for line in output.split('\n'):
            if line.startswith(' D.V'):
                parts = line.split()
                codec = parts[1]
                codecs.append(codec)
        return codecs

    def get_sub_codecs(self, filename):
        command = ['ffmpeg', '-codecs', "-f", filename, '-hide_banner']
        result = run(command, capture_output=True, text=True)
        output = result.stdout
        codecs = []
        for line in output.split('\n'):
            if line.startswith(' D.S'):
                parts = line.split()
                codec = parts[1]
                codecs.append(codec)
        return codecs

    def get_streams(self):
        return {"video": self.video, "audio": self.audio, "subs": self.sub}

    def change_streams(self, indexes):
        input_maps = ["-map 0"]
        for v_index in indexes.get("video", []):
            input_maps.append(f'-0:{v_index}')
        for a_index in indexes.get("audio", []):
            input_maps.append(f'-0:{a_index}')
        for s_index in indexes.get("sub", []):
            input_maps.append(f' -0:{s_index}')
        self.maps = " ".join(input_maps)
        print(self.maps)

    def change_video_codec(self, codec):
        if codec in self.video_codecs:
            self.vcodec = codec

    def change_audio_codec(self, codec):
        if codec in self.audio_codecs:
            self.acodec = codec

    def change_sub_codec(self, codec):
        if codec in self.sub_codecs:
            self.scodec = codec

    def change_format(self, new_format):
        if new_format != "copy":
            new_format = self.formats[new_format] if new_format in self.formats else new_format
        else:
            new_format = self.filename_old.split('.')[-1]
        self.new_format = "." + new_format

    def process(self):
        if self.streams_changed:
            path = f'tmp/{self.filename_old}'
        else:
            path = f'input/{self.filename_old}'
        if self.new_format == "matroska":
            self.new_format = ".mkv"
        output_filename = ".".join(self.filename_old.split(".")[
                                   :-1]) + self.new_format
        output_path = f'output/{output_filename}'
        stream = ffmpeg.input(path)
        stream = ffmpeg.output(stream, output_path, vcodec=self.vcodec,
                               acodec=self.acodec, scodec=self.scodec, map=self.maps)
        ffmpeg.run(stream)

        return output_filename

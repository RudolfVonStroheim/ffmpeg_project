import ffmpeg
from subprocess import run


class Converter:
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
            if line.startswith('.D.A'):
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
            if line.startswith('.D.V'):
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
            if line.startswith('.D.S'):
                parts = line.split()
                codec = parts[1]
                codecs.append(codec)
                return codecs

    def get_streams(self):
        return {"video": self.video, "audio": self.audio, "subs": self.sub}

    def change_streams(self, indexes):
        filters = []
        for stream_type, indexes in indexes.items():
            for index in indexes:
                if stream_type == 'video':
                    filters.append(f'v:{index}')
                elif stream_type == 'audio':
                    filters.append(f'a:{index}')
                elif stream_type == 'subs':
                    filters.append(f's:{index}')
        stream = ffmpeg.input(f'input/{self.filename_old}')
        stream = ffmpeg.filter(stream, 'null', *filters)
        output_path = f'tmp/{self.filename_old}'
        stream = ffmpeg.output(stream, output_path, format='null')
        ffmpeg.run(stream)
        self.streams_changed = True

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
        self.new_format = new_format
        self.check_codecs()

    def check_codecs(self):
        if self.vcodec != "copy":
            vcodecs = self.get_video_codecs(self.new_format)
            if self.vcodec not in vcodecs:
                self.vcodec = vcodecs[0]
            self.video_codecs = vcodecs
        else:
            vcodec = self.video[0]["codec_name"]
            vcodecs = self.get_video_codecs(self.new_format)
            if vcodec not in vcodecs:
                self.vcodec = vcodecs[0]
            self.video_codecs = vcodecs

        if self.acodec != "copy":
            acodecs = self.get_audio_codecs(self.new_format)
            if self.acodec not in acodecs:
                self.acodec = acodecs[0]
            self.audio_codecs = acodecs
        else:
            acodec = self.audio[0]["codec_name"]
            acodecs = self.get_audio_codecs(self.new_format)
            if acodec not in acodecs:
                self.acodec = acodecs[0]
            self.audio_codecs = acodecs
        if self.scodec != "copy":
            scodecs = self.get_sub_codecs(self.new_format)
            if self.scodec not in scodecs:
                self.scodec = scodecs[0]
            self.sub_codecs = scodecs
        else:
            scodec = self.sub[0]["codec_name"]
            scodecs = self.get_sub_codecs(self.new_format)
            if scodec not in scodecs:
                self.scodec = scodecs[0]
            self.sub_codecs = scodecs

    def process(self):
        if self.streams_changed:
            path = f'tmp/{self.filename_old}'
        else:
            path = f'inp/{self.filename_old}'
        output_filename = self.filename_old.split(".")[:-1] + self.new_format
        output_path = f'out/"{output_filename}"'
        stream = ffmpeg.input(f'input/"{self.filename_old}"')
        stream = ffmpeg.output(stream, output_path, vcodec=self.vcodec, acodec=self.acodec, scodec=self.scodec)
        ffmpeg.run(stream)

        return output_filename


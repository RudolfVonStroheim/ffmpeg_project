import ffmpeg
from json import dump

# Замените 'input_file' на путь к вашему файлу
input_file = 'input/inp.mp4'

# Получаем информацию о потоках файла
probe = ffmpeg.probe(input_file)
with open("out.json", "w") as f:
    dump(probe, f)
streams = probe['streams']

print("Информация о потоках файла:")
for stream in streams:
        print(stream)


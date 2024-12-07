from pydub import AudioSegment


def convert_mp3_to_ogg(mp3_path: str, ogg_path: str):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(ogg_path, format="ogg")


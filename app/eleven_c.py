import os

from elevenlabs import ElevenLabs
from mutagen.mp3 import MP3


def tts(text):
    client = ElevenLabs(api_key=os.getenv('XI_API_KEY'))
    print(text, type(text))
    audio = client.generate(
        text=text,
        voice='JJhISFzXutRuYXDTm19w',
        model="eleven_multilingual_v2",
        output_format="mp3_22050_32",
    )
    filename = f'speech.mp3'
    with open(f'{filename}', "wb") as f:
        for chunk in audio:
            if chunk:
                f.write(chunk)
        f.close()
    # utils.convert_mp3_to_ogg(filename, f'speech.ogg')
    # info = mediainfo(f'speech.mp3')
    # return int(float(info['duration']))

    audio_info = MP3(f'speech.mp3')
    duration = int(audio_info.info.length)
    return duration

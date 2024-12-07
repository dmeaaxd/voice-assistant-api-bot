import os

from elevenlabs import ElevenLabs
from pydub.utils import mediainfo

from app import utils


def tts(text):
    client = ElevenLabs(api_key=os.getenv('XI_API_KEY'))
    print(text, type(text))
    audio = client.generate(
        text=text,
        voice='21m00Tcm4TlvDq8ikWAM',
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
    info = mediainfo(f'speech.mp3')
    return int(float(info['duration']))

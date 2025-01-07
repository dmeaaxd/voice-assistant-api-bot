import os

import dotenv
from elevenlabs import ElevenLabs
from mutagen.mp3 import MP3

dotenv.load_dotenv()

voice_id = os.getenv('VOICE_ID')

def tts(text):
    client = ElevenLabs(api_key=os.getenv('XI_API_KEY'))
    print(text, type(text))
    audio = client.generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v2",
        output_format="mp3_22050_32",
    )
    filename = f'speech.mp3'
    with open(f'{filename}', "wb") as f:
        for chunk in audio:
            if chunk:
                f.write(chunk)
        f.close()


    audio_info = MP3(f'speech.mp3')
    duration = int(audio_info.info.length)
    return duration

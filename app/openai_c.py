import os
import time

import dotenv
from openai import OpenAI
import openai

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

openai.api_key = os.getenv("OPENAI_API_KEY")


def create_thread():
    return client.beta.threads.create().id


# Добавление сообщения в поток (чтобы ассистент знал контекст)
def add_message_to_assistant(thread_id, assistant_id, message):
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role='user',
        content=message
    )


def generate(thread_id, text):
    add_message_to_assistant(thread_id, os.getenv("OPENAI_ID"), text)

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=os.getenv("OPENAI_ID")
    )

    while run.status != 'completed':
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        time.sleep(5)

    thread_messages = client.beta.threads.messages.list(thread_id)

    return thread_messages.data[0].content[0].text.value


async def transcribe_audio(file_path: str):
    try:
        with open(file_path, 'rb') as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            return response.text
    except Exception as e:
        print(f"Ошибка при распознавании: {e}")
        return

import asyncio
import logging
import os
import sys
from os import getenv
from pathlib import Path

import dotenv
import whisper
from aiogram import Bot, Dispatcher, html, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, File

from app import openai_c, db, eleven_c

dotenv.load_dotenv()
TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)

whisper_model = whisper.load_model("base")


async def handle_file(file: File, file_name: str, path: str):
    Path(path).mkdir(parents=True, exist_ok=True)
    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")


@router.message(lambda message: message.voice is not None)
async def voice_message_handler(message: Message):
    voice = await bot.get_file(message.voice.file_id)
    path = "voices"
    file_name = f"{voice.file_id}.ogg"
    file_path = f"{path}/{file_name}"

    await handle_file(file=voice, file_name=file_name, path=path)

    try:
        result = whisper_model.transcribe(file_path)
        recognized_text = result.get("text", "").strip()

        if recognized_text:
            await bot.send_chat_action(message.chat.id, 'record_voice')

            thread = db.get_thread(message.chat.id)
            bot_response = openai_c.generate(thread, recognized_text)

            # Генерация голосового ответа
            duration = eleven_c.tts(bot_response)

            # Отправляем голосовой ответ
            await message.answer_voice(FSInputFile(f"speech.mp3"), duration=duration)

        else:
            await message.answer("Я не понял ваше голосовое сообщение")
    except Exception as e:
        logging.error(f"Ошибка при распознавании: {e}")
        await message.answer("Я не понял ваше голосовое сообщение")

    os.remove(file_path)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    db.delete_thread(message.chat.id)
    thread_id = openai_c.create_thread()
    db.create_thread(message.chat.id, thread_id)
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! История общения сброшена.")


@router.message()
async def echo_handler(message: Message) -> None:
    await bot.send_chat_action(message.chat.id, 'record_voice')
    thread = db.get_thread(message.chat.id)
    text = openai_c.generate(thread, message.text)
    duration = eleven_c.tts(text)
    await message.answer_voice(FSInputFile(f'speech.mp3'), duration=duration)


async def main() -> None:
    await dp.start_polling(bot)


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
asyncio.run(main())

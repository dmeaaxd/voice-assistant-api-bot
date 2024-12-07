import asyncio
import logging
import sys
from os import getenv

import dotenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from app import openai_c, db, eleven_c

dotenv.load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    db.delete_thread(message.chat.id)
    thread_id = openai_c.create_thread()
    db.create_thread(message.chat.id, thread_id)
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! История общения сброшена.")


@dp.message()
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

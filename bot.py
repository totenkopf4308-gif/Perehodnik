import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
COVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover.jpg")

GREETING = (
    "Только лучшие треки\n"
    "Без воды и проходняка\n"
    "Заряжай плейлист\n"
    "⬇️Ссылки на соц.сети⬇️"
)

KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📢 Telegram-канал", url="https://t.me/rap_oboyma")],
        [InlineKeyboardButton(text="📸 Instagram", url="https://www.instagram.com/rap_oboyma")],
        [InlineKeyboardButton(text="🎵 TikTok", url="https://www.tiktok.com/@rap_oboyma")],
    ]
)

dp = Dispatcher()

# После первой отправки Telegram отдаёт file_id — дальше шлём по нему, это быстрее.
_cover_file_id = None


async def send_card(message: Message):
    global _cover_file_id
    photo = _cover_file_id or FSInputFile(COVER_PATH)
    sent = await message.answer_photo(photo, caption=GREETING, reply_markup=KEYBOARD)
    if _cover_file_id is None and sent.photo:
        _cover_file_id = sent.photo[-1].file_id


@dp.message(CommandStart())
async def start(message: Message):
    await send_card(message)


@dp.message()
async def any_message(message: Message):
    await send_card(message)


async def main():
    bot = Bot(BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

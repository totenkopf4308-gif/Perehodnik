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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def find_cover():
    """Ищем cover.jpg / cover.jpeg / cover.png в папке бота и подпапках, без учёта регистра."""
    for root, _dirs, files in os.walk(BASE_DIR):
        if ".venv" in root or ".git" in root:
            continue
        for name in files:
            if name.lower() in ("cover.jpg", "cover.jpeg", "cover.png"):
                return os.path.join(root, name)
    return None


COVER_PATH = find_cover()
print(f"BASE_DIR={BASE_DIR} COVER_PATH={COVER_PATH}", flush=True)
print("Files:", sorted(os.listdir(BASE_DIR)), flush=True)

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
    if _cover_file_id is None and not COVER_PATH:
        # Нет файла cover.jpg рядом с bot.py — шлём без картинки, чтобы бот не молчал
        await message.answer(GREETING, reply_markup=KEYBOARD)
        return
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

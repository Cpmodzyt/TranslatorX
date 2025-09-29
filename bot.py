import os
import pysubs2
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import FSInputFile
from googletrans import Translator
import asyncio

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

translator = Translator()

# Store user translation settings
user_settings = {}  # {user_id: {"src": "en", "dest": "si"}}


async def translate_text(text: str, src: str, dest: str) -> str:
    """Translate text using googletrans"""
    return translator.translate(text, src=src, dest=dest).text


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply(
        "👋 Welcome to Subtitle Translator Bot!\n\n"
        "Set your translation using `/translate <src> <dest>`\n"
        "Example: `/translate en si` → English → Sinhala\n\n"
        "Then send any subtitle file (.srt, .ass, .vtt) and it will auto-translate.\n"
        "Use `/status` to check your current language setting.",
        parse_mode=ParseMode.MARKDOWN
    )


@dp.message(Command("translate"))
async def set_translation(message: types.Message):
    parts = message.text.split()
    if len(parts) != 3:
        await message.reply("❌ Usage: `/translate <source> <target>`", parse_mode=ParseMode.MARKDOWN)
        return

    src, dest = parts[1], parts[2]
    user_settings[message.from_user.id] = {"src": src, "dest": dest}
    await message.reply(f"✅ Translation set: `{src}` → `{dest}`", parse_mode=ParseMode.MARKDOWN)


@dp.message(Command("status"))
async def status(message: types.Message):
    settings = user_settings.get(message.from_user.id)
    if settings:
        await message.reply(
            f"⚙️ Current translation:\n`{settings['src']}` → `{settings['dest']}`\n"
            f"Translator: Free googletrans 🌍",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await message.reply("ℹ️ You haven't set translation yet. Use `/translate en si`.")


@dp.message()
async def handle_file(message: types.Message):
    if not message.document:
        return

    settings = user_settings.get(message.from_user.id)
    if not settings:
        await message.reply("ℹ️ Please set translation first using `/translate <src> <dest>`")
        return

    src, dest = settings["src"], settings["dest"]

    file = await bot.get_file(message.document.file_id)
    file_path = f"{message.document.file_unique_id}_{message.document.file_name}"
    await bot.download_file(file.file_path, file_path)

    try:
        subs = pysubs2.load(file_path, encoding="utf-8")

        # Translate each line
        for line in subs:
            if line.text.strip():
                line.text = await translate_text(line.text, src, dest)

        out_file = file_path.replace(".", "_translated.")
        subs.save(out_file)

        await message.reply_document(FSInputFile(out_file))

        os.remove(file_path)
        os.remove(out_file)
    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))

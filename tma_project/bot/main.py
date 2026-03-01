import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def load_env(env_path: Path) -> dict:
    env = {}
    if not env_path.is_file():
        return env

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


async def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    env_values = load_env(project_root / ".env")

        bot_token = os.getenv("BOT_TOKEN") or env_values.get("BOT_TOKEN")
    webapp_url = os.getenv("WEBAPP_URL") or env_values.get("WEBAPP_URL") or "https://example.com"

    if not bot_token:
        raise RuntimeError("BOT_TOKEN is not set. Specify it in .env or environment variables.")
    bot = Bot(token=bot_token)
    dp = Dispatcher()

    me = await bot.get_me()
    logger.info("Бот запущен как @%s (id=%s)", me.username, me.id)

    @dp.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Открыть мини‑приложение",
                        web_app=WebAppInfo(url=webapp_url),
                    )
                ]
            ]
        )

        logger.info("Обработан /start от %s (id=%s)", message.from_user.username, message.from_user.id)
        await message.answer(
            "Привет! Нажми на кнопку, чтобы открыть мини‑приложение.",
            reply_markup=keyboard,
        )

    @dp.message()
    async def fallback_echo(message: Message) -> None:
        logger.info("Получено сообщение: %s от id=%s", message.text, message.from_user.id)
        await message.answer("Я тебя вижу 🙂 Напиши /start, чтобы открыть мини‑приложение.")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())



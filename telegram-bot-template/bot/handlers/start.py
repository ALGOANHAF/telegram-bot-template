# ── bot/handlers/start.py ─────────────────────────
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, db):
    user = message.from_user
    await message.answer(
        f"👋 Hello, <b>{user.first_name}</b>!\n\n"
        f"Welcome to the bot.\n"
        f"Use /help to see available commands."
    )
    await db.log_message(user.id, "/start", message.text)


@router.message(Command("help"))
async def cmd_help(message: Message, db):
    await message.answer(
        "📋 <b>Available Commands</b>\n\n"
        "/start — Start the bot\n"
        "/help  — Show this message\n"
        "/me    — Your profile info\n"
    )
    await db.log_message(message.from_user.id, "/help", message.text)

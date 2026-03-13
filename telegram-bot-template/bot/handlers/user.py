# ── bot/handlers/user.py ──────────────────────────
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("me"))
async def cmd_me(message: Message, db):
    user = message.from_user
    db_user = await db.get_user(user.id)

    joined = db_user["joined_at"].strftime("%Y-%m-%d") if db_user else "Unknown"
    last   = db_user["last_seen"].strftime("%Y-%m-%d %H:%M") if db_user else "Unknown"

    await message.answer(
        f"👤 <b>Your Profile</b>\n\n"
        f"🆔 ID       : <code>{user.id}</code>\n"
        f"📛 Name     : {user.full_name}\n"
        f"🔖 Username : @{user.username or 'N/A'}\n"
        f"📅 Joined   : {joined}\n"
        f"🕐 Last seen: {last}\n"
    )

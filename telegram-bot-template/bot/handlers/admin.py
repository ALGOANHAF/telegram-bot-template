# ── bot/handlers/admin.py ─────────────────────────
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config.settings import ADMIN_IDS

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# ── Admin Panel ────────────────────────────────────
@router.message(Command("admin"))
async def cmd_admin(message: Message, db):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔ Access denied.")

    total   = await db.get_user_count()
    banned  = await db.get_banned_count()
    active  = total - banned

    await message.answer(
        "🛠 <b>Admin Panel</b>\n\n"
        f"👥 Total users  : <b>{total}</b>\n"
        f"✅ Active users : <b>{active}</b>\n"
        f"🚫 Banned users : <b>{banned}</b>\n\n"
        "📌 <b>Commands:</b>\n"
        "/ban &lt;user_id&gt;    — Ban a user\n"
        "/unban &lt;user_id&gt; — Unban a user\n"
        "/broadcast &lt;msg&gt; — Send message to all\n"
        "/userinfo &lt;id&gt;  — Get user details\n"
    )


# ── Ban User ───────────────────────────────────────
@router.message(Command("ban"))
async def cmd_ban(message: Message, db):
    if not is_admin(message.from_user.id):
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].strip().isdigit():
        return await message.answer("❌ Usage: /ban <user_id>")

    target_id = int(args[1].strip())
    user = await db.get_user(target_id)
    if not user:
        return await message.answer("❌ User not found.")

    await db.ban_user(target_id)
    await message.answer(f"🚫 User <code>{target_id}</code> has been banned.")


# ── Unban User ─────────────────────────────────────
@router.message(Command("unban"))
async def cmd_unban(message: Message, db):
    if not is_admin(message.from_user.id):
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].strip().isdigit():
        return await message.answer("❌ Usage: /unban <user_id>")

    target_id = int(args[1].strip())
    await db.unban_user(target_id)
    await message.answer(f"✅ User <code>{target_id}</code> has been unbanned.")


# ── User Info ──────────────────────────────────────
@router.message(Command("userinfo"))
async def cmd_userinfo(message: Message, db):
    if not is_admin(message.from_user.id):
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].strip().isdigit():
        return await message.answer("❌ Usage: /userinfo <user_id>")

    target_id = int(args[1].strip())
    user = await db.get_user(target_id)
    if not user:
        return await message.answer("❌ User not found.")

    status = "🚫 Banned" if user["is_banned"] else "✅ Active"
    role   = "👑 Admin"  if user["is_admin"]  else "👤 User"

    await message.answer(
        f"👤 <b>User Info</b>\n\n"
        f"🆔 ID       : <code>{user['id']}</code>\n"
        f"📛 Name     : {user['first_name']} {user['last_name'] or ''}\n"
        f"🔖 Username : @{user['username'] or 'N/A'}\n"
        f"🎭 Role     : {role}\n"
        f"📊 Status   : {status}\n"
        f"📅 Joined   : {user['joined_at']}\n"
        f"🕐 Last seen: {user['last_seen']}\n"
    )


# ── Broadcast ──────────────────────────────────────
@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, db):
    if not is_admin(message.from_user.id):
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.answer("❌ Usage: /broadcast <message>")

    text  = args[1].strip()
    users = await db.get_all_users()

    sent = failed = 0
    for user in users:
        try:
            await message.bot.send_message(user["id"], f"📢 <b>Broadcast</b>\n\n{text}")
            sent += 1
        except Exception:
            failed += 1

    await message.answer(
        f"📢 <b>Broadcast Complete</b>\n\n"
        f"✅ Sent   : {sent}\n"
        f"❌ Failed : {failed}\n"
    )

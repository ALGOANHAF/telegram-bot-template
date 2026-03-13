# ── bot/middlewares/auth.py ────────────────────────
from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


class AuthMiddleware(BaseMiddleware):
    def __init__(self, db):
        self.db = db

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        user = event.from_user

        # ── Auto-register user ─────────────────────
        await self.db.add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )

        # ── Check ban ──────────────────────────────
        db_user = await self.db.get_user(user.id)
        if db_user and db_user["is_banned"]:
            if isinstance(event, Message):
                await event.answer("🚫 You are banned from using this bot.")
            return  # block handler

        # ── Pass db to handler ─────────────────────
        data["db"] = self.db
        return await handler(event, data)

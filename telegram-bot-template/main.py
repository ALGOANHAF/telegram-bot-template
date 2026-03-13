#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════╗
║         TELEGRAM BOT TEMPLATE                    ║
║         Built by ALGOANHAF                       ║
║         github.com/algoanhaf                     ║
╚══════════════════════════════════════════════════╝
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config.settings import BOT_TOKEN
from database.db import Database
from bot.handlers import start, admin, user
from bot.middlewares.auth import AuthMiddleware

# ── Logging Setup ─────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("🚀 Starting bot...")

    # ── Init Database ──────────────────────────────
    db = Database()
    await db.connect()
    await db.create_tables()
    logger.info("✅ Database connected")

    # ── Init Bot & Dispatcher ──────────────────────
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # ── Register Middlewares ───────────────────────
    dp.message.middleware(AuthMiddleware(db))
    dp.callback_query.middleware(AuthMiddleware(db))

    # ── Register Routers ──────────────────────────
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(user.router)

    logger.info("✅ Handlers registered")

    # ── Start Polling ──────────────────────────────
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("🤖 Bot is running...")
        await dp.start_polling(bot, db=db)
    finally:
        await db.close()
        await bot.session.close()
        logger.info("❌ Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())

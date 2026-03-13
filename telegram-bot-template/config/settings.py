# ── config/settings.py ────────────────────────────
import os
from dotenv import load_dotenv

load_dotenv()

# ── Bot ────────────────────────────────────────────
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
BOT_USERNAME: str = os.getenv("BOT_USERNAME", "your_bot_username")

# ── Admin ──────────────────────────────────────────
# Comma-separated Telegram user IDs
_admin_ids = os.getenv("ADMIN_IDS", "123456789")
ADMIN_IDS: list[int] = [int(x.strip()) for x in _admin_ids.split(",")]

# ── Database ───────────────────────────────────────
DB_HOST: str = os.getenv("DB_HOST", "localhost")
DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
DB_NAME: str = os.getenv("DB_NAME", "telegram_bot")
DB_USER: str = os.getenv("DB_USER", "root")
DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")

# ── Bot Behavior ───────────────────────────────────
MAX_RETRIES: int = 3
RATE_LIMIT: int = 1  # seconds between messages per user

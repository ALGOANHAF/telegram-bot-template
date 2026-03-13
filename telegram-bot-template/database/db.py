# ── database/db.py ─────────────────────────────────
import logging
import aiomysql
from config.settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.pool = None

    # ── Connection ─────────────────────────────────
    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=DB_HOST,
            port=DB_PORT,
            db=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            autocommit=True,
            minsize=1,
            maxsize=10,
        )

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    # ── Table Setup ────────────────────────────────
    async def create_tables(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id          BIGINT PRIMARY KEY,
                        username    VARCHAR(64),
                        first_name  VARCHAR(64),
                        last_name   VARCHAR(64),
                        is_banned   BOOLEAN DEFAULT FALSE,
                        is_admin    BOOLEAN DEFAULT FALSE,
                        joined_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
                        last_seen   DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )
                """)
                await cur.execute("""
                    CREATE TABLE IF NOT EXISTS messages_log (
                        id          INT AUTO_INCREMENT PRIMARY KEY,
                        user_id     BIGINT,
                        command     VARCHAR(64),
                        text        TEXT,
                        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """)
        logger.info("✅ Tables ready")

    # ── User Methods ───────────────────────────────
    async def get_user(self, user_id: int) -> dict | None:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                return await cur.fetchone()

    async def add_user(self, user_id: int, username: str,
                       first_name: str, last_name: str = None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO users (id, username, first_name, last_name)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        username   = VALUES(username),
                        first_name = VALUES(first_name),
                        last_name  = VALUES(last_name),
                        last_seen  = CURRENT_TIMESTAMP
                """, (user_id, username, first_name, last_name))

    async def ban_user(self, user_id: int):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "UPDATE users SET is_banned = TRUE WHERE id = %s", (user_id,))

    async def unban_user(self, user_id: int):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "UPDATE users SET is_banned = FALSE WHERE id = %s", (user_id,))

    async def get_all_users(self) -> list:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    "SELECT * FROM users WHERE is_banned = FALSE")
                return await cur.fetchall()

    async def get_user_count(self) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT COUNT(*) FROM users")
                result = await cur.fetchone()
                return result[0]

    async def get_banned_count(self) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT COUNT(*) FROM users WHERE is_banned = TRUE")
                result = await cur.fetchone()
                return result[0]

    # ── Log Methods ────────────────────────────────
    async def log_message(self, user_id: int, command: str, text: str):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO messages_log (user_id, command, text)
                    VALUES (%s, %s, %s)
                """, (user_id, command, text))

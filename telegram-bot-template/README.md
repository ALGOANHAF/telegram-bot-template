<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:1a1f35,100:2ea043&height=160&section=header&text=Telegram%20Bot%20Template&fontSize=40&fontColor=ffffff&fontAlignY=65&animation=fadeIn" width="100%"/>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://aiogram.dev)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**A production-ready Telegram bot template with MySQL, Admin Panel & Command Handlers**

</div>

---

## ✨ Features

- 🤖 **aiogram 3.x** — Modern async Telegram bot framework
- 🗄️ **MySQL Database** — Async connection pool via `aiomysql`
- 👑 **Admin Panel** — Ban/unban, broadcast, user info
- 🔐 **Auth Middleware** — Auto-registers users, blocks banned users
- 📋 **Command Handlers** — /start, /help, /me out of the box
- 🏗️ **Clean Architecture** — Modular handlers, middlewares, config

---

## 📁 Project Structure

```
telegram-bot-template/
├── main.py                  # Entry point
├── requirements.txt
├── .env.example
├── config/
│   └── settings.py          # All config from .env
├── database/
│   └── db.py                # MySQL pool + all queries
└── bot/
    ├── handlers/
    │   ├── start.py          # /start, /help
    │   ├── user.py           # /me
    │   └── admin.py          # /admin, /ban, /unban, /broadcast
    └── middlewares/
        └── auth.py           # Auto-register + ban check
```

---

## ⚡ Quick Start

**1. Clone the repo**
```bash
git clone https://github.com/algoanhaf/telegram-bot-template.git
cd telegram-bot-template
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Setup environment**
```bash
cp .env.example .env
# Edit .env with your values
```

**4. Create MySQL database**
```sql
CREATE DATABASE telegram_bot;
```

**5. Run the bot**
```bash
python main.py
```

---

## ⚙️ Configuration (`.env`)

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Your bot token from [@BotFather](https://t.me/BotFather) |
| `ADMIN_IDS` | Comma-separated admin Telegram IDs |
| `DB_HOST` | MySQL host (default: localhost) |
| `DB_NAME` | Database name |
| `DB_USER` | MySQL username |
| `DB_PASSWORD` | MySQL password |

---

## 📋 Admin Commands

| Command | Description |
|---------|-------------|
| `/admin` | Show admin panel & stats |
| `/ban <user_id>` | Ban a user |
| `/unban <user_id>` | Unban a user |
| `/userinfo <user_id>` | Get user details |
| `/broadcast <message>` | Send message to all users |

---

## 🗄️ Database Schema

```sql
users (id, username, first_name, last_name, is_banned, is_admin, joined_at, last_seen)
messages_log (id, user_id, command, text, created_at)
```
Tables are **auto-created** on first run.

---

## 💼 Need a Custom Bot?

Built something cool with this template? Need a fully custom bot for your business?

<div align="center">

[![Fiverr](https://img.shields.io/badge/Hire%20me%20on-Fiverr-1DBF73?style=for-the-badge&logo=fiverr&logoColor=white)](https://fiverr.com/algoanhaf)
[![GitHub](https://img.shields.io/badge/Follow-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/algoanhaf)

</div>

---

<div align="center">

Made with ❤️ by [ALGOANHAF](https://github.com/algoanhaf)

⭐ **Star this repo if it helped you!**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2ea043,50:1a1f35,100:0d1117&height=100&section=footer" width="100%"/>

</div>

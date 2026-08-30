import os
import aiosqlite

DB_PATH = "berry_broker.db"

async def init_sqlite():
    """Initialize the database and ensure table schema exists."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                balance INTEGER DEFAULT 1000,
                last_daily TEXT DEFAULT NULL,
                last_rob TEXT DEFAULT NULL
            )
        """)
        await db.commit()

async def get_user(user_id: int, username: str):
    """Retrieve user row, creating a new rookie entry with 1,000 Berries if missing."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()
            
        if not user:
            await db.execute(
                "INSERT INTO users (user_id, username, balance) VALUES (?, ?, ?)",
                (user_id, username, 1000)
            )
            await db.commit()
            async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
                user = await cursor.fetchone()
        else:
            await db.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
            await db.commit()
            
        return dict(user)

async def update_balance(user_id: int, amount: int):
    """Update a pirate's balance."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        await db.commit()

async def update_cooldown(user_id: int, column: str, timestamp_iso: str):
    """Update daily or rob timestamp."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"UPDATE users SET {column} = ? WHERE user_id = ?", (timestamp_iso, user_id))
        await db.commit()

async def get_top_pirates(limit: int = 5):
    """Fetch the richest pirates on the Grand Line."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT username, balance FROM users ORDER BY balance DESC LIMIT ?", (limit,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
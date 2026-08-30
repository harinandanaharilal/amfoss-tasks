import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import database as db

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"⚓ The Berry Broker is open for business as {bot.user.name} (ID: {bot.user.id})")
    print("--------------------------------------------------")

async def main():
    # Initialize SQLite table schema
    await db.init_sqlite()

    # Load Cogs
    initial_extensions = ["cogs.economy", "cogs.games", "cogs.fun"]
    for extension in initial_extensions:
        await bot.load_extension(extension)

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("DISCORD_TOKEN environment variable is missing from .env file!")

    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
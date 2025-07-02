import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import os
import pytz

from roblox_commands import roblox_command_setup

TOKEN = 'MTA2NTgzNDY0NzAyOTgyNTUzNg.G69w9t.zgcsYAL05pljFtev25sWkY1-ik1CE8YOZiqD1g'
CHANNEL_ID = 1150863912707821611  # Replace with your actual channel ID
IST = pytz.timezone("Asia/Kolkata")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

roblox_command_setup(bot)

async def wait_until_next_twenty():
    while True:
        now = datetime.now(IST)
        if now.minute < 20:
            target = now.replace(minute=20, second=0, microsecond=0)
        else:
            target = (now + timedelta(hours=1)).replace(minute=20, second=0, microsecond=0)
        wait_seconds = (target - now).total_seconds()
        print(f"[TimeLoop] Waiting {wait_seconds:.1f} seconds")
        await asyncio.sleep(wait_seconds)

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("@everyone Wake up! Harvest in 10 minutes!")

async def check_for_commands():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    while not bot.is_closed():
        if os.path.exists("command.txt"):
            with open("command.txt", "r") as f:
                content = f.read().strip()
            if content:
                await channel.send(content)
                with open("command.txt", "w") as f:
                    f.write("")
        await asyncio.sleep(3)

@bot.event
async def on_ready():
    print(f"[Startup] Logged in as {bot.user}")
    bot.loop.create_task(wait_until_next_twenty())
    bot.loop.create_task(check_for_commands())

bot.run(TOKEN)

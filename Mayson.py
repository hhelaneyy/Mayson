import asyncio
import os
import sqlite3
import sys
import time
import disnake
from disnake.ext import commands
import json
import openai

with open('config.json') as f:
    data = json.load(f)
    token = data["token"]
    prefix = data["prefix"]
    openai.api_key = data['gpt_token']

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)

@bot.event
async def on_ready():
    bot.start_time = time.time()
    print("Ваш виртуальный ассистент запущен.")
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command(description="Мейсон спать.")
async def restart(ctx):
    if ctx.author.id == bot.owner.id:
        await ctx.reply("🫗 Перезапускаюсь...")
        await asyncio.sleep(1)

        python = sys.executable
        os.execl(python, python, *sys.argv)

bot.run(token)
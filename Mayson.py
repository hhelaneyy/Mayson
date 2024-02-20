import asyncio
import os
import sqlite3
import sys
import time
import disnake
from disnake.ext import commands
import json
import openai

conn = sqlite3.connect('Mayson.db')
c = conn.cursor()

with open('config.json') as f:
    data = json.load(f)
    token = data["token"]
    prefix = data['prefix']
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

#@bot.event
#async def on_message(message):
    #c.execute("SELECT prefix FROM bot_settings WHERE user_id=? AND guild_id=?", (message.author.id, message.guild.id))
    #prefix = c.fetchone()
    #if prefix:
        #bot.command_prefix = prefix[0]
    #else:
        #default_prefix = ['mn.', '<@1133774791174803618> ']
        #bot.command_prefix = default_prefix
        #c.execute("INSERT OR IGNORE INTO bot_settings (user_id, guild_id, prefix) VALUES (?, ?, ?)", (message.author.id, message.guild.id, default_prefix))
        #conn.commit()
    
    #await bot.process_commands(message)

@bot.command(description="Мейсон спать.")
async def restart(ctx):
    if ctx.author.id == bot.owner.id:
        await ctx.reply("🫗 Перезапускаюсь...")
        await asyncio.sleep(1)

        python = sys.executable
        os.execl(python, python, *sys.argv)

bot.run(token)
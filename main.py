import os
import json
import asyncio
import sys
import traceback
import discord
from discord.ext import commands, tasks
import sqlite3

from dotenv.main import load_dotenv
# from dotenv import load_dotenv

bot = commands.Bot(command_prefix='.', case_insensitive=True)
bot.remove_command('help')

cog_list = ['cogs.Core', 'cogs.playercount','cogs.help']

# Events

@bot.event
async def on_ready():
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wordcount(
        guild_id TEXT,
        msg TEXT,
        channel_id TEXT,
        count INT
        )
        ''')
    print(f'Bot is Online logged in as {bot.user}')
    # return await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='twitch.tv/tesseract_tv'))
    return await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='Dofus'))


if __name__ == '__main__':
    for cog in cog_list:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(f'Failed to load cog {cog}', file=sys.stderr)
            traceback.print_exc()

load_dotenv()
token = os.environ['token']

bot.run(token)

import os
import json
import asyncio
import sys
import traceback
import discord
from discord.ext import commands, tasks
import sqlite3
import random

from dotenv.main import load_dotenv
# from dotenv import load_dotenv

bot = commands.Bot(command_prefix='.', case_insensitive=True)
# bot.remove_command('help')

# cog_list = ['cogs.Core', 'cogs.PercMgmt','cogs.help']
cog_list = ['cogs.Core', 'cogs.PercMgmt']

def main():
    # load in the cogs
    for cog in cog_list:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(f'Failed to load cog {cog}', file=sys.stderr)
            traceback.print_exc()
    
    # read the token from the .env file and start the bot
    load_dotenv()
    token = os.environ['TOKEN']
    bot.run(token)


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
    return await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='Dofus'))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        await bot.process_commands(message)
        return
    
    lookingFor = ['d-bk.net', 'dofusbook.net']
    replies = [
        'What\'s that?! Try this: https://dofuslab.io',
        '??? https://dofuslab.io',
        'C\'mon man go for https://dofuslab.io',
        'r u lost? ... https://dofuslab.io',
        'you are so close bb... here try this: https://dofuslab.io',
        'good attempt, but try this next time: https://dofuslab.io',
        'BRO!!!!!! https://dofuslab.io',
        'bruv ur slackin -> https://dofuslab.io',
        'https://dofuslab.io'
    ]
    if any(x in message.content.lower() for x in lookingFor):
        await message.reply(random.choice(replies))
    await bot.process_commands(message)

if __name__ == '__main__':
    main()
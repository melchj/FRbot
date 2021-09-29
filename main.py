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

bot = commands.Bot(command_prefix='.', case_insensitive=True)

cog_list = ['cogs.Core', 'cogs.PercMgmt', 'cogs.Tingo']

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
    # create sqlite3 main database (for perc point scorekeeping)
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS percscore(
        guild_id INT,
        channel_id INT,
        player TEXT,
        win INT,
        loss INT,
        nocontest INT
        )
        ''')

    # create sqlite3 tingo database
    db2 = sqlite3.connect('tingo.sqlite')
    cursor2 = db2.cursor()
    cursor2.execute('''
        CREATE TABLE IF NOT EXISTS tingodex(
        guild_id INT,
        channel_id INT,
        trainer_id INT,
        victim_name TEXT,
        image_path TEXT
        )
        ''')

    print(f'Bot is Online logged in as {bot.user}')
    return await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='Dofus'))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        await bot.process_commands(message)
        return
    
    lookingFor = ['d-bk.net', 'dofusbook.net', 'dofusroom.com']
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
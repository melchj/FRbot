import os
import json
import asyncio
import sys
import traceback
import discord
from discord.ext import commands, tasks
import sqlite3
import random
from datetime import datetime

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
    # ignore message if it comes from this bot
    if message.author.id == bot.user.id:
        return
    
    # reply if someone mentioned dofusbook instead of dofuslab
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
    
    # save images attached to messages (https://discordpy.readthedocs.io/en/stable/api.html?highlight=message#discord.Attachment)
    # this is designed to be for saving all 5v5 screenshots, for later analysis
    # TODO: this should only be active in some channels
    extensions = ['.png', '.jpg', '.jpeg']
    for attachment in message.attachments:
        if attachment.filename.endswith(tuple(extensions)):
            # formatting the message send datetime to ISO 8601 for file name
            formattedDatetime = datetime.strftime(message.created_at, '%Y%m%dT%H%M%SZ')
            # print(formattedDatetime)
            # TODO: deal with potential exceptions from attachment.save (see docs)
            # TODO: save it in the right format (png/jpeg/jpg) (https://stackoverflow.com/questions/62375567/how-to-check-for-file-extension-in-discord-py)
            # TODO: maybe have different directories for each channel?
            await attachment.save(f'output/{formattedDatetime}.png', use_cached=True)

    # process all other commands
    await bot.process_commands(message)

if __name__ == '__main__':
    main()
import discord
from discord.ext import commands
import asyncio
import sqlite3
from datetime import datetime

from discord.ext.commands.errors import ExtensionNotLoaded

class Tingo(commands.Cog):
    '''Tingo'''

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    # @commands.command()
    # async def test(self, ctx, *args):
    #     await ctx.send(args)

    @commands.group(name='tingo', invoke_without_command=True)
    async def tingo(self, ctx, *args):
        print('tingo called without subcommand!!! do \".help tingo\" for subcommands')
        return
    
    @tingo.command()
    async def capture(self, ctx, *args):
        '''Gotta Catch \'em All! (use this command when u tingo someone. attach screenshot (.png) to message.)'''
        # print('tingooooo')

        # cancel if not exactly one attachment
        if (len(ctx.message.attachments) != 1):
            # TODO: bot response
            print('ERROR: .tingo capture needs exactly one image attached!')
            return

        # save attached image (if it's a png... error if not)
        # TODO: handle other image file types
        attachment = ctx.message.attachments[0]
        formattedDatetime = datetime.strftime(ctx.message.created_at, '%Y%m%dT%H%M%SZ')
        imgPath = f"tingo/{formattedDatetime}.png"
        if attachment.filename.endswith('.png'):
            await attachment.save(imgPath)
            print(f'attachment saved to {imgPath}')
        else:
            # TODO: bot response
            print('Chonk is lazy, this currently only works if attachment is png file...')
            return
        
        # add to database
        db = sqlite3.connect('tingo.sqlite')
        cursor = db.cursor()

        # loop through all the "tingo victims" here
        for victim in args:
            victim = str(victim).title()
            # put entry in database for victim with image url
            cursor.execute(f"INSERT INTO tingodex (guild_id,channel_id,trainer_id,victim_name,image_path) VALUES({ctx.guild.id},{ctx.channel.id},{ctx.message.author.id},'{victim}','{imgPath}')")
        
        db.commit()
        db.close()
        await ctx.message.add_reaction(emoji='✅')
    
    @tingo.command()
    async def list(self, ctx, *args):
        # ".tingo list" -- send a list of all the different people (names) this person has captured
        # show the tingo pictures? only a certain number of pictures?
        # have a ".tingo list <name>" command to show all the pictures for that person?
        return

def setup(bot):
    bot.add_cog(Tingo(bot))
    print('Tingo is loaded')
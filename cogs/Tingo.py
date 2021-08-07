from sqlite3.dbapi2 import Cursor
import discord
from discord.ext import commands
import asyncio
import sqlite3
from datetime import datetime

from discord.ext.commands.errors import ExtensionNotLoaded

# TODO: ensure the help messages are useful and pop up at the right time(s)
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
            # TODO: do i actually need the channel id? It can be server wide instead of channel specific, i think
            cursor.execute(f"INSERT INTO tingodex (guild_id,channel_id,trainer_id,victim_name,image_path) VALUES({ctx.guild.id},{ctx.channel.id},{ctx.message.author.id},'{victim}','{imgPath}')")
        
        db.commit()
        db.close()
        await ctx.message.add_reaction(emoji='✅')
    
    @tingo.command()
    async def list(self, ctx, *args):
        # ".tingo list" -- send a list of all the different people (names) this person has captured
        db = sqlite3.connect('tingo.sqlite')
        cursor = db.cursor()

        # list all UNIQUE victims of this trainer on this discord server
        cursor.execute(f"SELECT DISTINCT victim_name from tingodex WHERE guild_id={ctx.guild.id} AND trainer_id={ctx.message.author.id}")
        result = cursor.fetchall()
        print(result)

        if not result:
            await ctx.send('No results! You haven\'t captured anything?')
        else:
            embed = discord.Embed(color=0xf5f2ca) # TODO: make a tingo-esque color
            victims = ''
            for value in result:
                victims = victims + str(value[0]) + '\n'
            embed.add_field(name=f'{ctx.message.author.display_name}\'s Tingo Victims', value=victims, inline=True)
            embed.set_author(name='Free Ring Tingos', icon_url=f'{ctx.guild.icon_url}')
            embed.set_footer(text='Do \".tingo show <victim>\" for more info!')
            embed.set_thumbnail(url=f'{ctx.guild.icon_url}') # TODO: make this a tingo icon?

            await ctx.send(embed=embed)
        # TODO: show the tingo pictures? only a certain number of pictures?
        # TODO: have a ".tingo list <name>" command to show all the pictures for that person?
        # or are the above just for 

    # TODO: add a ".tingo backup" command, just like .perc backup? tho what to do with images...?

def setup(bot):
    bot.add_cog(Tingo(bot))
    print('Tingo is loaded')
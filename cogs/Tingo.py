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
        await ctx.send('tingo called without subcommand!!! do \".help tingo\" for subcommands')
        return
    
    @tingo.command()
    async def capture(self, ctx, *args):
        '''Use this when you tingo someone! MUST attach a screenshot (.png)'''

        # cancel if not exactly one attachment
        if (len(ctx.message.attachments) != 1):
            await ctx.send('ERROR: .tingo capture needs exactly one image attached!')
            return

        # save attached image
        attachment = ctx.message.attachments[0]
        formattedDatetime = datetime.strftime(ctx.message.created_at, '%Y%m%dT%H%M%SZ')
        extension = attachment.filename.split('.')[-1]
        imgPath = f"tingo/{formattedDatetime}.{extension}"
        await attachment.save(imgPath)
        
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
        '''See a list of all the people you've tingo\'d! Also try ".tingo list <name>" to see who other people have tingo\'d!'''
        # ".tingo list" -- send a list of all the different people (names) this person has captured
        db = sqlite3.connect('tingo.sqlite')
        cursor = db.cursor()

        # if (len(args) == 0):
        if (len(ctx.message.mentions) == 0):
            # list all UNIQUE victims of this trainer on this discord server
            cursor.execute(f"SELECT DISTINCT victim_name from tingodex WHERE guild_id={ctx.guild.id} AND trainer_id={ctx.message.author.id}")
            result = cursor.fetchall()
            print(result)

            if not result:
                await ctx.send('No results! You haven\'t captured anything?')
            else:
                embed = discord.Embed(color=0xec942a)
                victims = ''
                for value in result:
                    victims = victims + str(value[0]) + '\n'
                embed.add_field(name='Tingo Victims', value=victims, inline=True)
                embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                embed.set_footer(text='Try \".tingo show\"!')
                thumbnailFile = discord.File("res/larval.png", filename="larval.png") # TODO: tbh there's probably a better way to attach a local file to embed object? idk
                embed.set_thumbnail(url="attachment://larval.png")

                await ctx.send(embed=embed, file=thumbnailFile)
        else:
            # list the vitctims of the mentioned trainers
            for member in ctx.message.mentions:
                # await ctx.send(f'you mentioned {member}')
                cursor.execute(f"SELECT DISTINCT victim_name from tingodex WHERE guild_id={ctx.guild.id} AND trainer_id={member.id}")
                result = cursor.fetchall()
                print(result)

                if not result:
                    await ctx.send(f'No results! {member} hasen\'t captured anything?!')
                else:
                    embed = discord.Embed(color=0xec942a)
                    victims = ''
                    for value in result:
                        victims = victims + str(value[0]) + '\n'
                        print(value)
                    embed.add_field(name='Tingo Victims', value=victims, inline=True)
                    embed.set_author(name=member.name, icon_url=member.avatar_url)
                    embed.set_footer(text='Try \".tingo show\"!')
                    thumbnailFile = discord.File("res/larval.png", filename="larval.png") # TODO: tbh there's probably a better way to attach a local file to embed object? idk
                    embed.set_thumbnail(url="attachment://larval.png")

                    await ctx.send(embed=embed, file=thumbnailFile)

    @tingo.command()
    async def show(self, ctx, *args):
        """See the tingo screenshots!!"""
        db = sqlite3.connect('tingo.sqlite')
        cursor = db.cursor()

        maxImages = 10 # max number of pictures to send... TODO: probably a better way to limit this

        if (len(args) == 0):
            # no arguments, show all recent captures for all tingo victims
            await ctx.send('Here are your most recent tingos!')
            cursor.execute(f"SELECT DISTINCT victim_name, image_path from tingodex WHERE guild_id={ctx.guild.id} AND trainer_id={ctx.message.author.id}")
            result = cursor.fetchall()

            print(result)
            i = 0
            # TODO: the "most recent" order kind of depends on how the database is ordered... perhaps the database should store the date captured (currently date is stored in file name of images)
            for capture in reversed(result):
                i = i + 1
                if i > maxImages:
                    continue
                victim = str(capture[0])
                imagePath = str(capture[1])
                fileName = imagePath.split('/')[1]
                # TODO: format that date better... (below)
                embed = discord.Embed(color=0xec942a, title=f"Tingo'd {victim} on {fileName[0:4]} {fileName[4:6]} {fileName[6:8]}")
                screenshotFile = discord.File(imagePath)
                embed.set_image(url=f"attachment://{screenshotFile.filename}")
                embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                thumbnailFile = discord.File("res/larval.png", filename="larval.png") # TODO: tbh there's probably a better way to attach a local file to embed object? idk
                embed.set_thumbnail(url="attachment://larval.png")

                await ctx.send(files=(screenshotFile, thumbnailFile), embed=embed)

        else:
            # show all capture screenshots for the victim(s) named
            picsSent = 0
            for victim in args:
                victim = str(victim).title()
                cursor.execute(f"SELECT victim_name, image_path from tingodex WHERE guild_id={ctx.guild.id} AND trainer_id={ctx.message.author.id} AND victim_name='{victim}'")
                result = cursor.fetchall()

                # no results for this victim name, skip to next
                if len(result) == 0:
                    print('no results found')
                    await ctx.send('ERROR: no results found?')
                    break

                print(result)
                # victimName = result[0][0]
                plurality = ''
                if len(result) > 1:
                    plurality = 's'
                await ctx.send(f"You have tingo'd {victim} {len(result)} time{plurality}!")

                # loop through each capture event and send a the picture
                for capture in result:
                    if (picsSent > maxImages):
                        print('trying to send too many pics!!!')
                        break
                    imagePath = capture[1]
                    fileName = imagePath.split('/')[1]
                    # TODO: format that date better... (below)
                    embed = discord.Embed(color=0xec942a, title=f"Tingo'd {victim} on {fileName[0:4]} {fileName[4:6]} {fileName[6:8]}")
                    screenshotFile = discord.File(imagePath)
                    embed.set_image(url=f"attachment://{screenshotFile.filename}")
                    embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                    thumbnailFile = discord.File("res/larval.png", filename="larval.png") # TODO: tbh there's probably a better way to attach a local file to embed object? idk
                    embed.set_thumbnail(url="attachment://larval.png")

                    await ctx.send(files=(screenshotFile, thumbnailFile), embed=embed)
                    picsSent = picsSent + 1

    # TODO: add a ".tingo backup" command, just like .perc backup? tho what to do with images...? idk

def setup(bot):
    bot.add_cog(Tingo(bot))
    print('Tingo is loaded')
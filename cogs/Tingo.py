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

        # save attached image (if it's a png... error if not)
        # TODO: handle other image file types
        attachment = ctx.message.attachments[0]
        formattedDatetime = datetime.strftime(ctx.message.created_at, '%Y%m%dT%H%M%SZ')
        imgPath = f"tingo/{formattedDatetime}.png"
        if attachment.filename.endswith('.png'):
            await attachment.save(imgPath)
            print(f'attachment saved to {imgPath}')
        else:
            await ctx.send('ERROR: Chonk is lazy, this currently only works if the attached screenshot is a png file...')
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
    
    # TODO: this command should probably be modified so bot doesn't get rate limited if someone has too many tingos to list (https://discord.com/developers/docs/topics/rate-limits)
    @tingo.command()
    async def list(self, ctx, *args):
        '''See a list of all the people you've tingo\'d! Also try ".tingo list all" and ".tingo list <name>"'''
        # ".tingo list" -- send a list of all the different people (names) this person has captured
        db = sqlite3.connect('tingo.sqlite')
        cursor = db.cursor()

        if (len(args) == 0):
            # list all UNIQUE victims of this trainer on this discord server
            cursor.execute(f"SELECT DISTINCT victim_name from tingodex WHERE guild_id={ctx.guild.id} AND trainer_id={ctx.message.author.id}")
            result = cursor.fetchall()
            print(result)

            if not result:
                await ctx.send('No results! You haven\'t captured anything?')
            else:
                embed = discord.Embed(color=0xec942a) # TODO: make this a tingo-esque color
                victims = ''
                for value in result:
                    victims = victims + str(value[0]) + '\n'
                embed.add_field(name='Tingo Victims', value=victims, inline=True)
                embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                embed.set_footer(text='Do \".tingo list all\" or \".tingo list <name>\"for more!')
                thumbnailFile = discord.File("res/larval.png", filename="larval.png") # TODO: tbh there's probably a better way to attach a local file to embed object? idk
                embed.set_thumbnail(url="attachment://larval.png")

                await ctx.send(embed=embed, file=thumbnailFile)
        elif (args[0].lower() == 'all'):
            # show all capture screenshots for all victims (max 10? for now)
            await ctx.send('Here are your most recent tingos!')
            cursor.execute(f"SELECT DISTINCT victim_name, image_path from tingodex WHERE guild_id={ctx.guild.id} AND trainer_id={ctx.message.author.id}")
            result = cursor.fetchall()

            print(result)
            max = 10
            i = 0
            for capture in reversed(result):
                i = i + 1
                if i > max:
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

    # TODO: add a ".tingo backup" command, just like .perc backup? tho what to do with images...? idk

def setup(bot):
    bot.add_cog(Tingo(bot))
    print('Tingo is loaded')
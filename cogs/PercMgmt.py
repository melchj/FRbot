import discord
from discord.ext import commands
import asyncio
import sqlite3

def addToPlayers(guildID, channelID, value, *players):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    for player in players:
        player = str(player).title()
        cursor.execute(f"SELECT count from wordcount WHERE guild_id={guildID} AND channel_id={channelID} AND msg='{player}'")
        result = cursor.fetchone()
        if result is None:
            if (value < 1):
                continue
            cursor.execute(f"INSERT INTO wordcount (guild_id,channel_id,msg,count) VALUES({guildID},{channelID},'{player}','{value}')")
        else:
            newval = result[0] + value
            cursor.execute(f"UPDATE wordcount SET count={newval} WHERE guild_id={guildID} AND channel_id={channelID} AND msg='{player}'")
    db.commit()
    db.close()
    return

class PercMgmt(commands.Cog):
    """Perc Management"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

        # Commands
    @commands.group(name='perc', invoke_without_command=True)
    async def perc(self, ctx):
        """Do \".help perc\" for list of sub commands"""
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name='Perc Management', value='.perc help - for a list of Subcommands', inline=False)
        await ctx.send(embed=embed)

    # @perc.command()
    # async def help(self, ctx):
    #     """list of Sub Commands"""

    #     commands = self.bot.get_cog('PercMgt').get_commands()
        
    #     print([c.name for c in commands])
    #     print([c.qualified_name for c in self.bot.get_cog('PercMgt').walk_commands()])

    #     for c in self.bot.get_cog('PercMgt').get_commands():
    #         print(f'{c}')
    #         await ctx.send("bruh idk check the pinned messages maybe help is in there")


    @perc.command()
    async def add(self, ctx, *args):
        '''Adds 1 point.'''
        addToPlayers(ctx.guild.id, ctx.channel.id, 1, *args)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def win(self, ctx, *args):
        '''Adds 2 points. For perc def/attack 5v5 wins.'''
        addToPlayers(ctx.guild.id, ctx.channel.id, 2, *args)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def nodef(self, ctx, *args):
        '''Adds 1 point. For def/attack 5vX wins.'''
        addToPlayers(ctx.guild.id, ctx.channel.id, 1, *args)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def loss(self, ctx, *args):
        '''Adds 1 point. For def/attack 5v5 losses.'''
        addToPlayers(ctx.guild.id, ctx.channel.id, 1, *args)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def minus(self, ctx, *args):
        '''Subtracts 1 point.'''
        addToPlayers(ctx.guild.id, ctx.channel.id, -1, *args)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def list(self, ctx):
        '''Lists the current leaderboard for the channel.'''
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT msg, count from wordcount WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} ORDER BY count DESC")
        result = cursor.fetchall()
        print(result)
        if not result:
            await ctx.send('There is no Data for this channel')
        else:
            embed = discord.Embed(color=0xf5f2ca)
            player = ''
            count = ''
            for value in result:
                player = player + str(value[0]) + '\n'
                count = count + str(value[1]) + '\n'
            embed.add_field(name='Player', value=player, inline=True)
            embed.add_field(name='Count', value=count, inline=True)
            embed.set_author(name='Free Ring Tings', icon_url=f'{ctx.guild.icon_url}')
            embed.set_footer(text='#FOKSYM')
            embed.set_thumbnail(url=f'{ctx.guild.icon_url}')

            await ctx.send(embed=embed)

    @perc.command()
    async def backup(self, ctx):
        '''dev command (mod only)'''
        if ctx.message.author.guild_permissions.manage_messages:
            await ctx.message.author.send(file=discord.File('main.sqlite'))
            await ctx.message.add_reaction(emoji='✅')
        else:
            await ctx.message.add_reaction(emoji='‼')

    @perc.command()
    async def reset(self,ctx):
        '''Resets the leaderboard for this channel. (mod only)'''
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"DELETE from wordcount WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id}")
            db.commit()
            db.close()
            await ctx.send("Ah.. Yes Delete the proof of the 20% Winrate.")
            await ctx.message.add_reaction(emoji='✅')
        else:
            await ctx.send("What are you a SYM spy?!")
            await ctx.message.add_reaction(emoji='‼')

    @perc.command()
    async def edit(self, ctx, typoname, fixedname):
        '''Fix a mispelled name. \".perc edit <typoName> <correctedName>\"'''
        embed = discord.Embed(color=0xf5f2ca)
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            typo = str(typoname).title()
            fix = str(fixedname).title()
            cursor.execute(f"SELECT count from wordcount WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND msg='{typo}'")
            result = cursor.fetchone()
            if not result:
                embed.add_field(name="Error", value='Name not found in list. .perc edit <TypoName> <FixedName>')
                await ctx.send(embed=embed)
            else:
                countvalue = result[0]
                cursor.execute(f"SELECT count from wordcount WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND msg='{fix}'")
                result = cursor.fetchone()
                if not result:
                    cursor.execute(f"INSERT INTO wordcount (guild_id,channel_id,msg,count) VALUES({ctx.guild.id},{ctx.channel.id},'{fix}',{countvalue})")
                else:
                    value = result[0] + countvalue
                    cursor.execute(
                        f"UPDATE wordcount SET count={value} WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND msg='{fix}'")
                cursor.execute(f"DELETE from wordcount WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND msg='{typo}'")
            db.commit()
            db.close()
            await ctx.message.add_reaction(emoji='✅')
        else:
            embed.add_field(name="You cannot do that", value='Ping Louk or some shit')
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(PercMgmt(bot))
    print('perc is loaded')
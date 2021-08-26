import discord
from discord import channel
from discord.ext import commands
import asyncio
import sqlite3

def addToPlayers(guildID, channelID, category:str, value:int, *players):
    """
    Adds {value} to the database for all {players} for the given {category}.
    {category} must be one of: 'win', 'loss', 'nocontest'.
    """
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    # ensure the category given is valid
    categories = ['win', 'loss', 'nocontest']
    category = category.lower()
    if category not in categories:
        print(f'ERROR: in addToPlayers, can\'t use category: {category}')
        return

    for player in players:
        player = str(player).title()
        cursor.execute(f"SELECT {category} from percscore WHERE guild_id={guildID} AND channel_id={channelID} AND player='{player}'")
        result = cursor.fetchone()

        # if nothing is found in database, it must be because this player name hasn't been added... so insert it with 0s 
        if result is None:
            cursor.execute(f"INSERT INTO percscore (guild_id,channel_id,player,win,loss,nocontest) VALUES({guildID},{channelID},'{player}',0,0,0)")
            newValue = value

        # if something is found, calculate the new value to update to
        else:
            newValue = result[0] + value
        # dont let the database get a negative
        # if newValue < 0:
            # newValue = 0

        # update the value in the database
        cursor.execute(f"UPDATE percscore SET {category}={newValue} WHERE guild_id={guildID} AND channel_id={channelID} AND player='{player}'")
    db.commit()
    db.close()
    return

class PercMgmt(commands.Cog):
    """Perc Management"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    # Commands
    @commands.group(name='perc', invoke_without_command=True, case_insensitive=True)
    async def perc(self, ctx):
        """Do \".help perc\" for list of sub commands"""
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name='Perc Management', value='.help perc - for a list of Subcommands', inline=False)
        await ctx.send(embed=embed)

    @perc.command()
    async def win(self, ctx, *args):
        '''For perc def/attack 5v5 wins. Worth the most points.'''
        addToPlayers(ctx.guild.id, ctx.channel.id, 'win', 1, *args)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def loss(self, ctx, *args):
        '''For def/attack 5v5 losses. Worth slightly less points than win.'''
        addToPlayers(ctx.guild.id, ctx.channel.id, 'loss', 1, *args)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def noContest(self, ctx, *args):
        '''For def/attacks with 5vX wins.'''
        addToPlayers(ctx.guild.id, ctx.channel.id, 'nocontest', 1, *args)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def removeWin(self, ctx, *args):
        '''To remove a 5v5 win.'''
        addToPlayers(ctx.guild.id, ctx.channel.id, 'win', -1, *args)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def removeLoss(self, ctx, *args):
        '''To remove a 5v5 loss.'''
        addToPlayers(ctx.guild.id, ctx.channel.id, 'loss', -1, *args)
        await ctx.message.add_reaction(emoji='✅')
    
    @perc.command()
    async def removeNoContest(self, ctx, *args):
        '''To remove a 5vX win.'''
        addToPlayers(ctx.guild.id, ctx.channel.id, 'nocontest', -1, *args)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def list(self, ctx):
        '''Lists the current leaderboard for the channel.'''
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        # get everything from the database
        cursor.execute(f"SELECT player, win, loss, nocontest from percscore WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} ORDER BY win DESC")
        result = cursor.fetchall()
        if not result:
            await ctx.send('There is no Data for this channel')
        else:
            embed = discord.Embed(color=0xf5f2ca)
            # loop through everything returned from DB and calculate score per player
            entries = dict()
            for value in result:
                entries[value[0]] = value[1]*2 + value[2]*1 + value[3]*0.5
            
            # loop through the entries IN DESCENDING ORDER BY SCORE and make the strings to send
            players = ''
            scores = ''
            for key in sorted(entries, key=entries.get, reverse=True):
                players = players + key + '\n'
                scores = scores + f'{(entries[key]):g}\n'
            embed.add_field(name='Player', value=players, inline=True)
            embed.add_field(name='Score', value=scores, inline=True)
            embed.set_author(name='Free Ring Tings', icon_url=f'{ctx.guild.icon_url}')
            embed.set_footer(text='#FOKBLITY')
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
            cursor.execute(f"DELETE from percscore WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id}")
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

            cursor.execute(f"SELECT win, loss, nocontest from percscore WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND player='{typo}'")
            result = cursor.fetchone()

            if not result:
                embed.add_field(name="Error", value='Name not found in list. .perc edit <TypoName> <FixedName>')
                await ctx.send(embed=embed)
            else:
                winValue = result[0]
                lossValue = result[1]
                nocontestValue = result[2]

                # no get data for the correct spelling name
                cursor.execute(f"SELECT win, loss, nocontest from percscore WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND player='{fix}'")
                result = cursor.fetchone()

                # if the correctly spelled name doesn't exist, we insert it into the db
                if not result:
                    cursor.execute(f"INSERT INTO percscore (guild_id,channel_id,player,win,loss,nocontest) VALUES({ctx.guild.id},{ctx.channel.id},'{fix}',{winValue},{lossValue},{nocontestValue})")
                
                # if the correctly spelled name DOES exist, need to add the values from the typo name and update correctly spelled entry
                else:
                    winValue = winValue + result[0]
                    lossValue = lossValue + result[1]
                    nocontestValue = nocontestValue + result[2]
                    # TODO: the three execute commands could probably be just one? but i dont know enough SQL so rip...
                    cursor.execute(f"UPDATE percscore SET win={winValue} WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND player='{fix}'")
                    cursor.execute(f"UPDATE percscore SET loss={lossValue} WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND player='{fix}'")
                    cursor.execute(f"UPDATE percscore SET nocontest={nocontestValue} WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND player='{fix}'")
                cursor.execute(f"DELETE from percscore WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND player='{typo}'")
            db.commit()
            db.close()
            await ctx.message.add_reaction(emoji='✅')
        else:
            embed.add_field(name="You cannot do that", value='Ping Louk or some shit')
            await ctx.send(embed=embed)

    @perc.command(hidden=True)
    async def wrlist(self, ctx, mentionedChannel:discord.TextChannel=None):
        '''lists the full scores'''
        if ctx.message.author.guild_permissions.manage_messages:
            # return if no channel mentioned
            if mentionedChannel is None:
                await ctx.send("you need to tag a channel to look at. \".perc wrlist <#text-channel>\"")
                return

            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            # get everything from the database
            cursor.execute(f"SELECT player, win, loss, nocontest from percscore WHERE guild_id={ctx.guild.id} AND channel_id={mentionedChannel.id} ORDER BY win DESC")
            result = cursor.fetchall()
            if not result:
                await ctx.send('There is no Data for this channel')
            else:
                
                # loop through everything returned from DB and organize it all into a dict
                resultDict = dict()
                for value in result:
                    # skip this one if no wins + losses
                    if (value[1] + value[2]) == 0:
                        continue
                    # parse from value object to build dict
                    name = value[0]
                    wins = value[1]
                    losses = value[2]
                    wr = value[1] / (value[1] + value[2])
                    # build dict
                    resultDict[name] = (wins, losses, wr)

                # loop through dict and build the strings to send
                players = ''
                winloss = ''
                winrates = ''
                # sort descending by one of the items in the tuple
                for item in sorted(resultDict.items(), key = lambda x: x[1][0], reverse=True):
                    data = item[1]
                    players = players + item[0] + '\n'
                    winloss = winloss + f'{data[0]}-{data[1]}\n'
                    winrates = winrates + f'{data[2]:.2f}' + '\n'

                embed = discord.Embed(color=0xf5f2ca)
                embed.add_field(name='Player', value=players, inline=True)
                embed.add_field(name='W-L', value=winloss, inline=True)
                embed.add_field(name='WR%', value=winrates, inline=True)
                embed.set_author(name='Free Ring Tings', icon_url=f'{ctx.guild.icon_url}')
                embed.set_footer(text='\"No Contests (5vx)\" are ignored in winrate calculation')
                embed.set_thumbnail(url=f'{ctx.guild.icon_url}')

                await ctx.send(embed=embed)
        else:
            # if non-authorized member calls this, return as if it was incorrect subcommand
            await self.perc(ctx)

def setup(bot):
    bot.add_cog(PercMgmt(bot))
    print('perc is loaded')
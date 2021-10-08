import sqlite3
import discord
from discord.ext import commands


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
        print(f'ERROR: in prism addToPlayers, can\'t use category: {category}')
        return

    for player in players:
        player = str(player).title()
        cursor.execute(f"SELECT {category} from prismscore WHERE guild_id={guildID} AND channel_id={channelID} AND player='{player}'")
        result = cursor.fetchone()

        # if nothing is found in database, it must be because this player name hasn't been added... so insert it with 0s 
        if result is None:
            cursor.execute(f"INSERT INTO prismscore (guild_id,channel_id,player,win,loss,nocontest) VALUES({guildID},{channelID},'{player}',0,0,0)")
            newValue = value

        # if something is found, calculate the new value to update to
        else:
            newValue = result[0] + value
        # dont let the database get a negative
        # if newValue < 0:
            # newValue = 0

        # update the value in the database
        cursor.execute(f"UPDATE prismscore SET {category}={newValue} WHERE guild_id={guildID} AND channel_id={channelID} AND player='{player}'")
    db.commit()
    db.close()
    return

class PrismMgmt(commands.Cog):
    """Prism Management"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    # Commands
    @commands.group(name='prism', invoke_without_command=True, case_insensitive=True)
    async def prism(self, ctx):
        """Do \".help prism\" for list of sub commands"""
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name='Prism Management', value='.help prism - for a list of Subcommands', inline=False)
        await ctx.send(embed=embed)

    @prism.command()
    async def win(self, ctx, *args):
        '''For Prism wins.'''
        addToPlayers(ctx.guild.id, ctx.channel.id, 'win', 1, *args)
        await ctx.message.add_reaction(emoji='✅')
    
    @prism.command()
    async def removeWin(self, ctx, *args):
        '''To remove a prism win.'''
        addToPlayers(ctx.guild.id, ctx.channel.id, 'win', -1, *args)
        await ctx.message.add_reaction(emoji='✅')
    
    @prism.command()
    async def edit(self, ctx, typoname, fixedname):
        '''Fix a mispelled name. \".prism edit <typoName> <correctedName>\"'''
        embed = discord.Embed(color=0xf5f2ca)
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            typo = str(typoname).title()
            fix = str(fixedname).title()

            cursor.execute(f"SELECT win, loss, nocontest from prismscore WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND player='{typo}'")
            result = cursor.fetchone()

            if not result:
                embed.add_field(name="Error", value='Name not found in list. .prism edit <TypoName> <FixedName>')
                await ctx.send(embed=embed)
            else:
                winValue = result[0]
                lossValue = result[1]
                nocontestValue = result[2]

                # no get data for the correct spelling name
                cursor.execute(f"SELECT win, loss, nocontest from prismscore WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND player='{fix}'")
                result = cursor.fetchone()

                # if the correctly spelled name doesn't exist, we insert it into the db
                if not result:
                    cursor.execute(f"INSERT INTO prismscore (guild_id,channel_id,player,win,loss,nocontest) VALUES({ctx.guild.id},{ctx.channel.id},'{fix}',{winValue},{lossValue},{nocontestValue})")
                
                # if the correctly spelled name DOES exist, need to add the values from the typo name and update correctly spelled entry
                else:
                    winValue = winValue + result[0]
                    lossValue = lossValue + result[1]
                    nocontestValue = nocontestValue + result[2]
                    # TODO: the three execute commands could probably be just one? but i dont know enough SQL so rip...
                    cursor.execute(f"UPDATE prismscore SET win={winValue} WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND player='{fix}'")
                    cursor.execute(f"UPDATE prismscore SET loss={lossValue} WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND player='{fix}'")
                    cursor.execute(f"UPDATE prismscore SET nocontest={nocontestValue} WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND player='{fix}'")
                cursor.execute(f"DELETE from prismscore WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND player='{typo}'")
            db.commit()
            db.close()
            await ctx.message.add_reaction(emoji='✅')
        else:
            embed.add_field(name="You cannot do that", value='Ping Louk or some shit')
            await ctx.send(embed=embed)
    
    @prism.command()
    async def reset(self,ctx):
        '''Resets the leaderboard for this channel. (mod only)'''
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"DELETE from prismscore WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id}")
            db.commit()
            db.close()
            await ctx.send("Ah.. Yes Delete the proof of the 20% Winrate.")
            await ctx.message.add_reaction(emoji='✅')
        else:
            await ctx.send("What are you a SYM spy?!")
            await ctx.message.add_reaction(emoji='‼')
    
    @prism.command()
    async def list(self, ctx):
        '''Lists the current prism leaderboard for the channel.'''
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        # get everything from the database
        cursor.execute(f"SELECT player, win, loss, nocontest from prismscore WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} ORDER BY win DESC")
        result = cursor.fetchall()
        if not result:
            await ctx.send('There is no data for this channel')
        else:
            embed = discord.Embed(color=0xf5f2ca)
            # parse results from db query
            playersStr = ''
            winsStr = ''
            for row in result:
                playersStr = playersStr + row[0] + '\n'
                winsStr = winsStr + f"{row[1]}\n"

            # make the embed object to send
            embed.add_field(name='Player', value=playersStr, inline=True)
            embed.add_field(name='Prism Wins', value=winsStr, inline=True)
            embed.set_author(name='Free Ring Tings', icon_url=f'{ctx.guild.icon_url}')
            embed.set_footer(text='#FOKBLITY')
            embed.set_thumbnail(url=f'{ctx.guild.icon_url}')

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(PrismMgmt(bot))
    print('prism is loaded')
import discord
from discord.ext import commands
import asyncio

class Core(commands.Cog):

    """Basic Functions"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

        # Commands

    # Basic Ping Command
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def Jeff(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Jeff", value='...is dumb')
        await ctx.send(embed=embed)

    @commands.command()
    async def Blity(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Blity", value='...fuck blity')
        await ctx.send(embed=embed)

    @commands.command()
    async def krea(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Krea", value='...is a commie')
        await ctx.send(embed=embed)


    # Simple Clear Tool need to expand and add permissions to this.
    #@commands.command()
    #async def clear(self, ctx, amount=10):
        #if ctx.message.author.guild_permissions.manage_messages:
            #await ctx.channel.purge(limit=amount)
        #else:
            #await ctx.send("No can do bruh.")
def setup(bot):
    bot.add_cog(Core(bot))
    print('Core is loaded')

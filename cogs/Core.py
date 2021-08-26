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
        '''Pong!'''
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command(hidden=True)
    async def Jeff(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Jeff", value='...is dumb')
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def Blity(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Blity", value='...fuck blity')
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def krea(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Krea", value='...is a commie')
        await ctx.send(embed=embed)
    
    @commands.command(hidden=True)
    async def doublespeak(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Double", value='miss u bb <3')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Core(bot))
    print('Core is loaded')

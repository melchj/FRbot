import discord
from discord.ext import commands
import asyncio

class Core(commands.Cog):

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
    # Simple Welcome Plans to expand for Twitch server

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(785963981008797709)
        await channel.send(f'Welcome to the server{member.mention}')

def setup(bot):
    bot.add_cog(Core(bot))
    print('Welcome is loaded')
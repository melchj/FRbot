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

    # TODO: is there a way to have these "hidden" generic character commands be just a couple lists or something?
    # instead of copy/pasts with the command name and return text changed?
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

    @commands.command(hidden=True)
    async def duke(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Duke", value='..what a bandeur de meuf')
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def lucent(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Lucent", value='Bugün yüzlerce film, dizi ve belgeseli izlemeye başlayın')
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def loukani(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Loukani", value="Shai you're drolllinnnng")
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def vyxyn(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Vyxyn", value='... ok r****d')
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def world(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="World", value='.. died with 1 AP')
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def undine(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Undine", value="don't insult leadership please")
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def jeffers(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Jeffers", value='...is still in jail after insulting a policeman')
        await ctx.send(embed=embed)

    # TODO: make this one choose a random copypasta from a set of them
    @commands.command(hidden=True)
    async def alaxel(self, ctx):
        async def sendEmbed(string):
            embed = discord.Embed(color=0xf5f2ca)
            embed.add_field(name="Alaxel", value=string)
            await ctx.send(embed=embed)
        
        string1 = "RAID: Shadow Legends™️ is an immersive online experience with everything you'd expect from a brand new RPG title. It's got an amazing storyline, awesome 3D graphics, giant boss fights, PVP battles, and hundreds of never before seen champions to collect and customize."
        string2 = "I never expected to get this level of performance out of a mobile game. Look how crazy the level of detail is on these champions!"
        string3 = "RAID: Shadow Legends™️ is getting big real fast, so you should definitely get in early. Starting now will give you a huge head start. There's also an upcoming Special Launch Tournament with crazy prizes! And not to mention, this game is absolutely free!"
        string4 = "So go ahead and check out the video description to find out more about RAID: Shadow Legends™️. There, you will find a link to the store page and a special code to unlock all sorts of goodies. Using the special code, you can get 50,000 Silver immediately, and a FREE Epic Level Champion as part of the new players program, courtesy of course of the RAID: Shadow Legends™️ devs."

        await sendEmbed(string1)
        await sendEmbed(string2)
        await sendEmbed(string3)
        await sendEmbed(string4)

    @commands.command(hidden=True)
    async def biscroco(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Biscroco", value='..sorry my computer was laggy')
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def ayman(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Ayman", value='pee pee poo poo')
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def monka(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Monka", value='let me tell you something')
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def rakul(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Rakul", value='sorry i was in the kitchen')
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def jash(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Jash", value="bro i've had a bag of Doritos and a kinder bueno in the last month")
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def basi(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Basi", value='is afk in a mountain with monks, to learn 5v5')
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def osmo(self, ctx):
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name="Osmo", value='the perc theif')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Core(bot))
    print('Core is loaded')

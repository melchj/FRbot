import discord
from discord.ext import commands
import asyncio

class Help(commands.Cog):

    """Help Controls"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if hasattr(ctx.command, 'on_error'):
                return
            else:
                embed = discord.Embed(title=f'Error in {ctx.command}',
                                      description=f'`{ctx.command.qualified_name} {ctx.command.signature}` \n{error}',
                                      color=0xf5f2ca)
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title=f'Error in {ctx.command}', description=f'{error}',color=0xf5f2ca)
            await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, *cog):
        """Get all Commands in Provided Cog"""

        if not cog:
            embed = discord.Embed(color=0xf5f2ca)
            cogs_desc = ''
            for x in self.bot.cogs:
                cogs_desc += ('**{}** - {}'.format(x, self.bot.cogs[x].__doc__)+'\n')
            embed.add_field(name='Modules',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
            await ctx.send(embed=embed)
        else:
            if len(cog) > 1:
                embed = discord.Embed(title='Error!', description='One at a time', color=0xf5f2ca)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=0xf5f2ca)
                found = False
                for x in self.bot.cogs:
                    for y in cog:
                        if x == y:
                            embed = discord.Embed(color=0xf5f2ca)
                            scog_info = ''
                            for c in self.bot.get_cog(y).get_commands():
                                if not c.hidden:
                                    scog_info += f'**{c.name}** - {c.help}\n'
                            embed.add_field(name=f'{cog[0]} Module - {self.bot.cogs[cog[0]].__doc__}', value=scog_info)
                            found = True
                if not found:
                    for x in self.bot.cogs:
                        for c in self.bot.get_cog(x).get_commands():
                            if c.name == cog[0]:
                                embed = discord.Embed(color=0xf5f2ca)
                                embed.add_field(name=f'{c.name} - {c.help}', value=f'Proper Syntax: \n`{c.qualified_name} {c.signature}`')
                        found = True
                    if not found:
                        embed = discord.Embed(title='Error!', description='How do you even use "'+cog[0]+'"?',color=0xf5f2ca)
                await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Help(bot))
    print('Help is loaded')
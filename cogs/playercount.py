import discord
from discord.ext import commands
import asyncio
import sqlite3

class PercMgt(commands.Cog):

    """Perc Management"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

        # Commands
    @commands.group(name='perc', invoke_without_command=True)
    async def perc(self, ctx):
        """ .perc help for list of sub commands"""
        embed = discord.Embed(color=0xf5f2ca)
        embed.add_field(name='Perc Management', value='.perc help - for a list of Subcommands', inline=False)
        await ctx.send(embed=embed)

    @perc.command()
    async def help(self, ctx):
        """list of Sub Commands"""

        commands = self.bot.get_cog('PercMgt').get_commands()
        
        print([c.name for c in commands])
        print([c.qualified_name for c in self.bot.get_cog('PercMgt').walk_commands()])

        for c in self.bot.get_cog('PercMgt').get_commands():
            print(f'{c}')
            await ctx.send("bruh idk check the pinned messages maybe help is in there")


    @perc.command()
    async def add(self, ctx, *args):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        for arg in args:
            player = str(arg).title()
            cursor.execute(f"SELECT count from wordcount WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND msg='{player}'")
            result = cursor.fetchone()
            if result is None:
                cursor.execute(f"INSERT INTO wordcount (guild_id,channel_id,msg,count) VALUES({ctx.guild.id},{ctx.channel.id},'{player}',1)")
            else:
                value = result[0] + 1
                cursor.execute(f"UPDATE wordcount SET count={value} WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND msg='{player}'")
        db.commit()
        db.close()
        checkmark = self.bot.get_emoji(558322116685070378)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def win(self, ctx, *args):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        for arg in args:
            player = str(arg).title()
            cursor.execute(
                f"SELECT count from wordcount WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND msg='{player}'")
            result = cursor.fetchone()
            if result is None:
                cursor.execute(
                    f"INSERT INTO wordcount (guild_id,channel_id,msg,count) VALUES({ctx.guild.id},{ctx.channel.id},'{player}',2)")
            else:
                value = result[0] + 2
                cursor.execute(
                    f"UPDATE wordcount SET count={value} WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND msg='{player}'")
        db.commit()
        db.close()
        checkmark = self.bot.get_emoji(558322116685070378)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def nodef(self, ctx, *args):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        for arg in args:
            player = str(arg).title()
            cursor.execute(
                f"SELECT count from wordcount WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND msg='{player}'")
            result = cursor.fetchone()
            if result is None:
                cursor.execute(
                    f"INSERT INTO wordcount (guild_id,channel_id,msg,count) VALUES({ctx.guild.id},{ctx.channel.id},'{player}',1)")
            else:
                value = result[0] + 1
                cursor.execute(
                    f"UPDATE wordcount SET count={value} WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND msg='{player}'")
        db.commit()
        db.close()
        checkmark = self.bot.get_emoji(558322116685070378)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def loss(self, ctx, *args):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        for arg in args:
            player = str(arg).title()
            cursor.execute(
                f"SELECT count from wordcount WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND msg='{player}'")
            result = cursor.fetchone()
            if result is None:
                cursor.execute(
                    f"INSERT INTO wordcount (guild_id,channel_id,msg,count) VALUES({ctx.guild.id},{ctx.channel.id},'{player}',1)")
            else:
                value = result[0] + 1
                cursor.execute(
                    f"UPDATE wordcount SET count={value} WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND msg='{player}'")
        db.commit()
        db.close()
        checkmark = self.bot.get_emoji(558322116685070378)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def minus(self, ctx, *args):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        for arg in args:
            player = str(arg).title()
            cursor.execute(
                f"SELECT count from wordcount WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND msg='{player}'")
            result = cursor.fetchone()
            if result is None:
                continue
            else:
                value = result[0] - 1
                cursor.execute(
                    f"UPDATE wordcount SET count={value} WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id} AND msg='{player}'")
        db.commit()
        db.close()
        checkmark = self.bot.get_emoji(558322116685070378)
        await ctx.message.add_reaction(emoji='✅')

    @perc.command()
    async def list(self, ctx):
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
    async def reset(self,ctx):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"DELETE from wordcount WHERE guild_id={ctx.guild.id} AND channel_id={ctx.channel.id}")
            db.commit()
            db.close()
            await ctx.send("Ah.. Yes Delete the proof of the 20% Winrate.")
        else:
            await ctx.send("What are you a SYM spy?!")

    @perc.command()
    async def edit(self, ctx, typoname, fixedname):
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
        else:
            embed.add_field(name="You cannot do that", value='Ping Louk or some shit')
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(PercMgt(bot))
    print('perc is loaded')
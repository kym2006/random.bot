import copy
import json
from classes import converters

import discord
from discord.ext import commands
from discord import app_commands
import typing
import config
from utils import checks


# TODO Make this premium + fix multiple response problem

class Snippet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    '''
    @checks.is_patron()
    @app_commands.command(
        name="snippetaddfile",
        description="Add a snippet. Each user is allowed to 10000 length in total. Limit increased if you are a patron.",
    )
    async def snippetaddfile(self, ctx, name:str):
        f=await ctx.message.attachments[0].read()
        f=f.decode('utf-8')
        content = f
        for snuse in ["snippetuse","run", "snuse", "use"]:
            if content.find(snuse) != -1:
                await ctx.response.send_message(embed=discord.Embed(description="Please do not try and cause a snippet-ception!", colour=self.bot.primary_colour))
                return 
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet WHERE userid=$1", ctx.user.id)

        snippets = dict()
        if res == []:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.user.id, json.dumps(snippets)
                )
                snippets=json.dumps(snippets)
        else:
            snippets = res[0]["content"]

        guild = self.bot.get_guild(725303414220914758)
        limit = 500000
        if ctx.user.id in [g.id for g in guild.members]:
            patron1 = discord.utils.find(lambda r: r.id == self.bot.config.patron1, guild.roles)
            patron2 = discord.utils.find(lambda r: r.id == self.bot.config.patron2, guild.roles)
            patron3 = discord.utils.find(lambda r: r.id == self.bot.config.patron3, guild.roles)
            member = guild.get_member(ctx.user.id)
            if patron1 in member.roles:
                limit += 100000
            if patron2 in member.roles:
                limit += 200000
            if patron3 in member.roles:
                limit += 1000000

        if len(snippets) + len(content) > limit:
            await ctx.response.send_message(f"Limit of {limit} exceeded.")
            return
        print(snippets)
        s = json.loads(snippets)
        s[name] = content
        async with self.bot.pool.acquire() as conn:
            await conn.execute("UPDATE snippet set content=$1 where userid=$2", json.dumps(s), ctx.user.id)
        await ctx.message.add_reaction("✅")
    '''
    '''

    @checks.is_patron()
    @app_commands.command(
        name="snippetadd",
        description="Add a snippet. Each user is allowed to 10000 length in total. Limit increased if you are a patron.",
    )
    async def snippet_add(self, ctx, name: str, *, content: str):
        for snuse in ["snippetuse"]:
            if content.find(snuse) != -1:
                await ctx.response.send_message(
                    embed=discord.Embed(description="Please do not try and cause a snippet-ception!",
                                        colour=self.bot.primary_colour))
                return
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet WHERE userid=$1", ctx.user.id)

        snippets = dict()
        if res == []:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.user.id, json.dumps(snippets)
                )
                snippets = json.dumps(snippets)
        else:
            snippets = res[0]["content"]

        guild = self.bot.get_guild(725303414220914758)
        limit = 0
        if ctx.user.id in [g.id for g in guild.members]:
            patron1 = discord.utils.find(lambda r: r.id == self.bot.config.patron1, guild.roles)
            patron2 = discord.utils.find(lambda r: r.id == self.bot.config.patron2, guild.roles)
            patron3 = discord.utils.find(lambda r: r.id == self.bot.config.patron3, guild.roles)
            member = guild.get_member(ctx.user.id)
            if patron1 in member.roles:
                limit += 10000
            if patron2 in member.roles:
                limit += 20000
            if patron3 in member.roles:
                limit += 100000

        if len(snippets) + len(content) > limit:
            await ctx.response.send_message(f"Limit of {limit} exceeded.")
            return
        print(snippets)
        s = json.loads(snippets)
        s[name] = content
        async with self.bot.pool.acquire() as conn:
            await conn.execute("UPDATE snippet set content=$1 where userid=$2", json.dumps(s), ctx.user.id)
        await ctx.message.add_reaction("✅")

    @app_commands.command(
        name="snippetuse",
        description="use a snippet",
    )
    async def snippet_use(self, ctx, times: typing.Optional[int], name: str, user: str):
        user = await converters.GlobalUser().convert(ctx, user)
        if times is None:
            times = 1
        if times > 10 and ctx.user.id not in self.bot.config.owners:
            await ctx.response.send_message(
                embed=discord.Embed(description="The limit for amount of times is 10.", colour=self.bot.primary_colour))
            return
        tar = user or ctx.user
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet where userid=$1", tar.id)
        snippets = dict()
        if res == []:
            async with self.bot.pool.acquire() as conn:
                await conn.execute("INSERT INTO snippet(userid,content) VALUES($1,$2)", tar.id, json.dumps(snippets))
        else:
            snippets = res[0]["content"]
        s = json.loads(snippets)
        if name not in s:
            await ctx.response.send_message(embed=discord.Embed(title="No note of that name found",
                                                                description="Are you sure you have the correct spelling/added the snippet?",
                                                                colour=self.bot.config.primary_colour))
            return
        msg = copy.copy(ctx.message)
        msg.channel = ctx.channel
        try:
            msg.author = ctx.channel.guild.get_member(tar.id) or tar
        except Exception:
            msg.author = tar
        msg.content = '/' + s[name]
        for i in range(times):
            new_ctx = await self.bot.get_context(msg, cls=type(ctx))
            await self.bot.invoke(copy.copy(new_ctx))

    @app_commands.command(
        name="snippetview",
        description="View a snippet",
    )
    async def snippetview(self, ctx, name: str):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet where userid=$1", ctx.user.id)
        snippets = dict()
        if res == []:

            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.user.id, json.dumps(snippets)
                )
        else:
            snippets = res[0]["content"]
        s = json.loads(snippets)
        if name in s:
            await ctx.response.send_message(
                embed=discord.Embed(title=f"Snippet name: {name}", description=f"{'/'}{s[name]}",
                                    colour=self.bot.config.primary_colour))
        else:
            await ctx.response.send_message(
                embed=discord.Embed(title="Error", description="No snippet of that name is found.",
                                    colour=self.bot.config.primary_colour))

    @app_commands.command(
        name="snippetremove",
        description="remove a snippet",
    )
    async def snippetremove(self, ctx, name: str):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet WHERE userid=$1", ctx.user.id)

        snippets = dict()
        if res == []:

            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.user.id, json.dumps(snippets)
                )
        else:
            snippets = res[0]["content"]
        s = json.loads(snippets)
        try:
            del s[name]
        except Exception:
            await ctx.response.send_message("You do not have a snippet named that!")
        async with self.bot.pool.acquire() as conn:
            await conn.execute("UPDATE snippet set content=$1 where userid=$2", json.dumps(s), ctx.user.id)
        await ctx.message.add_reaction("✅")

    @app_commands.command(
        name="snippetall",
        description="View all the names of your snippets",
    )
    async def snippetall(self, ctx):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet WHERE userid=$1", ctx.user.id)

        snippets = dict()
        if res == []:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.user.id, json.dumps(snippets)
                )
        else:
            snippets = res[0]["content"]
        s = json.loads(snippets)
        res = ""
        for i in s.keys():
            res += i + "\n"
        await ctx.response.send_message(
            embed=discord.Embed(title="All snippets", description=res, colour=self.bot.config.primary_colour))

    @app_commands.command(name="snippetabout", description="How to use snippets")
    async def snippetabout(self, ctx):
        embed = discord.Embed(
            title="How to use snippets in random.bot",
            description="Simple! Just store a snippet with snippetadd, then you can use that snippet with snippetuse! Check out other snippet related commands by flipping through the help menu.",
            colour=self.bot.primary_colour,
        )
        embed.add_field(
            name="Example",
            value="For example, after doing\n ``?snippetadd letter choose a b c d e f g h i j k l m n o p q r s t u v w x y z``\nI can call it by doing\n``?snippetuse letter``\nand it'll choose a random letter for me! ",
        )
        embed.add_field(
            name="Other commands",
            value="Do /help to see all commands.\nSnippet commands include\n``snippetadd``, ``snippetuse``, ``snippetview``, ``snippetall`` and ``snippetremove``. Do /help <command> to get more information.",
        )
        embed.add_field(
            name="Snippet",
            value="If you want a dedicated bot to store snippet, then **Snippet** may be the right bot for you! You can check it out via [this link](https://snippetsite.netlify.app/)",
        )

        await ctx.response.send_message(embed=embed)
    '''

async def setup(bot):
    await bot.add_cog(Snippet(bot))

import copy
import json

import discord
from discord.ext import commands
import typing 
import config
from classes import converters


class Snippet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="snippetadd",
        description="Add a snippet. Each user is allowed to 10000 length in total. Limit increased if you are a patron.",
        usage="snippetadd <name> <command to run without prefix>",
        aliases=["snippetnew", "addsnippet", "newsnippet", "snadd"]
    )
    async def snippetadd(self, ctx, name: str, *, content: str):
        for snuse in ["snippetuse","run", "snuse", "use"]:
            if content.find(snuse) != -1:
                await ctx.send(embed=discord.Embed(description="Please do not try and cause a snippet-ception!", colour=self.bot.primary_colour))
                return 
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet WHERE userid=$1", ctx.author.id)

        snippets = dict()
        if res == []:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.author.id, json.dumps(snippets)
                )
                snippets=json.dumps(snippets)
        else:
            snippets = res[0]["content"]

        guild = self.bot.get_guild(725303414220914758)
        limit = 50000
        if ctx.author.id in [g.id for g in guild.members]:
            patron1 = discord.utils.find(lambda r: r.id == self.bot.config.patron1, guild.roles)
            patron2 = discord.utils.find(lambda r: r.id == self.bot.config.patron2, guild.roles)
            patron3 = discord.utils.find(lambda r: r.id == self.bot.config.patron3, guild.roles)
            member = guild.get_member(ctx.author.id)
            if patron1 in member.roles:
                limit += 10000
            if patron2 in member.roles:
                limit += 20000
            if patron3 in member.roles:
                limit += 100000

        if len(snippets) + len(content) > limit:
            await ctx.send(f"Limit of {limit} exceeded.")
            return
        print(snippets)
        s = json.loads(snippets)
        s[name] = content
        async with self.bot.pool.acquire() as conn:
            await conn.execute("UPDATE snippet set content=$1 where userid=$2", json.dumps(s), ctx.author.id)
        await ctx.message.add_reaction("✅")

    @commands.command(
        name="snippetuse", 
        description="use a snippet", 
        usage="snippetuse [times] <name> [user] (user and times is optional)",
        aliases=["run", "snuse", "use"]
    )
    async def snippetuse(self, ctx,times: typing.Optional[int], name: str, user:converters.GlobalUser=None):
        if times is None:
            times = 1 
        if times > 10 and ctx.author.id not in self.bot.config.owners:
            await ctx.send(embed=discord.Embed(description="The limit for amount of times is 10.", colour=self.bot.primary_colour))
            return 
        tar = user or ctx.author
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
            await ctx.send(embed=discord.Embed(title="No note of that name found", description="Are you sure you have the correct spelling/added the snippet?", colour=self.bot.config.primary_colour))
            return 
        msg = copy.copy(ctx.message)
        msg.channel = ctx.channel
        try:
            msg.author = ctx.channel.guild.get_member(tar.id) or tar
        except Exception:
            msg.author = tar
        msg.content = ctx.prefix + s[name]
        for i in range(times):
            new_ctx = await self.bot.get_context(msg, cls=type(ctx))
            await self.bot.invoke(copy.copy(new_ctx))

    @commands.command(
        name="snippetview", 
        description="View a snippet", 
        usage="snippetview <name", 
        aliases=["view", "snview"])
    async def snippetview(self, ctx, name: str):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet where userid=$1", ctx.author.id)
        snippets = dict()
        if res == []:
            
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.author.id, json.dumps(snippets)
                )
        else:
            snippets = res[0]["content"]
        s = json.loads(snippets)
        if name in s:
            await ctx.send(embed=discord.Embed(title=f"Snippet name: {name}", description=f"{ctx.prefix}{s[name]}", colour=self.bot.config.primary_colour))
        else:
            await ctx.send(embed=discord.Embed(title="Error", description="No snippet of that name is found.", colour=self.bot.config.primary_colour))

    @commands.command(
        name="snippetremove", 
        description="remove a snippet", 
        aliases=["snippetdelete", "snremove", "sndelete"], 
        usage="snippetremove <name>"
    )
    async def snippetremove(self, ctx, name: str):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet WHERE userid=$1", ctx.author.id)

        snippets = dict()
        if res == []:
            
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.author.id, json.dumps(snippets)
                )
        else:
            snippets = res[0]["content"]
        s = json.loads(snippets)
        try:
            del s[name]
        except Exception:
            await ctx.send("You do not have a snippet named that!")
        async with self.bot.pool.acquire() as conn:
            await conn.execute("UPDATE snippet set content=$1 where userid=$2", json.dumps(s), ctx.author.id)
        await ctx.message.add_reaction("✅")

    @commands.command(
        name="snippetall", 
        description="View all the names of your snippets", 
        usage="snippetall", 
        aliases=["snall"])
    async def snippetall(self, ctx):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet WHERE userid=$1", ctx.author.id)

        snippets = dict()
        if res == []:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.author.id, json.dumps(snippets)
                )
        else:
            snippets = res[0]["content"]
        s = json.loads(snippets)
        res = ""
        for i in s.keys():
            res += i + "\n"
        await ctx.send(embed=discord.Embed(title="All snippets", description=res, colour=self.bot.config.primary_colour))

    @commands.command(name="snippetabout", description="How to use snippets", usage="snippetabout")
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
            value="Do ?help to see all commands.\nSnippet commands include\n``snippetadd``, ``snippetuse``, ``snippetview``, ``snippetall`` and ``snippetremove``. Do ?help <command> to get more information.",
        )
        embed.add_field(
            name="Snippet",
            value="If you want a dedicated bot to store snippet, then **Snippet** may be the right bot for you! You can check it out via [this link](https://snippetsite.netlify.app/)",
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Snippet(bot))

import json
import copy 
from discord.ext import commands
import discord 

class Snippet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="snippetadd", description="Add a snippet. Each user is allowed to 10000 length in total. Limit increased if you are a patron.", usage = "snippetadd")
    async def snippetadd(self, ctx, name: str, *, content: str):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet WHERE userid=$1", ctx.author.id)

        snippets = str()
        if res == []:
            snippets = " {} "
            async with self.bot.pool.acquire() as conn:
                await conn.execute("INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.author.id, json.dumps(snippets))
        else:
            snippets = res[0]["content"]
        if(len(snippets) + len(content) > 10000):
            await ctx.send("Limit of 10000 exceeded.")
            return 
        s = json.loads(snippets)
        s[name] = content
        async with self.bot.pool.acquire() as conn:
            await conn.execute("UPDATE snippet set content=$1 where userid=$2", json.dumps(s), ctx.author.id)
        await ctx.message.add_reaction("✅")

    @commands.command(name="snippetuse", description="use a snippet")
    async def snippetuse(self, ctx, name: str):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet where userid=$1", ctx.author.id)
        snippets = str()
        if res == []:
            snippets = " {} "
            async with self.bot.pool.acquire() as conn:
                await conn.execute("INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.author.id,json.dumps(snippets))
        else:
            snippets = res[0]["content"]
        s = json.loads(snippets)
        msg = copy.copy(ctx.message)
        msg.channel = ctx.channel 
        msg.author = ctx.channel.guild.get_member(ctx.author.id) or ctx.author
        msg.content = ctx.prefix + s[name]
        print(msg)
        new_ctx = await self.bot.get_context(msg, cls=type(ctx))
        await self.bot.invoke(new_ctx)

    @commands.command(name="snippetview", description = "View a snippet")
    async def snippetview(self, ctx, name:str):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet where userid=$1", ctx.author.id)
        snippets = str()
        if res == []:
            snippets = " {} "
            async with self.bot.pool.acquire() as conn:
                await conn.execute("INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.author.id, json.dumps(snippets))
        else:
            snippets = res[0]["content"]
        s = json.loads(snippets)
        if name in s:
            await ctx.send(embed=discord.Embed(title = f"Snippet name: {name}", description = f"{ctx.prefix}{s[name]}"))
        else:
            await ctx.send(embed=discord.Embed(title = "Error", description = "No snippet of that name is found."))

    @commands.command(name="snippetremove", description="remove a snippet", aliases = ["snippetdelete"], usage = "snippetremove <name>")
    async def snippetremove(self, ctx, name: str):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet WHERE userid=$1", ctx.author.id)

        snippets = str()
        if res == []:
            snippets = " {} "
            async with self.bot.pool.acquire() as conn:
                await conn.execute("INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.author.id, json.dumps(snippets))
        else:
            snippets = res[0]["content"]
        s = json.loads(snippets)
        try:
            del s[name]

        except:
            await ctx.send("You do not have a snippet named that!")
        print(s)
        async with self.bot.pool.acquire() as conn:
            await conn.execute("UPDATE snippet set content=$1 where userid=$2", json.dumps(s), ctx.author.id)
        await ctx.message.add_reaction("✅")


    @commands.command(name ="snippetall", description = "View all the names of your snippets", usage = "snippetall")
    async def snippetall(self, ctx):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet WHERE userid=$1", ctx.author.id)

        snippets = str()
        if res == []:
            snippets = " {} "
            async with self.bot.pool.acquire() as conn:
                await conn.execute("INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.author.id, json.dumps(snippets))
        else:
            snippets = res[0]["content"]
        s = json.loads(snippets)
        res = ""
        for i in s.keys():
            res += i + '\n'
        await ctx.send(embed = discord.Embed(title="All snippets", description = res))

    @commands.command(name = "snippetabout", description = "How to use snippets", usage = "snippetabout")
    async def snippetabout(self, ctx):
        embed = discord.Embed(title="How to use snippets in random.bot", description="Simple! Just store a snippet with snippetadd, then you can use that snippet with snippetuse! Check out other snippet related commands by flipping through the help menu.")

        embed.add_field(name="Example", value="For example, after doing\n ``@snippetadd letter choose a b c d e f g h i j k l m n o p q r s t u v w x y z``\nI can call it by doing\n``@snippetuse letter``\nand it'll choose a random letter for me! ")
        embed.add_field(name="Other commands", value="Do @help to see all commands.\nSnippet commands include\n``snippetadd``, ``snippetuse``, ``snippetview``, ``snippetall`` and ``snippetremove``. Do @help <command> to get more information.")
        embed.add_field(name="Snippet", value="If you want a dedicated bot to store snippet, then **Snippet** may be the right bot for you! You can check it out via [this link](https://snippetsite.netlify.app/)")

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Snippet(bot))

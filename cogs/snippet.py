import json

from discord.ext import commands


class Snippet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="snippetadd", description="add a snippet")
    async def snippetadd(self, ctx, name: str, *, content: str):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet WHERE userid=$1", ctx.user.id)

        snippets = str()
        if res == []:
            snippets = " {} "
            await conn.execute("INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.author.id, snippets)
        else:
            snippets = res["content"]
        s = json.loads(snippets)
        s[name] = content
        async with self.bot.pool.acquire() as conn:
            await conn.execute("UPDATE snippet set content=$1 where userid=$2", str(s), ctx.author.id)

    @commands.command(name="snippetuse", description="use a snippet")
    async def snippetuse(self, ctx, name: str):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM snippet where userid=$1", ctx.author.id)
        snippets = str()
        if res == []:
            snippets = " {} "
            await conn.execute("INSERT INTO snippet(userid,content) VALUES($1,$2)", ctx.author.id, snippets)
        else:
            snippets = res["content"]

        s = json.loads(snippets)
        msg = s["name"]
        channel = ctx.channel
        msg.channel = channel
        msg.author = channel.guild.get_member(ctx.user.id) or ctx.user
        msg.content = ctx.prefix + msg
        new_ctx = await self.bot.get_context(msg, cls=type(ctx))
        await self.bot.invoke(new_ctx)


def setup(bot):
    bot.add_cog(Snippet(bot))

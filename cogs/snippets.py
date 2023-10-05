import discord
from discord.ext import commands
from classes import converters
from discord import app_commands

class Snippets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    @app_commands.command(name="makelist", description="Store your own custom list to be used for /choose or /shuffle.")
    async def makelist(self, ctx, *, name:str, choices:str):
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                    "INSERT INTO lists(userid,name,content) VALUES($1,$2,$3)", ctx.user.id, name, choices
                )
            await ctx.response.send_message(embed=discord.Embed(description="Done!", colour=self.bot.primary_colour))
    @app_commands.command(name="deletelist", description="Delete your own custom list.")
    async def deletelist(self, ctx, *, name:str):
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                    "DELETE FROM lists WHERE userid=$1 AND name=$2", ctx.user.id, name
                )
            await ctx.response.send_message(embed=discord.Embed(description="Done!", colour=self.bot.primary_colour))
    @app_commands.command(name="viewlist", description="List your own custom list.")
    async def list(self, ctx):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM lists WHERE userid=$1", ctx.user.id)
            if res == []:
                await ctx.response.send_message(embed=discord.Embed(description="You don't have any lists!", colour=self.bot.primary_colour))
            else:
                res = [i["name"] for i in res]
                await ctx.response.send_message(embed=discord.Embed(description="\n".join(res), colour=self.bot.primary_colour))
    @app_commands.command(name="listcontent", description="List the content of your own custom list.")
    async def listcontent(self, ctx, *, name:str):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT * FROM lists WHERE userid=$1 AND name=$2", ctx.user.id, name)
            if res == []:
                await ctx.response.send_message(embed=discord.Embed(description="You don't have any lists!", colour=self.bot.primary_colour))
            else:
                res = res[0]["content"]
                await ctx.response.send_message(embed=discord.Embed(description=res, colour=self.bot.primary_colour))
    


async def setup(bot):
    await bot.add_cog(Snippets(bot))

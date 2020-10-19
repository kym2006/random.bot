import json

import aiohttp
import discord
from discord.ext import commands


class Animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Sends a random dog image", usage="dog")
    async def dog(self, ctx):
        url = "https://dog.ceo/api/breeds/image/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(colour=self.bot.primary_colour)
                embed.set_image(url=res["message"])
                await ctx.send(embed=embed)

    @commands.command(description="Sends a random dog fact", usage="dogfact")
    async def dogfact(self, ctx):
        url = "https://dog-api.kinduff.com/api/facts"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                await ctx.send(embed=discord.Embed(description=res["facts"], colour=self.bot.primary_colour))

    @commands.command(description="Sends a random cat image", usage="cat")
    async def cat(self, ctx):
        url = "https://aws.random.cat/meow"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(colour=self.bot.primary_colour)
                embed.set_image(url=res["file"])
                await ctx.send(embed=embed)

    @commands.command(description="Sends a random cat fact", usage="catfact")
    async def catfact(self, ctx):
        url = "https://catfact.ninja/fact"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(colour=self.bot.primary_colour)
                embed.set_image(url=res["fact"])
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Animals(bot))

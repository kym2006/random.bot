import json

import aiohttp
import discord
from discord.ext import commands

class More(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(description="Sends a random activity", usage="activity")
    async def activity(self, ctx):
        url = "https://boredapi.com/api/activity"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(description=res["activity"], colour=self.bot.primary_colour)
                embed.set_footer(text=f"Type: {res['type']}")
                await ctx.send(embed=embed)

    @commands.command(description="Sends a random piece of advice", usage="advice")
    async def advice(self, ctx):
        url = "https://api.adviceslip.com/advice"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(description=res["slip"]["advice"], colour=self.bot.primary_colour)
                await ctx.send(embed=embed)

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
                await ctx.send(embed=discord.Embed(description=res["fact"], colour=self.bot.primary_colour))

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
                await ctx.send(embed=discord.Embed(description=res["facts"][0], colour=self.bot.primary_colour))

    @commands.command(description="Sends a random joke", usage="joke")
    async def joke(self, ctx):
        url = "https://official-joke-api.appspot.com/jokes/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                await ctx.send(
                    embed=discord.Embed(
                        title=res["type"],
                        description=f'Setup: {res["setup"]}\nPunchline: {res["punchline"]}',
                        colour=self.bot.primary_colour
                    )
                )

    @commands.command(description="Sends a random (inspirational?) quote", usage="quote")
    async def quote(self, ctx):
        url = "https://api.quotable.io/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(description=res["content"], colour=self.bot.primary_colour)
                embed.set_author(name=res["author"])
                await ctx.send(embed=embed)

    @commands.command(description="Sends a random quote by Trump", usage="trump")
    async def trump(self, ctx):
        url = "https://api.tronalddump.io/random/quote"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(description=res["value"], colour=self.bot.primary_colour)
                embed.set_author(name="Donald Trump")
                await ctx.send(embed=embed)
                              
    @commands.command(description="Sends a random word", usage="word")
    async def word(self, ctx):
        url = "https://random-word-api.herokuapp.com/word"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(description=res[0], colour=self.bot.primary_colour)
                await ctx.send(embed=embed)


    



def setup(bot):
    bot.add_cog(More(bot))

import json

import aiohttp
import discord
from discord.ext import commands
from discord import app_commands

class More(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    

    @app_commands.command(description="Sends a random wikipedia page")
    async def wikipedia(self, ctx):
        url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(title=res["title"], description=res["extract"], colour=self.bot.primary_colour)
                embed.set_image(url=res["thumbnail"]["source"])
                await ctx.response.send_message(embed=embed)

    @app_commands.command(description="Sends a random xkcd comic")
    async def xkcd(self, ctx):
        url = "https://xkcd.com/info.0.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                num = random.randint(1, res["num"])
                url = f"https://xkcd.com/{num}/info.0.json"
                async with session.get(url) as data:
                    res = json.loads(await data.text())
                    embed = discord.Embed(title=res["title"], description=res["alt"], colour=self.bot.primary_colour)
                    embed.set_image(url=res["img"])
                    await ctx.response.send_message(embed=embed)
    
    @app_commands.command(description="Sends a random anime waifu")
    async def waifu(self, ctx):
        url = "https://api.waifu.pics/sfw/waifu"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(colour=self.bot.primary_colour)
                embed.set_image(url=res["url"])
                await ctx.response.send_message(embed=embed)

    @commands.is_nsfw()
    @app_commands.command(description="Send a random nsfw picture")
    async def nsfw(self, ctx):
        channel_nsfw = await self.is_nsfw(ctx.message.channel) 
        if not channel_nsfw: 
            print("You cannot use this command in a non-nsfw channel")
            return
        url = "https://api.waifu.pics/nsfw/waifu"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(colour=self.bot.primary_colour)
                embed.set_image(url=res["url"])
                await ctx.response.send_message(embed=embed)


    
    @app_commands.command(description="Sends a random fact")
    async def fact(self, ctx):
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                await ctx.response.send_message(embed=discord.Embed(description=res["text"], colour=self.bot.primary_colour))

    @app_commands.command(description="Sends a random number fact")
    async def numberfact(self, ctx, number:int):
        url = f"http://numbersapi.com/{number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                await ctx.response.send_message(embed=discord.Embed(description=await data.text(), colour=self.bot.primary_colour))
        
    @app_commands.command(description="Sends a random activity")
    async def activity(self, ctx):
        url = "https://boredapi.com/api/activity"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(description=res["activity"], colour=self.bot.primary_colour)
                embed.set_footer(text=f"Type: {res['type']}")
                await ctx.response.send_message(embed=embed)

    @app_commands.command(description="Sends a random piece of advice")
    async def advice(self, ctx):
        url = "https://api.adviceslip.com/advice"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(description=res["slip"]["advice"], colour=self.bot.primary_colour)
                await ctx.response.send_message(embed=embed)

    @app_commands.command(description="Sends a random cat image")
    async def cat(self, ctx):
        url = "https://aws.random.cat/meow"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(colour=self.bot.primary_colour)
                embed.set_image(url=res["file"])
                await ctx.response.send_message(embed=embed)

    @app_commands.command(description="Sends a random cat fact")
    async def catfact(self, ctx):
        url = "https://catfact.ninja/fact"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                await ctx.response.send_message(embed=discord.Embed(description=res["fact"], colour=self.bot.primary_colour))

    @app_commands.command(description="Sends a random dog image")
    async def dog(self, ctx):
        url = "https://dog.ceo/api/breeds/image/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(colour=self.bot.primary_colour)
                embed.set_image(url=res["message"])
                await ctx.response.send_message(embed=embed)

    @app_commands.command(description="Sends a random dog fact")
    async def dogfact(self, ctx):
        url = "https://dog-api.kinduff.com/api/facts"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                await ctx.response.send_message(embed=discord.Embed(description=res["facts"][0], colour=self.bot.primary_colour))

    @app_commands.command(description="Sends a random joke")
    async def joke(self, ctx):
        url = "https://official-joke-api.appspot.com/jokes/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                await ctx.response.send_message(
                    embed=discord.Embed(
                        title=res["type"],
                        description=f'Setup: {res["setup"]}\nPunchline: {res["punchline"]}',
                        colour=self.bot.primary_colour
                    )
                )

    @app_commands.command(description="Sends a random (inspirational?) quote")
    async def quote(self, ctx):
        url = "https://api.quotable.io/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(description=res["content"], colour=self.bot.primary_colour)
                embed.set_author(name=res["author"])
                await ctx.response.send_message(embed=embed)

    @app_commands.command(description="Sends a random quote by Trump")
    async def trump(self, ctx):
        url = "https://api.tronalddump.io/random/quote"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(description=res["value"], colour=self.bot.primary_colour)
                embed.set_author(name="Donald Trump")
                await ctx.response.send_message(embed=embed)
                              
    @app_commands.command(description="Sends a random word")
    async def word(self, ctx):
        url = "https://random-word-api.herokuapp.com/word"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(description=res[0], colour=self.bot.primary_colour)
                await ctx.response.send_message(embed=embed)


    



async def setup(bot):
    await bot.add_cog(More(bot))

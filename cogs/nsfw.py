import json
import random
import aiohttp
import discord
from discord.ext import commands
from discord import app_commands

class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(description="Send a random nsfw picture")
    async def nsfw(self, ctx):
        # check if channel is nsfw
        if not ctx.channel.is_nsfw():
            return await ctx.response.send_message(embed=discord.Embed(description="This command can only be used in NSFW channels.", colour=self.bot.error_colour))
        url = "https://api.waifu.pics/nsfw/waifu"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(colour=self.bot.primary_colour)
                embed.set_image(url=res["url"])
                await ctx.response.send_message(embed=embed)
    
    @app_commands.command(description="Send a random hentai picture")
    async def hentai(self, ctx):
        # check if channel is nsfw
        if not ctx.channel.is_nsfw():
            return await ctx.response.send_message(embed=discord.Embed(description="This command can only be used in NSFW channels.", colour=self.bot.error_colour))
        url = "https://api.waifu.pics/nsfw/neko"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(colour=self.bot.primary_colour)
                embed.set_image(url=res["url"])
                await ctx.response.send_message(embed=embed)

    @app_commands.command(description="Send a random nude picture from reddit")
    async def nude(self, ctx):
        # check if channel is nsfw
        if not ctx.channel.is_nsfw():
            return await ctx.response.send_message(embed=discord.Embed(description="This command can only be used in NSFW channels.", colour=self.bot.error_colour))
        url = "https://www.reddit.com/r/nsfw/random.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(colour=self.bot.primary_colour)
                embed.set_image(url=res[0]["data"]["children"][0]["data"]["url"])
                await ctx.response.send_message(embed=embed)
    
    @app_commands.command(description="Send a random hentai picture from reddit")
    async def rhentai(self, ctx):
        # check if channel is nsfw
        if not ctx.channel.is_nsfw():
            return await ctx.response.send_message(embed=discord.Embed(description="This command can only be used in NSFW channels.", colour=self.bot.error_colour))
        url = "https://www.reddit.com/r/hentai/random.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                res = json.loads(await data.text())
                embed = discord.Embed(colour=self.bot.primary_colour)
                embed.set_image(url=res[0]["data"]["children"][0]["data"]["url"])
                await ctx.response.send_message(embed=embed)

    @app_commands.command(description="Send a random pornhub video")
    async def phub(self, ctx):
        # check if channel is nsfw
        if not ctx.channel.is_nsfw():
            return await ctx.response.send_message(embed=discord.Embed(description="This command can only be used in NSFW channels.", colour=self.bot.error_colour))
        url = "https://www.pornhub.com/random"
        await ctx.response.send_message(url)
    



    
        

async def setup(bot):
    await bot.add_cog(Nsfw(bot))

import logging
import random
import json
import aiohttp
import discord
from discord.ext import commands
from discord import app_commands
from classes import converters
from utils import checks
log = logging.getLogger(__name__)
import random 
# API with random.org

class Randomdotorg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="org", description="A group of commands whereby random.org api is used to generate more cryptographically secure results")

    @app_commands.command(name="orginfo", description="A group of commands whereby random.org api is used to generate more cryptographically secure results")
    async def org(self, ctx):
        cog = self.bot.get_cog("Randomdotorg")
        commands = [c.qualified_name for c in cog.walk_app_commands()]
        res = "```\nCommands using random.org api:\n"
        for i in commands:
            res += i+'\n'
        res += '```'
        await ctx.response.send_message(embed=discord.Embed(description=res, colour=self.bot.config.primary_colour))

    async def get_data(self,payload):
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.random.org/json-rpc/1/invoke", data=json.dumps(payload)) as r:  
                js=await r.json()
                return js['result']

    @checks.is_patron()
    @group.command(name="randint", description="Get a random integer from <start> to <end>, using random.org api")
    async def randint(self, ctx, start: int, end: int):
        if start == end:
            await ctx.response.send_message("What do you think?")
            return 
        if start > end:
            start,end=end,start
        payload={"jsonrpc":"2.0","method":"generateIntegers","params":{"apiKey":self.bot.config.randomorg,"n":1,"min":start,"max":end,"replacement":True,"base":10},"id":1}
        res=await self.get_data(payload)
        await ctx.response.send_message(embed=discord.Embed(description=f"Picked {res['random']['data'][0]} from {start} to {end}",colour=self.bot.config.primary_colour))

    @checks.is_patron()
    @group.command(name="choose", description="Choose something from the list, using random.org api. Separate with comma")
    async def choose(self, ctx, *, args:str):
        args=args.split(',')
        if len(args)==0:
            await ctx.response.send_message("Give me something to choose!")
            return 
        elif len(args) == 1:
            await ctx.response.send_message("What do you think?")
            return 
        payload={"jsonrpc":"2.0","method":"generateIntegers","params":{"apiKey":self.bot.config.randomorg,"n":1,"min":0,"max":len(args)-1,"replacement":True,"base":10},"id":2}
        res=await self.get_data(payload) 
        await ctx.response.send_message(embed=discord.Embed(description=f"Picked `{args[res['random']['data'][0]]}`!", colour=self.bot.config.primary_colour))
    
    @checks.is_patron()
    @group.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, ctx):
        payload={"jsonrpc":"2.0","method":"generateIntegers","params":{"apiKey":self.bot.config.randomorg,"n":1,"min":0,"max":1,"replacement":True,"base":10},"id":3}
        res=await self.get_data(payload)
        guild = self.bot.get_guild(725303414220914758)
        heads = [e for e in guild.emojis if e.name == "washingtonheads"][0]
        tails = [e for e in guild.emojis if e.name == "washingtontails"][0]
        await ctx.response.send_message([heads, tails][res['random']['data'][0]])

async def setup(bot):
    await bot.add_cog(Randomdotorg(bot))

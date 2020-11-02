import logging
import random
import json
import aiohttp
import discord
from discord.ext import commands
from classes import converters
from utils import checks
log = logging.getLogger(__name__)
# API with random.org

class Org(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #@checks.is_patron()
    @commands.group()
    async def org(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=discord.Embed(description=f"Invalid command! Do `{ctx.prefix}help` or `{ctx.prefix}commands` to find out the commands!"))
    
    async def get_data(self,payload):
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.random.org/json-rpc/1/invoke", data=json.dumps(payload)) as r:  
                js=await r.json()
                return js['result']

    @checks.is_patron()
    @org.command()
    async def randint(self,ctx,start:int,end:int):
        payload={"jsonrpc":"2.0","method":"generateIntegers","params":{"apiKey":self.bot.config.randomorg,"n":1,"min":start,"max":end,"replacement":True,"base":10},"id":29440}
        res=await self.get_data(payload)
        await ctx.send(embed=discord.Embed(description=f"Picked {res['random']['data'][0]} from {start} to {end}",colour=self.bot.config.primary_colour))


def setup(bot):
    bot.add_cog(Org(bot))

import logging
import random
import json
import aiohttp
import discord
from discord.ext import commands
from classes import converters
from utils import checks
log = logging.getLogger(__name__)
import random 
# API with random.org

class Randomdotorg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #@checks.is_patron()
    @commands.group(usage="org", description="A group of commands whereby random.org api is used to generate more cryptographically secure results")
    async def org(self,ctx):
        if ctx.invoked_subcommand is None:
            cog=self.bot.get_cog("Org")
            commands=[c.qualified_name for c in cog.walk_commands()]
            res="```\nCommands using random.org api:\n"
            for i in commands:
                res+=i+'\n'
            res+='```'
            await ctx.send(embed=discord.Embed(description=res,colour=self.bot.config.primary_colour))
            
    
    async def get_data(self,payload):
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.random.org/json-rpc/1/invoke", data=json.dumps(payload)) as r:  
                js=await r.json()
                return js['result']

    @checks.is_patron()
    @org.command(usage="randint <start> <end>", description="Get a random integer from <start> to <end>, using random.org api")
    async def randint(self,ctx,start:int,end:int):
        if start == end:
            await ctx.send("What do you think?")
            return 
        if start > end:
            start,end=end,start
        payload={"jsonrpc":"2.0","method":"generateIntegers","params":{"apiKey":self.bot.config.randomorg,"n":1,"min":start,"max":end,"replacement":True,"base":10},"id":1}
        res=await self.get_data(payload)
        await ctx.send(embed=discord.Embed(description=f"Picked {res['random']['data'][0]} from {start} to {end}",colour=self.bot.config.primary_colour))

    @checks.is_patron()
    @org.command(usage="choose <list of things to choose from, separated by space>", description="Choose something from the list, using random.org api")
    async def choose(self, ctx, *args):
        args=list(args)
        if len(args)==0:
            await ctx.send("Give me something to choose!")
            return 
        elif len(args) == 1:
            await ctx.send("What do you think?")
            return 
        payload={"jsonrpc":"2.0","method":"generateIntegers","params":{"apiKey":self.bot.config.randomorg,"n":1,"min":0,"max":len(args)-1,"replacement":True,"base":10},"id":2}
        res=await self.get_data(payload) 
        await ctx.send(embed=discord.Embed(description=f"Picked `{args[res['random']['data'][0]]}`!", colour=self.bot.config.primary_colour))
    
    @checks.is_patron()
    @org.command(usage="coinflip", description="Flip a coin")
    async def coinflip(self, ctx):
        payload={"jsonrpc":"2.0","method":"generateIntegers","params":{"apiKey":self.bot.config.randomorg,"n":1,"min":0,"max":1,"replacement":True,"base":10},"id":3}
        res=await self.get_data(payload)
        guild = self.bot.get_guild(725303414220914758)
        heads = [e for e in guild.emojis if e.name == "washingtonheads"][0]
        tails = [e for e in guild.emojis if e.name == "washingtontails"][0]
        await ctx.send([heads, tails][res['random']['data'][0]])

def setup(bot):
    bot.add_cog(Randomdotorg(bot))

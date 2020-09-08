import logging
import platform

import discord
import psutil
import datetime
from discord.ext import commands
import asyncpg 
log = logging.getLogger(__name__)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "mine", description = "mine for ~~bit~~silver coins")
    async def mine(self, ctx):
        id = ctx.message.author.id
        row = await self.bot.conn.fetchrow(
        'SELECT * FROM credit WHERE userid = $1', id)
        if row == None:
            await self.bot.conn.execute('''
            INSERT INTO credit(userid, silver, gold) VALUES($1, $2, $3)
        ''', id, 1, 0)
        else:
            newval = row['silver'] + 1 
            
            await self.bot.conn.execute('''
            UPDATE credit
            SET silver = $1
            WHERE userid = $2
            ''', newval, id)
        row = await self.bot.conn.fetchrow(
        'SELECT * FROM credit WHERE userid = $1', id)
        await ctx.send(f"You now have {row['silver']} silver.")



    



def setup(bot):
    bot.add_cog(Events(bot))

import logging
import platform
import json 
import discord
import psutil
import datetime
from discord.ext import commands
import asyncpg 
import requests 
log = logging.getLogger(__name__)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "mine", description = "mine for ~~bit~~silver coins", usage = "<mine>")
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
    
    @commands.command(name = "leaderboard", description = "See the richest people", usage = "leaderboard")
    async def leaderboard(self, ctx):
        rows = await self.bot.conn.fetch('SELECT * FROM credit')
        payload = ""
        data = []
        for i in rows:
            user = self.bot.get_user(i['userid'])
            data.append((i['silver'], i['gold'], f"{user.name}#{user.discriminator}"))
            
        data = sorted(data, key = lambda x:x[0]+x[1], reverse=True)
        gold = self.bot.get_emoji(635020560249913394)
        silver = self.bot.get_emoji(635020537349013519)
        for i in data:
            payload += f"{i[2]}: {i[0]} {silver}, {i[1]} {gold}\n"
        response = requests.post('https://hastebin.com/documents', data=payload.encode('utf-8'))
        li = json.loads(response.content)
        key = li['key']
        await ctx.send(embed=discord.Embed(description="Full leaderboard: {}".format("https://hastebin.com/" + key)))
        partial = ""
        for i in payload.split('\n')[:10]:
            partial += i+'\n'
        await ctx.send(embed=discord.Embed(header="Top 5", description = partial))

    



def setup(bot):
    bot.add_cog(Events(bot))

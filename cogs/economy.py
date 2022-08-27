import logging
import random

import aiohttp
import discord
from discord.ext import commands
from classes import converters
import time 
cooldown = dict({"mine": dict()})
log = logging.getLogger(__name__)
cdtime = 3

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def on_cooldown(self, cmd, id):
        if id not in cooldown[cmd]:
            return False 
        dif = time.time() - cooldown[cmd][id]
        return dif < cdtime 

    @commands.command(name="mine", description="mine for ~~bit~~silver coins", usage="mine")
    async def mine(self, ctx):
        id = ctx.author.id 
        if self.on_cooldown("mine", id):
            dif = time.time() - cooldown["mine"][id]
            await ctx.response.send_message(embed=discord.Embed(title="You are rate-limited!", description=f"Try again in {round(cdtime-dif,1)} seconds!", colour=self.bot.config.primary_colour))
            return 
        cooldown["mine"][id] = time.time()
        
        row=await self.bot.get_user_data(ctx.author.id)
        newval = row["silver"] + 1
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                    """
            UPDATE credit
            SET silver = $1
            WHERE userid = $2
            """,
                newval,
                id,
            )
        await ctx.response.send_message(
            embed=discord.Embed(description=f"You now have {newval} silver.", colour=self.bot.primary_colour)
        )

    @commands.command(
        name="bet",
        description="Double or nothing!",
        usage="bet <amount>",
        aliases=["gamble"],
    )
    async def bet(self, ctx, amount: int):
        if amount < 0:
            await ctx.response.send_message("positive amounts only")
            return
        id = ctx.author.id
        row=await self.bot.get_user_data(id)
        have = row["silver"]
        if amount > have:
            await ctx.response.send_message("You do not have enough money to bet that much")
            return
        else:
            newval = row["silver"] + random.choice([1, -1]) * amount
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    """
            UPDATE credit
            SET silver = $1
            WHERE userid = $2
            """,
                    newval,
                    id,
                )
        await ctx.response.send_message(
            embed=discord.Embed(
                description=f"You got {newval-row['silver']} silver. You now have {newval} silver.",
                colour=self.bot.primary_colour,
            ),
        )
    
    @commands.command(name="give", description="Give money to someone", usage="give <user> <amount>")
    async def give(self, ctx,  user: converters.GlobalUser, amount:int):
        if amount < 0:
            await ctx.response.send_message(embed=discord.Embed(description="That would be stealing!"))
            return 
        row=await self.bot.get_user_data(ctx.author.id)
        have = row["silver"]
        if amount > have:
            await ctx.response.send_message("You do not have enough money to give that much")
            return
        else:
            newval = row["silver"] - amount
            async with self.bot.pool.acquire() as conn:
                await conn.execute("UPDATE credit SET silver=$1 where userid=$2", newval, ctx.author.id)
                given = await conn.fetchrow("SELECT * FROM credit where userid=$1", user.id)
                if given is None:
                    await conn.execute("INSERT INTO credit(userid, silver, gold) VALUES($1,$2,$3)",user.id, amount, 0)
                else:

                    await conn.execute("UPDATE credit SET silver=$1 where userid=$2", given['silver']+amount, user.id)
        await ctx.response.send_message(
            embed=discord.Embed(
                description=f"You gave {amount} silver to {user.name}#{user.discriminator}. You now have {newval} silver.",
                colour=self.bot.primary_colour,
            ),
        )

    @commands.command(name="leaderboard", description="See the richest people", usage="leaderboard")
    async def leaderboard(self, ctx):
        async with self.bot.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM credit")
        payload = ""
        data = []
        for i in rows:
            user = self.bot.get_user(i["userid"])
            try:
                data.append((i["silver"], i["gold"], user.id, i['displaytext']))
            except AttributeError:
                pass

        data = sorted(data, key=lambda x: x[0] + x[1], reverse=True)
        gold = self.bot.get_emoji(635020560249913394)
        silver = self.bot.get_emoji(635020537349013519)
        for i in data:
            payload += f"{self.bot.get_user(i[2]).name}#{self.bot.get_user(i[2]).discriminator} - ** {i[3]} ** : {i[0]} {silver}, {i[1]} {gold}\n"
        partial = ""
        for i in payload.split("\n")[:10]:
            partial += i + "\n"
        rank = 1
        found = False
        for i in data:
            if ctx.author.id == i[2]:
                found = True 
                partial += f"Your rank: {rank}/{len(data)}\n"
                await ctx.response.send_message(embed=discord.Embed(title="Top 10", description=partial, colour=self.bot.primary_colour))
                break 
            else:
                rank += 1
        if found == False:
            await ctx.response.send_message(embed=discord.Embed(title="Top 10", description=partial, colour=self.bot.primary_colour))
        payload = payload.replace("<:silver:635020537349013519>", "silver")
        payload = payload.replace("<:gold:635020560249913394>", "gold")
        payload = payload.replace('**', '')
        data = {
            "api_dev_key":self.bot.config.pastebin,
            "api_option":"paste",
            "api_paste_code":payload
        }
        async with aiohttp.ClientSession() as session:
            async with session.post("https://pastebin.com/api/api_post.php", data=data) as r:
                if r.status == 200:
                    res = await r.text()
                    await ctx.response.send_message(
                        embed=discord.Embed(
                            description="Full leaderboard: {}".format(res),
                            colour=self.bot.primary_colour,
                        )
                    )

    @commands.command(name="displaytext", description="Set what you would like your text to be displayed as", usage="displaytext <text>")
    async def displaytext(self,ctx,*,content):
        await self.bot.get_user_data(ctx.author.id)
        if len(content) > 50:
            await ctx.response.send_message("Max characters of text is 50!")
            return 
        async with self.bot.pool.acquire() as conn:
            await conn.execute("UPDATE credit set displaytext=$1 where userid=$2", content, ctx.author.id)
        await ctx.response.send_message(embed=discord.Embed(description=f"Updated your displaytext! (Use `{ctx.prefix}leaderboard` to check!)",colour=self.bot.config.primary_colour))


async def setup(bot):
    await bot.add_cog(Economy(bot))
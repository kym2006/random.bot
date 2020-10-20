import logging
import random

import aiohttp
import discord
from discord.ext import commands

log = logging.getLogger(__name__)


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mine", description="mine for ~~bit~~silver coins", usage="mine")
    async def mine(self, ctx):
        id = ctx.message.author.id
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM credit WHERE userid = $1", id)
        if row is None:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    """
            INSERT INTO credit(userid, silver, gold) VALUES($1, $2, $3)
        """,
                    id,
                    1,
                    0,
                )
        else:
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
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM credit WHERE userid = $1", id)
            await ctx.send(
                embed=discord.Embed(description=f"You now have {row['silver']} silver.", colour=self.bot.primary_colour)
            )

    @commands.command(
        name="bet",
        description="Double or nothing!",
        usage="bet <amount>",
        aliases=["gamble"],
    )
    async def bet(self, ctx, amount: int):
        if amount < 0:
            await ctx.send("positive amounts only")
            return
        id = ctx.message.author.id
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM credit WHERE userid = $1", id)
        if row is None:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    """
            INSERT INTO credit(userid, silver, gold) VALUES($1, $2, $3)
        """,
                    id,
                    1,
                    0,
                )
            await ctx.send("You cannot bet anything due to your lack of funds")
            return
        have = row["silver"]
        if amount > have:
            await ctx.send("You do not have enough money to bet that much")
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
        await ctx.send(
            embed=discord.Embed(
                description=f"You got {newval-row['silver']} silver. You now have {newval} silver.",
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
                data.append((i["silver"], i["gold"], f"{user.name}#{user.discriminator}"))
            except AttributeError:
                pass

        data = sorted(data, key=lambda x: x[0] + x[1], reverse=True)
        """
        gold = self.bot.get_emoji(752769769895100447)
        silver = self.bot.get_emoji(752770848808763432)
        """
        gold = self.bot.get_emoji(635020560249913394)
        silver = self.bot.get_emoji(635020537349013519)
        for i in data:
            payload += f"{i[2]}: {i[0]} {silver}, {i[1]} {gold}\n"
        partial = ""
        for i in payload.split("\n")[:10]:
            partial += i + "\n"
        await ctx.send(embed=discord.Embed(title="Top 10", description=partial, colour=self.bot.primary_colour))
        payload = payload.replace("<:silver:635020537349013519>", "silver")
        payload = payload.replace("<:gold:635020560249913394>", "gold")
        async with aiohttp.ClientSession() as session:
            async with session.post("https://hasteb.in/documents", data=payload.encode("utf-8")) as r:
                if r.status == 200:
                    js = await r.json()
                    key = js["key"]
                    await ctx.send(
                        embed=discord.Embed(
                            description="Full leaderboard: {}".format("https://hasteb.in/" + key),
                            colour=self.bot.primary_colour,
                        )
                    )


def setup(bot):
    bot.add_cog(Economy(bot))

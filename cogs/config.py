import asyncio
import random
import typing

import discord
from discord.ext import commands


# This cog implements a lot of the random functions of random.bot
class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(
        description="Change the prefix or view the current prefix.",
        usage="prefix [new prefix]",
        aliases=["setprefix"],
    )
    async def prefix(self, ctx, *, prefix: str = None):
        if prefix is None:
            await ctx.send(
                embed=discord.Embed(
                    description=f"The prefix for this server is `{ctx.prefix}`.",
                    colour=self.bot.primary_colour,
                )
            )
            return
        if ctx.author.guild_permissions.administrator is False:
            await ctx.send("You need to be an administrator to do this.")
            return
        else:
            if len(prefix) > 10:
                await ctx.send(
                    embed=discord.Embed(
                        description="The chosen prefix is too long.",
                        colour=discord.Color.red(),
                    )
                )
                return
            if prefix == "@":
                prefix = None
            have = await self.bot.conn.fetchrow(
                "SELECT * FROM data WHERE guild=$1", ctx.guild.id
            )
            print(have)
            if have == None:
                print("hi")
                await self.bot.conn.execute(
                    "INSERT INTO data(guild, prefix) VALUES($1, $2);",
                    ctx.guild.id,
                    prefix,
                )
            else:

                await self.bot.conn.execute(
                    "UPDATE data SET prefix=$1 WHERE guild=$2", prefix, ctx.guild.id
                )
            await ctx.send(
                embed=discord.Embed(
                    description="Successfully changed the prefix to "
                    f"`{'@' if prefix is None else prefix}`.",
                    colour=self.bot.primary_colour,
                )
            )


def setup(bot):
    bot.add_cog(Config(bot))

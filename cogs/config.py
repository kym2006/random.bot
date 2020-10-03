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


    @commands.guild_only()
    @commands.command(
        name="toggleping",
        usage="toggleping",
        description="toggle between pinging a user or not",
    )
    async def toggleping(self, ctx):
        member = ctx.guild.get_member(ctx.author.id)
        if not member.guild_permissions.administrator:
            await ctx.send(
                "You do not have permissions in this server to use this command."
            )
            return
        row = await self.bot.conn.fetchrow(
            "SELECT * FROM ping WHERE serverid=$1", ctx.guild.id
        )
        if row == None:
            await self.bot.conn.execute(
                """INSERT INTO ping(serverid, haveping) VALUES($1, $2)""",
                ctx.guild.id,
                0,
            )
        row = await self.bot.conn.fetchrow(
            "SELECT * FROM ping WHERE serverid=$1", ctx.guild.id
        )
        await self.bot.conn.execute(
            """
        UPDATE ping
        SET haveping=$1
        WHERE serverid=$2
        """,
            1 - row["haveping"],
            ctx.guild.id,
        )
        await ctx.send("Successfuly updated your settings!")


def setup(bot):
    bot.add_cog(Config(bot))

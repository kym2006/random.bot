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
        description="Change the prefix or view the current prefix.", usage="prefix [new prefix]", aliases=["setprefix"]
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
            raise commands.MissingPermissions(["administrator"])
        else:
            if len(prefix) > 10:
                await ctx.send(
                    embed=discord.Embed(
                        description="The chosen prefix is too long.",
                        colour=self.bot.error_colour,
                    )
                )
                return
            if prefix == self.bot.config.default_prefix:
                prefix = None
            await self.bot.get_data(ctx.guild.id)
            async with self.bot.pool.acquire() as conn:
                await conn.execute("UPDATE data SET prefix=$1 WHERE guild=$2", prefix, ctx.guild.id)
            self.bot.all_prefix[ctx.guild.id] = prefix
            await ctx.send(
                embed=discord.Embed(
                    description="Successfully changed the prefix to "
                    f"`{self.bot.config.default_prefix if prefix is None else prefix}`.",
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
            await ctx.send("You do not have permissions in this server to use this command.")
            return
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", ctx.guild.id)
        if row == None:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    """INSERT INTO data(guild, ping) VALUES($1, $2)""",
                    ctx.guild.id,
                    False,
                )
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", ctx.guild.id)
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                """
        UPDATE data
        SET ping=$1
        WHERE guild=$2
        """,
                1 - row["ping"],
                ctx.guild.id,
            )
        await ctx.send("Successfuly updated your settings!")


def setup(bot):
    bot.add_cog(Config(bot))

import logging

import discord

from discord.ext import commands

log = logging.getLogger(__name__)

owners = [298661966086668290, 412969691276115968, 446290930723717120, 488283878189039626,685456111259615252]
admins = []
def is_owner():
    def predicate(ctx):
        if ctx.author.id not in owners:
            raise commands.NotOwner()
        else:
            return True

    return commands.check(predicate)


def is_admin():
    def predicate(ctx):
        if ctx.author.id not in admins and ctx.author.id not in owners:
            raise commands.NotOwner()
        else:
            return True

    return commands.check(predicate)



def is_premium():
    async def predicate(ctx):
        async with ctx.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT guild FROM premium")
        all_premium = []
        for row in res:
            all_premium.extend(row[0])
        if ctx.guild.id not in all_premium:
            await ctx.send(
                embed=discord.Embed(
                    description="This server does not have premium. Want to get premium? More information "
                    f"is available with the `{ctx.prefix}premium` command.",
                    colour=ctx.bot.error_colour,
                )
            )
            return False
        else:
            return True

    return commands.check(predicate)


def is_patron():
    async def predicate(ctx):
        async with ctx.bot.pool.acquire() as conn:
            res = await conn.fetchrow("SELECT identifier FROM premium WHERE identifier=$1", ctx.author.id)
        if res:
            return True
        slots = await ctx.bot.tools.get_premium_slots(ctx.bot, ctx.author.id)
        if slots is False:
            await ctx.send(
                embed=discord.Embed(
                    description="This command requires you to be a patron. Want to become a patron? More "
                    f"information is available with the `{ctx.prefix}premium` command.",
                    colour=ctx.bot.error_colour,
                )
            )
            return False
        else:
            async with ctx.bot.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO premium (identifier, guild) VALUES ($1, $2)",
                    ctx.author.id,
                    [],
                )
            return True

    return commands.check(predicate)


def is_mod():
    async def predicate(ctx):
        has_role = False
        roles = (await ctx.bot.get_data(ctx.guild.id))[3]
        for role in roles:
            role = ctx.guild.get_role(role)
            if not role:
                continue
            if role in ctx.author.roles:
                has_role = True
                break
        if has_role is False and ctx.author.guild_permissions.administrator is False:
            await ctx.send(
                embed=discord.Embed(
                    description=f"You do not have access to use this command.",
                    colour=ctx.bot.error_colour,
                )
            )
            return False
        else:
            return True

    return commands.check(predicate)
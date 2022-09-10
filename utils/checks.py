from discord.ext import commands
import discord
from discord import app_commands
def is_owner():
    async def predicate(ctx):
        if ctx.user.id not in ctx.client.config.owners:
            return False
        else:
            return True

    return app_commands.check(predicate)


def is_admin():
    async def predicate(ctx):
        if ctx.user.id not in ctx.client.config.owners and ctx.user.id not in ctx.client.config.admins:
            return False
        else:
            return True

    return app_commands.check(predicate)

def is_patron():
    async def predicate(ctx):
        guild = await ctx.client.fetch_guild(725303414220914758)
        await guild.chunk()
        can = 0
        members = []
        async for i in guild.fetch_members(limit=None):
            members.append(i)
        if ctx.user.id in [g.id for g in members]:
            patron1 = discord.utils.find(lambda r: r.id == ctx.client.config.patron1, guild.roles)
            patron2 = discord.utils.find(lambda r: r.id == ctx.client.config.patron2, guild.roles)
            patron3 = discord.utils.find(lambda r: r.id == ctx.client.config.patron3, guild.roles)
            member = guild.get_member(ctx.user.id)
            print(member)
            print(member.roles)
            if patron1 in member.roles:
                can = 1
            if patron2 in member.roles:
                can = 1
            if patron3 in member.roles:
                can = 1
        if can:
            return True 
        else:
            await ctx.response.send_message(embed=discord.Embed(
                description=f"You do not have access to this command, as it is a premium only command. More information is available with the `/donate` command.",
                colour=ctx.client.config.primary_colour
            ))
            return False 

    return app_commands.check(predicate)
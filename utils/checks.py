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
        # check if the user has the patron role in the main server
        guild = ctx.client.get_guild(ctx.client.config.main_server)
        member = guild.get_member(ctx.user.id)
        if not member:
            return False
        # check if the user has the patron role
        if ctx.client.config.patron1 in [i.id for i in member.roles] or ctx.client.config.patron2 in [i.id for i in member.roles] or ctx.client.config.patron3 in [i.id for i in member.roles]:
            return True
        else:
            return False
        

    return app_commands.check(predicate)
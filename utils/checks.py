from discord.ext import commands
import discord 

def is_owner():
    async def predicate(ctx):
        if ctx.author.id not in ctx.bot.config.owners:
            raise commands.NotOwner()
        else:
            return True

    return commands.check(predicate)


def is_admin():
    async def predicate(ctx):
        if ctx.author.id not in ctx.bot.config.owners and ctx.author.id not in ctx.bot.config.admins:
            raise commands.NotOwner()
        else:
            return True

    return commands.check(predicate)

def is_patron():
    async def predicate(ctx):
        guild = ctx.bot.get_guild(725303414220914758)
        can=0
        if ctx.author.id in [g.id for g in guild.members]:
            patron1 = discord.utils.find(lambda r: r.id == ctx.bot.config.patron1, guild.roles)
            patron2 = discord.utils.find(lambda r: r.id == ctx.bot.config.patron2, guild.roles)
            patron3 = discord.utils.find(lambda r: r.id == ctx.bot.config.patron3, guild.roles)
            member = guild.get_member(ctx.author.id)
            if patron1 in member.roles:
                can=1
            if patron2 in member.roles:
                can=1
            if patron3 in member.roles:
                can=1
        if can:
            return True 
        else:
            await ctx.send(embed=discord.Embed(
                description=f"You do not have access to this command, as it is a premium only command. More information is available with the `{ctx.prefix}donate` command.",
                colour=ctx.bot.config.primary_colour
            ))
            return False 

    return commands.check(predicate)
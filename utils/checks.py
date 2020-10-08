from discord.ext import commands


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


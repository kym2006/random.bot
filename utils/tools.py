async def get_prefix(bot, guild):
    if not guild:
        return bot.config.default_prefix
    try:
        prefix = bot.all_prefix[guild.id]
        return bot.config.default_prefix if prefix is None else prefix
    except KeyError:
        return bot.config.default_prefix


def perm_format(perm):
    return perm.replace("_", " ").replace("guild", "server").title()

def get_prefix(bot, guild):
    if not guild:
        return bot.config.default_prefix
    try:
        prefix = bot.all_prefix[guild.id]
        return bot.config.default_prefix if prefix is None else prefix
    except KeyError:
        return bot.config.default_prefix

def get_cd(bot, guild, cmd):
    try:
        cd = bot.cooldown[guild][cmd]
        return 0 if cd is None else cd
    except KeyError:
        return 0



def perm_format(perm):
    return perm.replace("_", " ").replace("guild", "server").title()

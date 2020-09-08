import logging
import platform

import discord
import psutil
import datetime
from discord.ext import commands

log = logging.getLogger(__name__)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(
            title="Server Join",
            description=f"{guild.name} ({guild.id}): {guild.member_count} members",
            colour=discord.Colour.green(),
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_footer(text=f"{len(self.bot.guilds)} servers, {len(self.bot.users)} users")
        await self.bot.http.send_message(725303414916907043, None, embed=embed.to_dict())
        await self.bot.change_presence(activity=discord.Game("@help | @someone | being random on {} servers".format(len(self.bot.guilds))))
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(
            title="Server Leave",
            description=f"{guild.name} ({guild.id})",
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_footer(text=f"{len(self.bot.guilds)} servers, {len(self.bot.users)} users")
        await self.bot.http.send_message(725303414916907043, None, embed=embed.to_dict())      
        await self.bot.change_presence(activity=discord.Game("@help | @someone | being random on {} servers".format(len(self.bot.guilds))))


def setup(bot):
    bot.add_cog(Events(bot))

import datetime
import logging
import platform

import discord
import psutil
from discord.ext import commands

log = logging.getLogger(__name__)


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"@help | @someone on {len(self.bot.guilds)} servers"
            )
        )

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
        await self.bot.change_presence(
            activity=discord.Game("@help | @someone | being random on {} servers".format(len(self.bot.guilds)))
        )
        txtchannel = self.bot.get_channel(725303414363390018)
        for i in guild.channels:
            if i.type == txtchannel.type:
                try:
                    await i.send(
                        """Thank you for inviting random.bot! Join our support server at https://discord.gg/ZatYnsX for monthly giveaways!
Type @help to view all commands! 
Type @leaderboard to see who's the richest users for random.bot! Note that the richer you are, the more likely you are to be chosen for the giveaway!
Type @prefix to change the prefix."""
                    )
                    return
                except:
                    continue

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(
            title="Server Leave",
            description=f"{guild.name} ({guild.id}): {guild.member_count} members",
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_footer(text=f"{len(self.bot.guilds)} servers, {len(self.bot.users)} users")
        await self.bot.http.send_message(725303414916907043, None, embed=embed.to_dict())
        await self.bot.change_presence(
            activity=discord.Game("@help | @someone | being random on {} servers".format(len(self.bot.guilds)))
        )


def setup(bot):
    bot.add_cog(Events(bot))

import datetime
import logging

import discord

from discord.ext import commands

log = logging.getLogger(__name__)


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        embed = discord.Embed(
            title="Bot Ready",
            colour=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        await self.bot.http.send_message(self.bot.config.event_channel, None, embed=embed.to_dict())
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"@help | @someone on {len(self.bot.guilds)} servers"
            )
        )

    @commands.Cog.listener()
    async def on_shard_ready(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Ready",
            colour=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        await self.bot.http.send_message(self.bot.config.event_channel, None, embed=embed.to_dict())

    @commands.Cog.listener()
    async def on_shard_connect(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Connected",
            colour=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        await self.bot.http.send_message(self.bot.config.event_channel, None, embed=embed.to_dict())

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Disconnected",
            colour=0xFF0000,
            timestamp=datetime.datetime.utcnow(),
        )
        await self.bot.http.send_message(self.bot.config.event_channel, None, embed=embed.to_dict())

    @commands.Cog.listener()
    async def on_shard_resumed(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Resumed",
            colour=self.bot.config.primary_colour,
            timestamp=datetime.datetime.utcnow(),
        )
        await self.bot.http.send_message(self.bot.config.event_channel, None, embed=embed.to_dict())

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(
            title="Server Join",
            description=f"{guild.name} ({guild.id}): {guild.member_count} members",
            colour=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        guilds = len(self.bot.guilds)
        embed.set_footer(text=f"{guilds} servers")
        await self.bot.http.send_message(self.bot.config.join_channel, None, embed=embed.to_dict())
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"@help | @someone on {len(self.bot.guilds)} servers"
            )
        )
        
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(
            title="Server Leave",
            description=f"{guild.name} ({guild.id}): {guild.member_count} members",
            colour=0xFF0000,
            timestamp=datetime.datetime.utcnow(),
        )
        guilds = len(self.bot.guilds)
        embed.set_footer(text=f"{guilds} servers")
        await self.bot.http.send_message(self.bot.config.join_channel, None, embed=embed.to_dict())
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"@help | @someone on {len(self.bot.guilds)} servers"
            )
        )

def setup(bot):
    bot.add_cog(Events(bot))
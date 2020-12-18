import datetime
import logging

import discord
from discord.ext import commands

log = logging.getLogger(__name__)


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if str(ctx.command) in self.bot.down_commands:
            await ctx.send(embed=discord.Embed(description="That command is down right now. Join the [support server](https://discord.gg/ZatYnsX) and read the announcements to find out why. We are already working on a fix :)"))
            return 
        if ctx.command.cog_name in ["Owner", "Admin"] and (
            ctx.author.id in self.bot.config.admins or ctx.author.id in self.bot.config.owners
            ):
            embed = discord.Embed(
                title=ctx.command.name.title(),
                description=ctx.message.content,
                colour=self.bot.primary_colour,
                timestamp=datetime.datetime.utcnow(),
            )
            embed.set_author(name=f"{ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar_url)

            await self.bot.get_channel(self.bot.config.admin_channel).send(embed=embed)
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
                type=discord.ActivityType.watching, name=f"?help | random on {len(self.bot.guilds)} servers"
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
        await self.bot.get_channel(self.bot.config.join_channel).send(embed=embed)
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"?help | ?someone on {len(self.bot.guilds)} servers"
            )
        )
        txtchannel = self.bot.get_channel(self.bot.config.join_channel)
        for i in guild.channels:
            if i.type == txtchannel.type:
                try:
                    await i.send(
                        embed=discord.Embed(
                            description="""Thank you for inviting random.bot! Join our support server at https://discord.gg/ZatYnsX if you need help.
The default prefix for the bot is ?, but you can change it with the prefix command.
Type ?commands for a brief menu of all the commands, or ?help for a more detailed version.""",
                            colour=self.bot.primary_colour,
                        )
                    )
                    return
                except:
                    continue

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
                type=discord.ActivityType.watching, name=f"?help | ?someone on {len(self.bot.guilds)} servers"
            )
        )
    


def setup(bot):
    bot.add_cog(Events(bot))

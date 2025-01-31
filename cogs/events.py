import datetime
import logging

import discord
from discord.ext import commands
import random 
log = logging.getLogger(__name__)


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        ctx = await self.bot.get_context(message)
        if not ctx.command:
            return
        if message.guild:
            permissions = message.channel.permissions_for(message.guild.me)
            if permissions.send_messages is False:
                return
            elif permissions.embed_links is False:
                await message.channel.send("The Embed Links permission is needed for basic commands to work.")
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
            if self.bot.config.admin_channel:
                await self.bot.fetch_channel(self.bot.config.admin_channel).send(embed=embed.to_dict())
        
        
        
        await self.bot.invoke(ctx)

    '''
    @commands.Cog.listener()
    async def on_command(self, ctx):
        if str(ctx.command) in self.bot.down_commands:
            await ctx.response.send_message(embed=discord.Embed(description="That command is down right now. Join the [support server](https://discord.gg/ZatYnsX) and read the announcements to find out why. We are already working on a fix :)"))
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
    '''
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.tree.copy_global_to(guild=(await self.bot.fetch_guild(725303414220914758)))
        await self.bot.tree.sync(guild=(await self.bot.fetch_guild(725303414220914758)))
        embed = discord.Embed(
            title="Bot Ready",
            colour=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        
        await (await self.bot.fetch_channel(self.bot.config.event_channel)).send(embed=embed)
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"Consider donating with /donate!",
            )
        )

    @commands.Cog.listener()
    async def on_shard_ready(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Ready",
            colour=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        c = await self.bot.fetch_channel(self.bot.config.event_channel)
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_shard_connect(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Connected",
            colour=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        c = await self.bot.fetch_channel(self.bot.config.event_channel)
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Disconnected",
            colour=0xFF0000,
            timestamp=datetime.datetime.utcnow(),
        )
        c = await self.bot.fetch_channel(self.bot.config.event_channel)
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_shard_resumed(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Resumed",
            colour=self.bot.config.primary_colour,
            timestamp=datetime.datetime.utcnow(),
        )
        c = await self.bot.fetch_channel(self.bot.config.event_channel)
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        content = f"New guild: {guild.name}! Now at **{len(self.bot.guilds)}** guilds!"
        c = await self.bot.fetch_channel(self.bot.config.join_channel)
        await c.send(content=content, allowed_mentions=discord.AllowedMentions.none())
        txtchannel = await self.bot.fetch_channel(self.bot.config.join_channel)
        await guild.chunk()
        for i in guild.channels:
            if i.type == txtchannel.type:
                try:
                    await i.send(
                        embed=discord.Embed(
                            description="""Thank you for inviting random.bot! Join our support server at https://discord.gg/ZatYnsX if you need help.
Type /help for a menu of all the commands. If you enjoy using the bot, consider [donating](https://ko-fi.com/ktxdym)""",
                            colour=self.bot.primary_colour,
                        )
                    )
                    return
                except:
                    continue

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        content = f"Guild leave: {guild.name}... Now at **{len(self.bot.guilds)}** guilds"
        c = await self.bot.fetch_channel(self.bot.config.join_channel)
        await c.send(content=content,allowed_mentions=discord.AllowedMentions.none())

    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction, command):
        content = f"{interaction.user} used {command.name} {interaction.data}"
        c = await self.bot.fetch_channel(1018037359691960390)
        await c.send(content=content,allowed_mentions=discord.AllowedMentions.none())


async def setup(bot):
    await bot.add_cog(Events(bot))

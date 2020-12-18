import logging
from typing import Optional

import discord
from discord.ext import commands

from classes import converters
from utils import checks
from utils.paginator import Paginator

log = logging.getLogger(__name__)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_admin()
    @commands.command(
        description="Get a list of servers with the specified name.",
        usage="findserver [member count] <name>",
        hidden=True,
    )
    async def findserver(self, ctx, count: Optional[bool], *, name: str):

        guilds = []
        for guild in self.bot.guilds:
            if guild.name.lower().count(name.lower()) > 0:
                guilds.append(guild)
        if count:
            guilds = [f"{guild.name} `{guild.id}` ({guild.member_count} members)" for guild in guilds]
        else:
            guilds = [f"{guild.name} `{guild.id}`" for guild in guilds]
        if len(guilds) == 0:
            await ctx.send(embed=discord.Embed(description="No such guild was found.", colour=self.bot.error_colour))
            return
        all_pages = []
        for chunk in [guilds[i : i + 20] for i in range(0, len(guilds), 20)]:
            page = discord.Embed(title="Servers", colour=self.bot.primary_colour)
            for guild in chunk:
                if page.description == discord.Embed.Empty:
                    page.description = guild
                else:
                    page.description += f"\n{guild}"
            page.set_footer(text="Use the reactions to flip pages.")
            all_pages.append(page)
        if len(all_pages) == 1:
            embed = all_pages[0]
            embed.set_footer(text=discord.Embed.Empty)
            await ctx.send(embed=embed)
            return
        paginator = Paginator(length=1, entries=all_pages, use_defaults=True, embed=True, timeout=120)
        await paginator.start(ctx)

    @checks.is_owner()
    @commands.command(name="sharedservers")
    async def sharedservers(self, ctx, user: int):
        user = self.bot.get_user(user)
        count = 1
        guilds = []
        for i in self.bot.guilds:
            for j in i.members:
                if j.id == user.id:
                    guilds.append(i)
                    continue
        if count:
            guilds = [f"{guild.name} `{guild.id}` ({guild.member_count} members)" for guild in guilds]
        else:
            guilds = [f"{guild.name} `{guild.id}`" for guild in guilds]
        all_pages = []
        for chunk in [guilds[i : i + 20] for i in range(0, len(guilds), 20)]:
            page = discord.Embed(title="Servers", colour=self.bot.primary_colour)
            for guild in chunk:
                if page.description == discord.Embed.Empty:
                    page.description = guild
                else:
                    page.description += f"\n{guild}"
            page.set_footer(text="Use the reactions to flip pages.")
            all_pages.append(page)
        if len(all_pages) == 1:
            embed = all_pages[0]
            embed.set_footer(text=discord.Embed.Empty)
            await ctx.send(embed=embed)
            return
        paginator = Paginator(length=1, entries=all_pages, use_defaults=True, embed=True, timeout=120)
        await paginator.start(ctx)

    @checks.is_admin()
    @commands.command(
        description="View invites of specified server.",
        usage="viewinvites <server ID>",
        hidden=True,
    )
    async def viewinvites(self, ctx, *, guild_id: int):
        guild = self.bot.get_guild(guild_id)
        try:
            invite = (await guild.invites())[0]
            await ctx.send(f"Here is the invite link: https://discord.gg/{invite[0]['code']}")
        except Exception:
            await ctx.send("Cannot be done")

    @checks.is_admin()
    @commands.command(
        description="Create an invite to the specified server.",
        usage="createinvite <server ID>",
        hidden=True,
    )
    async def createinvite(self, ctx, *, guild: converters.GlobalGuild):
        try:
            invite = (await guild.invites())[0]
        except (IndexError, discord.Forbidden):
            try:
                invite = await guild.text_channels[0].create_invite(max_age=120)
            except discord.Forbidden:
                pass
        if not invite:
            await ctx.send(
                embed=discord.Embed(
                    description="No permissions to create an invite link.",
                    colour=self.bot.primary_colour,
                )
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    description=f"Here is the invite link: https://discord.gg/{invite[0]['code']}",
                    colour=self.bot.primary_colour,
                )
            )

    @checks.is_admin()
    @commands.command(
        description="Get the top servers using the bot.",
        aliases=["topguilds"],
        usage="topservers [count]",
        hidden=True,
    )
    async def topservers(self, ctx, *, count: int = 20):
        guilds = self.bot.guilds
        guilds = sorted(guilds, key=lambda x: x.member_count, reverse=True)[:count]
        top_guilds = []
        for index, guild in enumerate(guilds):
            top_guilds.append(f"#{index + 1} {guild.name} `{guild.id}` ({guild.member_count} members)")
        all_pages = []
        for chunk in [top_guilds[i : i + 20] for i in range(0, len(top_guilds), 20)]:
            page = discord.Embed(title="Top Servers", colour=self.bot.primary_colour)
            for guild in chunk:
                if page.description == discord.Embed.Empty:
                    page.description = guild
                else:
                    page.description += f"\n{guild}"
            page.set_footer(text="Use the reactions to flip pages.")
            all_pages.append(page)
        if len(all_pages) == 1:
            embed = all_pages[0]
            embed.set_footer(text=discord.Embed.Empty)
            await ctx.send(embed=embed)
            return
        paginator = Paginator(length=1, entries=all_pages, use_defaults=True, embed=True, timeout=120)
        await paginator.start(ctx)

    @checks.is_admin()
    @commands.command(description="Make me say something.", usage="echo [channel] <message>", hidden=True)
    async def echo(self, ctx, channel: Optional[discord.TextChannel], *, content: str):
        channel = channel or ctx.channel
        await ctx.message.delete()
        await channel.send(content, allowed_mentions=discord.AllowedMentions(everyone=False))


def setup(bot):
    bot.add_cog(Admin(bot))

import logging
import platform

import discord
import psutil

from discord.ext import commands
from utils.paginator import Paginator

log = logging.getLogger(__name__)


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(add_reactions=True)
    @commands.command(
        description="Shows the help menu or information for a specific command when specified.",
        usage="help [command]",
        aliases=["h", "commands"],
    )
    async def help(self, ctx, *, command: str = None):
        if command:
            command = self.bot.get_command(command.lower())
            if not command:
                await ctx.send(
                    embed=discord.Embed(
                        description=f"That command does not exist. Use `{ctx.prefix}help` to see all the commands.",
                        colour=self.bot.primary_colour,
                    )
                )
                return
            embed = discord.Embed(title=command.name, description=command.description, colour=self.bot.primary_colour)
            usage = "\n".join([ctx.prefix + x.strip() for x in command.usage.split("\n")])
            embed.add_field(name="Usage", value=f"```{usage}```", inline=False)
            if len(command.aliases) > 1:
                embed.add_field(name="Aliases", value=f"`{'`, `'.join(command.aliases)}`")
            elif len(command.aliases) > 0:
                embed.add_field(name="Alias", value=f"`{command.aliases[0]}`")
            await ctx.send(embed=embed)
            return
        all_pages = []
        page = discord.Embed(
            title=f"{self.bot.user.name} Help Menu",
            description="Thank you for using Random.bot! Please direct message me if you wish to contact staff. You can "
            "also invite me to your server with the link below, or join our support server if you need further help."
            f"\n\nDon't forget to check out our partners with the `{ctx.prefix}partners` command!",
            colour=self.bot.primary_colour,
        )
        page.set_thumbnail(url=self.bot.user.avatar_url)
        page.set_footer(text="Use the reactions to flip pages. Help menu made by: CHamburr#2591(Thank you!)")
        page.add_field(
            name="Invite",
            value=f"https://discordapp.com/api/oauth2/authorize?client_id={self.bot.user.id}"
            "&permissions=134150&scope=bot",
            inline=False,
        )
        page.add_field(name="Support Server", value="https://discord.gg/ZatYnsX", inline=False)
        all_pages.append(page)
        page = discord.Embed(title=f"{self.bot.user.name} Help Menu", colour=self.bot.primary_colour)
        page.set_thumbnail(url=self.bot.user.avatar_url)
        page.set_footer(text="Use the reactions to flip pages.")
        page.add_field(
            name="About Random.bot",
            value="Random.bot provides convenient, random randomness in your server.",
            inline=False,
        )
        page.add_field(
            name="Getting Started",
            value="Follow these steps to get the bot all ready to serve your server!\n1. Invite the bot with "
            f"[this link](https://discord.com/oauth2/authorize?client_id=606402391314530319&scope=bot&permissions=134150)\n2."
            f"\n3. All done! For a full list of commands, see `{ctx.prefix}help`.",
            inline=False,
        )
        all_pages.append(page)
        for _, cog_name in enumerate(self.bot.cogs):
            if cog_name in ["Owner", "Admin"]:
                continue
            cog = self.bot.get_cog(cog_name)
            cog_commands = cog.get_commands()
            if len(cog_commands) == 0:
                continue
            page = discord.Embed(
                title=cog_name,
                description=f"My prefix is `{ctx.prefix}`. Use `{ctx.prefix}"
                "help <command>` for more information on a command.",
                colour=self.bot.primary_colour,
            )
            page.set_author(name=f"{self.bot.user.name} Help Menu", icon_url=self.bot.user.avatar_url)
            page.set_thumbnail(url=self.bot.user.avatar_url)
            page.set_footer(text="Use the reactions to flip pages.")
            for cmd in cog_commands:
                if cmd.hidden is False:
                    page.add_field(name=cmd.name, value=cmd.description, inline=False)
            all_pages.append(page)
        paginator = Paginator(length=1, entries=all_pages, use_defaults=True, embed=True, timeout=120)
        await paginator.start(ctx)

    @commands.command(description="Pong! Get my latency.", usage="ping")
    async def ping(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="Pong!",
                description=f"My current latency is {round(self.bot.latency * 1000, 2)}ms.",
                colour=self.bot.primary_colour,
            )
        )

    def get_bot_uptime(self, *, brief=False):
        hours, remainder = divmod(int(self.bot.uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        if not brief:
            if days:
                fmt = "{d} days, {h} hours, {m} minutes, and {s} seconds"
            else:
                fmt = "{h} hours, {m} minutes, and {s} seconds"
        else:
            fmt = "{h}h {m}m {s}s"
            if days:
                fmt = "{d}d " + fmt
        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    @commands.command(
        description="See some super cool statistics about me.",
        usage="stats",
        aliases=["statistics", "info"],
    )
    async def stats(self, ctx):
        guilds = sum(await self.bot.cogs["Communication"].handler("guild_count", self.bot.cluster_count))
        channels = sum(await self.bot.cogs["Communication"].handler("channel_count", self.bot.cluster_count))
        users = sum(await self.bot.cogs["Communication"].handler("user_count", self.bot.cluster_count))

        embed = discord.Embed(title=f"{self.bot.user.name} Statistics", colour=self.bot.primary_colour)
        embed.add_field(name="Owner", value="CHamburr#2591")
        embed.add_field(name="Bot Version", value=self.bot.version)
        embed.add_field(name="Uptime", value=self.get_bot_uptime(brief=True))
        embed.add_field(name="Clusters", value=f"{self.bot.cluster}/{self.bot.cluster_count}")
        if ctx.guild:
            embed.add_field(name="Shards", value=f"{ctx.guild.shard_id + 1}/{self.bot.shard_count}")
        else:
            embed.add_field(name="Shards", value=f"{self.bot.shard_count}")
        embed.add_field(name="Servers", value=str(guilds))
        embed.add_field(name="Channels", value=str(channels))
        embed.add_field(name="Users", value=str(users))
        embed.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%")
        embed.add_field(name="RAM Usage", value=f"{psutil.virtual_memory().percent}%")
        embed.add_field(name="Python Version", value=platform.python_version())
        embed.add_field(name="discord.py Version", value=discord.__version__)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(
            text="Made with ❤ using discord.py",
            icon_url="https://www.python.org/static/opengraph-icon-200x200.png",
        )
        await ctx.send(embed=embed)

    @commands.command(description="Get a link to invite me.", usage="invite")
    async def invite(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="Invite Link",
                description=f"https://discord.com/oauth2/authorize?client_id=606402391314530319&scope=bot&permissions=134150",
                colour=self.bot.primary_colour,
            )
        )

    @commands.command(description="Get a link to my support server.", usage="support", aliases=["server"])
    async def support(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="Support Server",
                description="https://discord.gg/ZatYnsX",
                colour=self.bot.primary_colour,
            )
        )

    @commands.command(description="Get the link to ModMail's website.", usage="website")
    async def website(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="Website",
                description=f"https://randomweb.netlify.app/",
                colour=self.bot.primary_colour,
            )
        )

    @commands.command(description="Usage statistics of the bot.", usage="usagestats", hidden=True)
    async def usagestats(self, ctx):
        embed = discord.Embed(
            title="Usage Statistics",
            description="Bot usage statistics since 1 January 2020.",
            colour=self.bot.primary_colour,
        )
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetchrow("SELECT commands, messages, tickets FROM stats")
        embed.add_field(name="Total commands", value=str(res[0]), inline=False)
        embed.add_field(name="Total messages", value=str(res[1]), inline=False)
        embed.add_field(name="Total tickets", value=str(res[2]), inline=False)
        await ctx.send(embed=embed)

    @commands.command(
        description="Get the top 15 servers using this bot.",
        aliases=["topguilds"],
        usage="topservers",
        hidden=True,
    )
    async def topservers(self, ctx):
        data = self.bot.guilds 
        guilds = []
        for chunk in data:
            guilds.extend(chunk)
        guilds = sorted(guilds, key=lambda x: x["member_count"], reverse=True)[:15]
        top_guilds = []
        for index, guild in enumerate(guilds):
            top_guilds.append(f"#{str(index + 1)} {guild['name']} ({guild['member_count']} members)")
        await ctx.send(
            embed=discord.Embed(
                title="Top 15 Servers",
                description="\n".join(top_guilds),
                colour=self.bot.primary_colour,
            )
        )


def setup(bot):
    bot.add_cog(General(bot))


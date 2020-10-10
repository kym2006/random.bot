import logging
import platform
import time

import aiohttp
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
        aliases=["h"],
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
            embed = discord.Embed(
                title=command.name,
                description=command.description,
                colour=self.bot.primary_colour,
            )
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
            description="Thank you for using Random.bot! You can "
            "also invite me to your server with the link below, or join our support server if you need further help."
            f"\n\nDon't forget to check out our partners with the `{ctx.prefix}partners` command!",
            colour=self.bot.primary_colour,
        )
        page.set_thumbnail(url=self.bot.user.avatar_url)
        page.set_footer(text="Use the reactions to flip pages. Help menu from CHamburr#2591(Thank you!)")
        page.add_field(
            name="Invite",
            value=f"https://discord.com/oauth2/authorize?client_id=606402391314530319&scope=bot&permissions=314374"
            + "&permissions=314374&scope=bot\nKudos to you if you don't leave within a minute.",
            inline=False,
        )
        page.add_field(name="Support Server", value="https://invite.gg/randombot", inline=False)
        all_pages.append(page)
        page = discord.Embed(
            title=f"Commands Menu",
            description="See all commmands briefly, use flip pages to see the more detailed versions.",
            colour=self.bot.primary_colour,
        )
        page.set_thumbnail(url=self.bot.user.avatar_url)
        page.set_thumbnail(url=self.bot.user.avatar_url)
        for _, cog_name in enumerate(self.bot.cogs):
            if cog_name in ["Owner", "Admin"]:
                continue
            cog = self.bot.get_cog(cog_name)
            cog_commands = cog.get_commands()
            if len(cog_commands) == 0:
                continue
            cmds = "```\n"
            for cmd in cog_commands:
                if cmd.hidden is False:
                    cmds += cmd.name + "\n"
            cmds += "```"
            page.add_field(name=cog_name, value=cmds)
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
            page.set_author(
                name=f"{self.bot.user.name} Help Menu",
                icon_url=self.bot.user.avatar_url,
            )
            page.set_thumbnail(url=self.bot.user.avatar_url)
            page.set_footer(text="Use the reactions to flip pages.")
            for cmd in cog_commands:
                if cmd.hidden is False:
                    page.add_field(name=cmd.name, value=cmd.description, inline=False)
            all_pages.append(page)
        paginator = Paginator(length=1, entries=all_pages, use_defaults=True, embed=True, timeout=120)
        await paginator.start(ctx)

    @commands.command(description="Shows brief help menu", usage="commands", name="commands")
    async def _commands(self, ctx):
        page = discord.Embed(
            title=f"{self.bot.user.name} Commands Menu",
            description="See all commmands brief, use @help to see the more detailed versions.",
            colour=self.bot.primary_colour,
        )
        page.set_thumbnail(url=self.bot.user.avatar_url)
        page.add_field(
            name="Invite",
            value=f"[Invite Link](https://discord.com/oauth2/authorize?client_id=606402391314530319&scope=bot&permissions=314374)",
        )
        page.add_field(name="Support Server", value="https://invite.gg/randombot", inline=False)
        page.set_thumbnail(url=self.bot.user.avatar_url)
        for _, cog_name in enumerate(self.bot.cogs):
            if cog_name in ["Owner", "Admin"]:
                continue
            cog = self.bot.get_cog(cog_name)
            cog_commands = cog.get_commands()
            if len(cog_commands) == 0:
                continue
            cmds = "```\n"
            for cmd in cog_commands:
                if cmd.hidden is False:
                    cmds += cmd.name + "\n"
            cmds += "```"
            page.add_field(name=cog_name, value=cmds)

        await ctx.send(embed=page)

    @commands.command(description="post a command")
    async def posthuggin(self, ctx, *, content: str):
        async with aiohttp.ClientSession() as session:
            await session.post(
                "https://huginn.chamburr.xyz/users/1/web_requests/12/ae7cf81ab0f456972fb91ce8dc4c5d46",
                data={"content": content},
            )

    @commands.command(description="Look at my partners", usage="partners")
    async def partners(self, ctx):

        all_pages = []
        page = discord.Embed(
            title="Snippet",
            description="Snippet is a bot designed to help you easily store and retrieve something in discord. You can use this bot to store copypasta, store music, display faq, and many more. Invite it with https://discordapp.com/oauth2/authorize?client_id=726673431143383090&scope=bot&permissions=11328",
            colour=self.bot.primary_colour,
        )
        page.add_field(name="Website", value="https://snippetsite.netlify.app")
        page.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/726673431143383090/bd4e791fbfc8f7cd7662a281989c15f4.png"
        )
        all_pages.append(page)
        paginator = Paginator(length=1, entries=all_pages, use_defaults=True, embed=True, timeout=120)
        await paginator.start(ctx)

    @commands.command(description="Pong! Get my latency.", usage="ping")
    async def ping(self, ctx):
        start = time.time()
        msg = await ctx.send(embed=discord.Embed(description="Checking latency...", colour=self.bot.primary_colour))
        await msg.edit(
            embed=discord.Embed(
                title="Pong!",
                description=f"Gateway latency: {round(self.bot.latency * 1000, 2)}ms.\n"
                f"HTTP API latency: {round((time.time() - start) * 1000, 2)}ms.",
                colour=self.bot.primary_colour,
            )
        )

    @commands.command(description="Support random.bot!", usage="donate")
    async def donate(self, ctx):
        embed = discord.Embed(title="Looking to donate?", description="As the bot grows, so must our hosting servers. Please support us for us to get better hosting, and motivating us to spend more time developing the bot! Here's [the link](https://paypal.me/waterflamev8).")

        embed.add_field(name="Snippet storage space", value="Patrons get additional storage space for snippets\nPatrons: 20000\nSuper patrons: 50000\nSuper duper patrons: 100000")
        embed.add_field(name="Priority support", value="If you are a patron, we would definitely support you first! (Then again, support for our normal members are rather fast as well) :)")
        embed.add_field(name="Test beta features", value="Beta features will be released to patrons exclusively in the development phase :)")
        embed.add_field(name="Other patrons exclusive features", value="More features are on the way, stay tuned for that!")

        await ctx.send(embed=embed)
    

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
        guilds = len(self.bot.guilds)
        users = len(self.bot.users)
        channels = sum([len(g.channels) for g in self.bot.guilds])
        embed = discord.Embed(title=f"{self.bot.user.name} Statistics", colour=self.bot.primary_colour)
        embed.add_field(
            name="Owners",
            value="kym2006#6342, SquiddyPoos#6795, waterflamev8#4123",
        )
        embed.add_field(name="Bot Version", value=self.bot.version)
        embed.add_field(name="Uptime", value=self.get_bot_uptime(brief=True))
        # embed.add_field(name="Clusters", value=f"{self.bot.cluster}/{self.bot.cluster_count}")
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
        embed.add_field(name="Statcord", value="https://statcord.com/bot/606402391314530319")
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
                description=f"https://discord.com/oauth2/authorize?client_id=606402391314530319&scope=bot&permissions=314374",
                colour=self.bot.primary_colour,
            )
        )

    @commands.command(
        description="Get a link to my support server.",
        usage="support",
        aliases=["server"],
    )
    async def support(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="Support Server",
                description="https://invite.gg/randombot",
                colour=self.bot.primary_colour,
            )
        )

    @commands.command(description="Get the link to Random.bot's website.", usage="website")
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


def setup(bot):
    bot.add_cog(General(bot))

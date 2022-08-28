import logging
import platform
import time
from typing import Optional
from discord import app_commands

import discord
import psutil
from discord.ext import commands
#from paginator import Paginator, Page, NavigationType
from utils.paginator import Paginator

log = logging.getLogger(__name__)


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.paginator = Paginator(bot)


    '''@commands.command(
        description="Shows the help menu or information for a specific command when specified.",
        usage="help [command]",
        aliases=["h"],
    )'''
    @app_commands.command(name="help",description="Shows the help menu or information for a specific command when specified.")
    async def help(self, ctx, *, command: str = None):
        if command:
            try:
                command = self.bot.tree.get_command(command.lower())
            except:
                command = self.bot.get_command((command.lower()))
            if not command:
                await ctx.response.send_message(
                    embed=discord.Embed(
                        description=f"That command does not exist. Use `/help` to see all the commands.",
                        colour=self.bot.primary_colour,
                    )
                )
                return
            embed = discord.Embed(
                title=command.name,
                description=command.description,
                colour=self.bot.primary_colour,
            )
            await ctx.response.send_message(embed=embed)
            return

        page = discord.Embed(
            title=f"{self.bot.user.name} Commands Menu",
            description="See all commmands brief, use /help to see the more detailed versions.",
            colour=self.bot.primary_colour,
        )
        page.set_thumbnail(url=self.bot.user.avatar)
        page.add_field(
            name="Invite",
            value=f"[Invite Link](https://discord.com/oauth2/authorize?client_id=606402391314530319&permissions=268823640&scope=bot+applications.commands)",
        )
        page.add_field(name="Support Server", value="https://discord.gg/ZatYnsX", inline=False)
        page.add_field(name="Donate", value="https://paypal.me/kym2k06", inline=False)
        page.set_thumbnail(url=self.bot.user.avatar)
        for _, cog_name in enumerate(self.bot.cogs):
            if cog_name in ["Owner", "Admin"]:
                continue
            cog = self.bot.get_cog(cog_name)
            cog_commands = cog.get_app_commands()
            if len(cog_commands) == 0:
                continue
            cmds = "```\n"
            for cmd in cog_commands:
                cmds += cmd.name + "\n"
            cmds += "```"
            if cog_name == "More":
                cog_name = "Random 2.0"
            page.add_field(name=cog_name, value=cmds)

        await ctx.response.send_message(embed=page)
        '''
        all_pages = []
        page = discord.Embed(
            title=f"{self.bot.user.name} Help Menu",
            description="Thank you for using Random.bot! You can "
            "also invite me to your server with the link below, or join our support server if you need further help."
            f"\n\nDon't forget to check out our partners with the `/partners` command!",
            colour=self.bot.primary_colour,
        )
        page.set_thumbnail(url=self.bot.user.avatar)
        page.add_field(
            name="Invite",
            value="https://discord.com/oauth2/authorize?client_id=606402391314530319&permissions=268823640&scope=bot+applications.commands",
            inline=False,
        )
        page.add_field(name="Support Server", value="https://discord.gg/ZatYnsX", inline=False)
        all_pages.append(page)
        page = discord.Embed(
            title="Commands Menu",
            description="See all commmands briefly, use flip pages to see the more detailed versions.",
            colour=self.bot.primary_colour,
        )
        page.set_thumbnail(url=self.bot.user.avatar)
        page.set_thumbnail(url=self.bot.user.avatar)
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
            if cog_name == "More":
                cog_name = "Random 2.0"
            page.add_field(name=cog_name, value=cmds)
        all_pages.append(page)
        for _, cog_name in enumerate(self.bot.cogs):
            if cog_name in ["Owner", "Admin"]:
                continue
            cog = self.bot.get_cog(cog_name)
            cog_commands = cog.get_commands()
            if len(cog_commands) == 0:
                continue
            if cog_name == "More":
                cog_name = "Random 2.0"
            page = discord.Embed(
                title=cog_name,
                description=f"My prefix is `/`. Use `/"
                "help <command>` for more information on a command.",
                colour=self.bot.primary_colour,
            )
            page.set_author(
                name=f"{self.bot.user.name} Help Menu",
                icon_url=self.bot.user.avatar,
            )
            page.set_thumbnail(url=self.bot.user.avatar)
            page.set_footer(text="Use the reactions to flip pages.")
            for cmd in cog_commands:
                if cmd.hidden is False:
                    page.add_field(name=cmd.name, value=cmd.description, inline=False)
            all_pages.append(page)
        
        paginator = Paginator(length=1, entries=all_pages, use_defaults=True, embed=True, timeout=120)
        await paginator.start(ctx)
        '''

    @commands.command(description="Shows brief help menu", usage="commands", name="commands")
    async def _commands(self, ctx):
        page = discord.Embed(
            title=f"{self.bot.user.name} Commands Menu",
            description="See all commmands brief, use ?help to see the more detailed versions.",
            colour=self.bot.primary_colour,
        )
        page.set_thumbnail(url=self.bot.user.avatar)
        page.add_field(
            name="Invite",
            value=f"[Invite Link](https://discord.com/oauth2/authorize?client_id=606402391314530319&permissions=268823640&scope=bot+applications.commands)",
        )
        page.add_field(name="Support Server", value="https://discord.gg/ZatYnsX", inline=False)
        page.add_field(name="Donate", value="https://paypal.me/kym2k06", inline=False)
        page.set_thumbnail(url=self.bot.user.avatar)
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
            if cog_name == "More":
                cog_name = "Random 2.0"
            page.add_field(name=cog_name, value=cmds)

        await ctx.response.send_message(embed=page)
    '''
    @commands.command(description="Suggest a feature!", name="suggest", usage="suggest")
    async def suggest(self, ctx, *, content: str):
        channel = self.bot.get_channel(766642940323037214)
        embed = discord.Embed(description=content, colour=self.bot.config.primary_colour)
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.avatar_url}")
        await channel.send(embed=embed)

    @commands.command(description="Look at my partners", usage="partners")
    async def partners(self, ctx):
        all_pages = []
        page = discord.Embed(
            title="Snippet",
            description="Snippet is a bot designed to help you easily store and retrieve something in discord. You can use this bot to store copypasta, store music, display faq, and many more. Invite it with https://discord.com/api/oauth2/authorize?client_id=606402391314530319&permissions=526636809431&scope=bot%20applications.commands",
            colour=self.bot.primary_colour,
        )
        page.add_field(name="Website", value="https://snippetsite.netlify.app")
        page.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/726673431143383090/bd4e791fbfc8f7cd7662a281989c15f4.png"
        )
        all_pages.append(page)
        page = discord.Embed(
            title="The Organisation Without A Cool Acronym",
            description="""
        Phineas and Ferb Fan?

        Join our server cause why not?

        **Benefits of joining the server**
        1. Chat with the community of Phineas And Ferb, Milo Murphy’s Law.
        2. Be an Agent, Villain.
        3. Play some music using bot commands of Groovy.
        4. Share memes with the community.
        5. Get to participate in our Monthly Quizzes and have great fun
        6. We have a great Phineas and Ferb Community


        **Our Server Owners**
        Owner - Major Monogram#3339/ Kendall#5259
        Co-Owner - Darth Ferb#8114

        **Our Mod Team**
        Mraxadil#6694
        Candar#1984
        Irving#5978
        Gamer Danger#6896 - Former Server Owner
        snoopy#5026
        Grinch Omar Steals Christmas#0468
        CJKindaBasedThough (Jeff)#6339

        **Our Admins Alts**
        Bradley the part Pistachion#8922
        Candace-2#0714
        Kendall#5259
        Mrax#7677
        ThatOneFanboy#8978

        Make sure you join us today and have great fun.

        Link
        https://discord.gg/nEJ8FMY
        """,
            colour=self.bot.primary_colour,
        )
        page.set_thumbnail(
            url="https://cdn.discordapp.com/icons/754311436104106055/daa2cf48eb68b97db316cea02a580750.webp?size=1024"
        )
        all_pages.append(page)
        paginator = Paginator(length=1, entries=all_pages, use_defaults=True, embed=True, timeout=120)
        await paginator.start(ctx)
    '''
#@commands.command(description="Pong! Get my latency.", usage="ping")
    @app_commands.command(name="ping", description="Pong! Get my latency.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Pong!",
                description=f"Gateway latency: {round(self.bot.latency * 1000, 2)}ms.\n",
                colour=self.bot.primary_colour,
            )
        )
        print(self.bot.tree.get_commands())
    @app_commands.command(name="donate", description="Donate to the bot!")
    async def donate(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Looking to donate? Donate At least 5USD to get the patron role!!",
            description="As the bot grows, so must our hosting servers. Please support us for us to get better hosting, and motivating us to spend more time developing the bot! Here's [the link](https://paypal.me/kym2k06).",
            colour=self.bot.primary_colour,
        )
        embed.add_field(
            inline=False,
            name="Using random.org api functions",
            value=f"Patrons also get access to functions that use the random.org api directly. Run `/org` to view a list of functions that have already been implemented. RANDOM.ORG offers true random numbers to anyone on the Internet. The randomness comes from atmospheric noise, which for many purposes is better than the pseudo-random number algorithms typically used in computer programs. People use RANDOM.ORG for holding drawings, lotteries and sweepstakes, to drive online games, for scientific applications and for art and music. Visit https://random.org to learn more."
        )
        embed.add_field(
            inline=False,
            name="Snippet storage space",
            value="Patrons get additional storage space for snippets\nPatrons: 20000\nSuper patrons: 50000\nSuper duper patrons: 100000",
        )
        embed.add_field(
            inline=False,
            name="Priority support",
            value="If you are a patron, we would definitely support you first! (Then again, support for our normal members are rather fast as well) :)",
        )
        embed.add_field(
            inline=False,
            name="Test beta features",
            value="Beta features will be released to patrons exclusively in the development phase :)",
        )
        embed.add_field(
            inline=False,
            name="Other patrons exclusive features",
            value="More features are on the way, stay tuned for that!",
        )

        await interaction.response.send_message(embed=embed)

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


    @app_commands.command(name="stats", description= "See some cool statistics about me.")
    async def stats(self, ctx):
        guilds = len(self.bot.guilds)
        users = len(self.bot.users)
        channels = sum([len(g.channels) for g in self.bot.guilds])
        embed = discord.Embed(title=f"{self.bot.user.name} Statistics", colour=self.bot.primary_colour)
        embed.add_field(
            name="Owners",
            value="kym#6342\nSquiddyPoos#6795",
        )
        embed.add_field(
            name="Contributers",
            value="waterflamev8#4123",
        )
        embed.add_field(name="Bot Version", value=self.bot.version)
        embed.add_field(name="Uptime", value=self.get_bot_uptime(brief=True))
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
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.add_field(name="Statcord", value="https://statcord.com/bot/606402391314530319")
        embed.set_footer(
            text="</> with ❤ using discord.py",
            icon_url="https://www.python.org/static/opengraph-icon-200x200.png",
        )
        await ctx.response.send_message(embed=embed)

    @app_commands.command(name="invite", description="Get an invite link for the bot.")
    #@commands.command(description="Get a link to invite me.", usage="invite")
    async def invite(self, ctx):
        await ctx.response.send_message(
            embed=discord.Embed(
                title="Invite Link",
                description=f"https://discord.com/oauth2/authorize?client_id=606402391314530319&permissions=268823640&scope=bot+applications.commands",
                colour=self.bot.primary_colour,
            )
        )


    @app_commands.command(name="support", description="Get a link to my support server.")
    async def support(self, ctx):
        await ctx.response.send_message(
            embed=discord.Embed(
                title="Support Server",
                description="https://discord.gg/ZatYnsX",
                colour=self.bot.primary_colour,
            )
        )

    @app_commands.command(name="website", description="Get a link to my website.")
    async def website(self, ctx):
        await ctx.response.send_message(
            embed=discord.Embed(
                title="Website",
                description="https://randomweb.netlify.app/",
                colour=self.bot.primary_colour,
            )
        )

    @app_commands.command(description="Top.gg site for random.bot", name="vote")
    async def vote(self, ctx):
        await ctx.response.send_message(
            embed=discord.Embed(
                title="Vote for random.bot!",
                description="https://top.gg/bot/606402391314530319/vote",
                colour=self.bot.primary_colour,
            )
        )


async def setup(bot):
    await bot.add_cog(General(bot))

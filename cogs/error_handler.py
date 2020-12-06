import logging
import traceback

import discord
from discord.ext import commands

log = logging.getLogger(__name__)


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.on_command_error = self._on_command_error
        self.client = None

    async def get_permissions(self, member, channel):
        permissions = channel.permissions_for(member)
        embed = discord.Embed(
            title=f"Permissions for {member.name}#{member.discriminator}",
            colour=self.bot.primary_colour,
        )
        allowed, denied = [], []
        for name, value in permissions:
            name = self.bot.tools.perm_format(name)
            if value:
                allowed.append(name)
            else:
                denied.append(name)

        embed.add_field(name="Allowed", value="\n".join(allowed))
        embed.add_field(name="Denied", value="\n".join(denied))
        return embed


    async def _on_command_error(self, ctx, error, bypass=False):
        if (
            hasattr(ctx.command, "on_error")
            or (ctx.command and hasattr(ctx.cog, f"_{ctx.command.cog_name}__error"))
            and not bypass
        ):
            return
        if isinstance(error, commands.CommandNotFound):
            return
        if ctx.guild is not None: 
            embed = await self.get_permissions(ctx.guild.me, ctx.channel) 
        else:
            embed = discord.Embed()
        errorchannel = self.bot.get_channel(782156413090529301)
        embed.add_field(
            name="Content", value=f"{ctx.message.content}\n", inline=False 
        )
        embed.add_field(
            name="Author", value=f"{ctx.message.author.id}", inline=False
        )
        
        await errorchannel.send(embed=embed)


        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send(
                embed=discord.Embed(
                    title="Command Unavailable",
                    description="This command cannot be used in Direct Message.",
                    colour=self.bot.error_colour,
                )
            )
        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.send(
                embed=discord.Embed(
                    title="Command Unavailable",
                    description="This command can only be used in Direct Message.",
                    colour=self.bot.error_colour,
                )
            )
        elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="Invalid Arguments",
                description=f"Please check the usage below or join the support server with "
                f"`{ctx.prefix}support` if you don't know what went wrong.",
                colour=self.bot.error_colour,
            )
            usage = "\n".join([ctx.prefix + x.strip() for x in ctx.command.usage.split("\n")])
            embed.add_field(name="Usage", value=f"```{usage}```")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission Denied",
                    description="You do not have permission to use this command.",
                    colour=self.bot.error_colour,
                )
            )
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission Denied",
                    description="You do not have permission to use this command. "
                    f"Permissions needed: {', '.join([self.bot.tools.perm_format(p) for p in error.missing_perms])}",
                    colour=self.bot.error_colour,
                )
            )
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(
                embed=discord.Embed(
                    title="Bot Missing Permissions",
                    description="Bot is missing permissions to perform that action. The following permissions are"
                    f" needed: {', '.join([self.bot.tools.perm_format(p) for p in error.missing_perms])}",
                    colour=self.bot.error_colour,
                )
            )
        elif isinstance(error, discord.HTTPException):
            await ctx.send(
                embed=discord.Embed(
                    title="Unknown HTTP Exception",
                    description=f"Please report this in the support server.\n```{error.text}````",
                    colour=self.bot.error_colour,
                )
            )
        elif isinstance(error, commands.CommandInvokeError):
            log.error(
                f"{error.original.__class__.__name__}: {error.original} (In {ctx.command.name})\n"
                f"Traceback:\n{''.join(traceback.format_tb(error.original.__traceback__))}"
            )
            try:
                await ctx.send(
                    embed=discord.Embed(
                        title="Unknown Error",
                        description="Please report this in the support server.\n"
                        f"```{error.original.__class__.__name__}: {error.original}```",
                        colour=self.bot.error_colour,
                    )
                )
            except Exception:
                pass


def setup(bot):
    bot.add_cog(ErrorHandler(bot))

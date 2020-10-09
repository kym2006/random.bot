import copy
import io
import logging
import subprocess
import textwrap
import traceback
from contextlib import redirect_stdout
from datetime import timezone
from typing import Optional

import discord
from classes import converters
from discord.ext import commands
from utils import checks

log = logging.getLogger(__name__)


def cleanup_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])
    return content.strip("` \n")


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    '''
    @checks.is_owner()
    @commands.command(description="Load a module.", usage="load <cog>", hidden=True)
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(f"cogs.{cog}.py")
            await ctx.send(
                embed=discord.Embed(
                    description="Successfully loaded the module.",
                    colour=self.bot.primary_colour,
                )
            )
        except Exception as e:
            await ctx.send(embed=discord.Embed(description=f"Error: {e}", colour=self.bot.error_colour)


    @checks.is_owner()
    @commands.command(description="Unload a module.", usage="unload <cog>", hidden=True)
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(f"cogs.{cog}.py")
            await ctx.send(
                embed=discord.Embed(
                    description="Successfully unloaded the module.",
                    colour=self.bot.primary_colour,
                )
            )
        except Exception as e:
            await ctx.send(embed=discord.Embed(description=f"Error: {e}", colour=self.bot.error_colour)

    '''
    @checks.is_owner()
    @commands.command(name="eval", description="Evaluate code.", usage="eval <code>", hidden=True)
    async def _eval(self, ctx, *, body: str):
        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
        }
        stdout = io.StringIO()
        exec("", env)
        to_compile = f'async def func():\n  try:\n{textwrap.indent(body, "    ")}\n  except:\n    raise'
        try:
            exec(to_compile, env)
        except:
            await ctx.send(
                embed=discord.Embed(
                    description=f"```py\n{traceback.format_exc()}\n```",
                    colour=discord.Color.red(),
                )
            )
            return
        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except (AttributeError, Exception, BaseException):
            await ctx.send(
                embed=discord.Embed(
                    description=f"```py\n{stdout.getvalue()}{traceback.format_exc()}\n```",
                    colour=discord.Color.red(),
                )
            )
        else:
            value = ret
            try:
                await ctx.message.add_reaction("✅")
            except discord.Forbidden:
                pass

            if stdout.getvalue():
                try:
                    if value != None:
                        await ctx.send(
                            embed=discord.Embed(
                                description=f"```py\n{stdout.getvalue()}{value}\n```",
                                colour=discord.Color.green(),
                            )
                        )
                    else:
                        await ctx.send(
                            embed=discord.Embed(
                                description=f"```py\n{stdout.getvalue()}\n```",
                                colour=discord.Color.green(),
                            )
                        )
                except:
                    await ctx.send(
                        embed=discord.Embed(
                            description=f"```py\n{traceback.format_exc()[-5000:]}\n```",
                            colour=discord.Color.red(),
                        )
                    )
            else:
                try:
                    # will not send if no return value
                    if value != None:
                        await ctx.send(
                            embed=discord.Embed(
                                description=f"```py\n{value}\n```",
                                colour=discord.Color.green(),
                            )
                        )
                except:
                    await ctx.send(
                        embed=discord.Embed(
                            description=f"```py\n{traceback.format_exc()[-5000:]}\n```",
                            colour=discord.Color.red(),
                        )
                    )

    @checks.is_owner()
    @commands.command(description="Execute code in bash.", usage="bash <command>", hidden=True)
    async def bash(self, ctx, *, command_to_run: str):
        try:
            output = subprocess.check_output(command_to_run.split(), stderr=subprocess.STDOUT).decode("utf-8")
            await ctx.send(embed=discord.Embed(description=f"```py\n{output}\n```", colour=self.bot.primary_colour))
        except Exception as error:
            await ctx.send(
                embed=discord.Embed(
                    title="⚠ Error",
                    description=f"```py\n{error.__class__.__name__}: {error}\n```",
                    colour=self.bot.error_colour
                )
            )

    @checks.is_owner()
    @commands.command(description="Execute SQL.", usage="sql <query>", hidden=True)
    async def sql(self, ctx, *, query: str):
        try:
            async with self.bot.pool.acquire() as conn:
                res = await conn.fetch(query)
        except Exception:
            await ctx.send(
                embed=discord.Embed(
                    title="⚠ Error",
                    description=f"```py\n{traceback.format_exc()}```",
                    colour=self.bot.error_colour,
                )
            )
            return
        if res:
            await ctx.send(embed=discord.Embed(description=f"```{res}```", colour=self.bot.primary_colour))
        else:
            await ctx.send(embed=discord.Embed(description="No results to fetch.", colour=self.bot.primary_colour))

    @checks.is_owner()
    @commands.command(
        description="Invoke the command as another user and optionally in another channel.",
        usage="invoke [channel] <user> <command>",
        hidden=True,
    )
    async def invoke(
        self,
        ctx,
        channel: Optional[discord.TextChannel],
        user: converters.GlobalUser,
        *,
        command: str,
    ):
        msg = copy.copy(ctx.message)
        channel = channel or ctx.channel
        msg.channel = channel
        msg.author = channel.guild.get_member(user.id) or user
        msg.content = ctx.prefix + command
        new_ctx = await self.bot.get_context(msg, cls=type(ctx))
        await self.bot.invoke(new_ctx)

    @checks.is_owner()
    @commands.command(description="Ban a user from the bot", usage="banuser <user>", hidden=True)
    async def banuser(self, ctx, *, user: converters.GlobalUser):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetchrow("SELECT * FROM ban WHERE identifier=$1 AND category=$2", user.id, 0)
            if res:
                await ctx.send(
                    embed=discord.Embed(
                        description="That user is already banned.",
                        colour=discord.Color.red(),
                    )
                )
                return
            await conn.execute("INSERT INTO ban (identifier, category) VALUES ($1, $2)", user.id, 0)
        self.bot.banned_users.append(user.id)
        await ctx.send(
            embed=discord.Embed(
                description="Successfully banned that user from the bot.",
                colour=self.bot.primary_colour,
            )
        )

    @checks.is_owner()
    @commands.command(description="Unban a user from the bot", usage="unbanuser <user>", hidden=True)
    async def unbanuser(self, ctx, *, user: int):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetchrow("SELECT * FROM ban WHERE identifier=$1 AND category=$2", user, 0)
            if not res:
                await ctx.send(
                    embed=discord.Embed(
                        description="That user is not already banned.",
                        colour=discord.Color.red(),
                    )
                )
                return
            await conn.execute("DELETE FROM ban WHERE identifier=$1 AND category=$2", user, 0)
        self.bot.banned_users.remove(user)
        await ctx.send(
            embed=discord.Embed(
                description="Successfully unbanned that user from the bot.",
                colour=self.bot.primary_colour,
            )
        )

    @checks.is_owner()
    @commands.command(
        description="Make the bot leave a server.",
        usage="leaveserver <server ID>",
        hidden=True,
    )
    async def leaveserver(self, ctx, *, guild: converters.GlobalGuild):
        data = await self.bot.cogs["Communication"].handler("leave_guild", 1, {"guild_id": guild["id"]})
        if not data:
            await ctx.send(embed=discord.Embed(description="That server is not found.", colour=discord.Color.red()))
        else:
            await ctx.send(
                embed=discord.Embed(
                    description="The bot has left that server.",
                    colour=self.bot.primary_colour,
                )
            )

    @checks.is_owner()
    @commands.command(
        description="Ban a server from the bot",
        usage="banserver <server ID>",
        hidden=True,
    )
    async def banserver(self, ctx, *, guild: converters.GlobalGuild):
        data = await self.bot.cogs["Communication"].handler("leave_guild", 1, {"guild_id": guild["id"]})
        if not data:
            await ctx.send(embed=discord.Embed(description="That server is not found.", colour=discord.Color.red()))
            return
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetchrow("SELECT * FROM ban WHERE identifier=$1 AND category=$2", guild["id"], 1)
            if res:
                await ctx.send(
                    embed=discord.Embed(
                        description="That server is already banned.",
                        colour=discord.Color.red(),
                    )
                )
                return
            await conn.execute("INSERT INTO ban (identifier, category) VALUES ($1, $2)", guild["id"], 1)
        self.bot.banned_guilds.append(guild["id"])
        await ctx.send(
            embed=discord.Embed(
                description="Successfully banned that server from the bot.",
                colour=self.bot.primary_colour,
            )
        )

    @checks.is_owner()
    @commands.command(
        description="Unban a server from the bot",
        usage="unbanserver <server ID>",
        hidden=True,
    )
    async def unbanserver(self, ctx, *, guild: int):
        async with self.bot.pool.acquire() as conn:
            res = await conn.fetchrow("SELECT * FROM ban WHERE identifier=$1 AND category=$2", guild, 1)
            if not res:
                await ctx.send(
                    embed=discord.Embed(
                        description="That server is not already banned.",
                        colour=discord.Color.red(),
                    )
                )
                return
            await conn.execute("DELETE FROM ban WHERE identifier=$1 AND category=$2", guild, 1)
        self.bot.banned_guilds.remove(guild)
        await ctx.send(
            embed=discord.Embed(
                description="Successfully unbanned that server from the bot.",
                colour=self.bot.primary_colour,
            )
        )


def setup(bot):
    bot.add_cog(Owner(bot))

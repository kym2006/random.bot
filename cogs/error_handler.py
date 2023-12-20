import logging
import traceback

import discord
from discord.ext import commands
from discord import app_commands

log = logging.getLogger(__name__)


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.tree.error(coro = self.__dispatch_to_app_command_handler)

    async def __dispatch_to_app_command_handler(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        self.bot.dispatch("app_command_error", interaction, error)
          
    @commands.Cog.listener("on_app_command_error")
    async def get_app_command_error(self, ctx: discord.Interaction, error: discord.app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandNotFound):
            return
        
        if isinstance(error, app_commands.CheckFailure):
            await ctx.response.send_message(
                embed=discord.Embed(
                    title="Permission Denied",
                    description="You do not have permission to use this command. Consider [becoming a patron](https://ko-fi.com/ktxdym) to use this command.",
                    colour=self.bot.error_colour,
                )
            )





        


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))

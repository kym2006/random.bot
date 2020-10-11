import os

import aiohttp
import discord
from aiohttp import web
from discord.ext import commands, tasks
from quart import Quart

app = web.Application()
routes = web.RouteTableDef()


class Webserver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        app = Quart(__name__)

        @app.route("/")
        async def hello():
            return "hello world"

        @app.route("/ping")
        async def ping():
            return f"{self.bot.latency*1000}"

        bot.loop.create_task(app.run_task())


def setup(bot):
    bot.add_cog(Webserver(bot))

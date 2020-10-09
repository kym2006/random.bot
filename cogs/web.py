from aiohttp import web
from discord.ext import commands, tasks
import discord
import os
import aiohttp

app = web.Application()
routes = web.RouteTableDef()


def setup(bot):
    bot.add_cog(Webserver(bot))


class Webserver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.web_server.start()

        @routes.get('/')
        async def welcome(request):
            return web.Response(text="Hello, world")

        @routes.get('/ping')
        async def ping(request):
            return web.Response(text=f"Ping is: {self.bot.latency*1000}")

        self.webserver_port = os.environ.get('PORT', 5000)
        print(self.webserver_port)
        app.add_routes(routes)

        

    @tasks.loop()
    async def web_server(self):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host = "randombot2.herokuapp.com")
        await site.start()

    @web_server.before_loop
    async def web_server_before_loop(self):
        await self.bot.wait_until_ready()
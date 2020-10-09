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

        @routes.post('/dbl')
        async def dblwebhook(request):
            if request.headers.get('authorization') == '3mErTJMYFt':
                data = await request.json()
                user = self.bot.get_user(data['user']) or await self.bot.fetch_user(data['user'])
                if user is None:
                    return
                _type = f'Tested!' if data['type'] == 'test' else f'Voted!'
                upvoted_bot = f'<@{data["bot"]}>'
                embed = discord.Embed(title=_type, colour=discord.Color.blurple())
                embed.description = f'**Upvoter :** {user.mention} Just {_type}' + f'\n**Upvoted Bot :** {upvoted_bot}'
                embed.set_thumbnail(url=user.avatar_url)
                channel = self.bot.get_channel(5645646545142312312)
                await channel.send(embed=embed)
            return 200

        @routes.get('/ping')
        async def ping(request):
            return web.Response(text=f"Ping is: {self.bot.latency*1000}")

        self.webserver_port = os.environ.get('PORT', 5000)
        app.add_routes(routes)

        

    @tasks.loop()
    async def web_server(self):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host='0.0.0.0', port=self.webserver_port)
        await site.start()

    @web_server.before_loop
    async def web_server_before_loop(self):
        await self.bot.wait_until_ready()
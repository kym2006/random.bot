import asyncio
import datetime
import json
import logging
from pathlib import Path

import asyncpg
import discord
from discord.ext import commands

blacklist = []


def config_load():
    f = open("data/config.json", "r", encoding="utf-8-sig")
    return json.load(f)


async def run():
    """
    Where the bot gets started. If you wanted to create an database connection pool or other session for the bot to use,
    it's recommended that you create it here and pass it to the bot as a kwarg.
    """

    config = config_load()
    bot = Bot(shard_count=10, config=config, description=config["description"])
    bot.help_command = None
    bot.primary_colour = discord.Color.green()

    try:
        await bot.start(config["token"])

    except KeyboardInterrupt:
        await bot.logout()


class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=self.get_prefix_, description=kwargs.pop("description"))
        self.start_time = None
        self.app_info = None
        self.version = "1.0.0"
        self.loop.create_task(self.track_start())
        self.loop.create_task(self.load_all_extensions())
        self.loop.create_task(self.connect_postgres())
        self.loop.create_task(self.getcommands())

    async def connect_postgres(self):
        self.conn = await asyncpg.connect(
            "postgres://wzjgcdxwbmwonx:69810806bf38d4e8a89c73830da992814460afd68cd64f01aeb6d7bd32b3372d@ec2-54-235-192-146.compute-1.amazonaws.com:5432/d81vhiqqts6r24?sslmode=require"
        )

    async def track_start(self):
        """
        Waits for the bot to connect to discord and then records the time.
        Can be used to work out uptime.
        """
        await self.wait_until_ready()
        self.start_time = datetime.datetime.utcnow()

    async def get_prefix_(self, bot, message):
        """
        A coroutine that returns a prefix.

        I have made this a coroutine just to show that it can be done. If you needed async logic in here it can be done.
        A good example of async logic would be retrieving a prefix from a database.
        """
        prefix = "@"
        if message.guild is None:
            return commands.when_mentioned_or("@")(bot, message)
        row = await self.conn.fetchrow("SELECT * FROM data WHERE guild = $1", message.guild.id)
        if row is None or row["prefix"] is None:
            prefix = "@"
        else:
            prefix = row["prefix"]
        return commands.when_mentioned_or(prefix)(bot, message)

    async def load_all_extensions(self):
        """
        Attempts to load all .py files in /cogs/ as cog extensions
        """
        await self.wait_until_ready()
        await asyncio.sleep(1)  # ensure that on_ready has completed and finished printing
        await self.change_presence(
            activity=discord.Game("@help | @someone | being random on {} servers".format(len(self.guilds)))
        )
        cogs = [x.stem for x in Path("cogs").glob("*.py")]
        for extension in cogs:
            try:
                self.load_extension(f"cogs.{extension}")
                print(f"loaded {extension}")
            except Exception as e:
                error = f"{extension}\n {type(e).__name__} : {e}"
                print(f"failed to load extension {error}")
            print("-" * 10)

    async def on_ready(self):
        """
        This event is called every time the bot connects or resumes connection.
        """
        print("-" * 10)
        self.app_info = await self.application_info()
        print(
            f"Logged in as: {self.user.name}\n"
            f"Using discord.py version: {discord.__version__}\n"
            f"Owner: {self.app_info.owner}\n"
            f"Template Maker: SourSpoon / Spoon#0001"
        )
        print("-" * 10)

    async def getcommands(self):
        await self.wait_until_ready()
        await asyncio.sleep(2)
        self.botcommands = []
        for _, cog_name in enumerate(self.cogs):
            cog = self.get_cog(cog_name)
            cog_commands = cog.get_commands()
            self.botcommands.extend(cog_commands)
        print(self.botcommands)

    async def on_message(self, message):
        """
        This event triggers on every message received by the bot. Including one's that it sent itself.

        If you wish to have multiple event listeners they can be added in other cogs. All on_message listeners should
        always ignore bots.
        """
        if message.author.bot:
            return
        if message.author.id in blacklist:
            return
        await self.process_commands(message)

    @property
    def uptime(self):
        return datetime.datetime.utcnow() - self.start_time


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

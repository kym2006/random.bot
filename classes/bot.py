import datetime
import logging
import sys
import traceback
import config
import asyncpg
from discord.ext import commands
from pathlib import Path

import config
from utils import tools

log = logging.getLogger(__name__)


class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        print(kwargs)
        super().__init__(**kwargs)
        self.help_command = None
        self.start_time = datetime.datetime.utcnow()
        self.version = "1.0.0"

    @property
    def uptime(self):
        return datetime.datetime.utcnow() - self.start_time

    @property
    def config(self):
        return config

    @property
    def tools(self):
        return tools

    @property
    def primary_colour(self):
        return self.config.primary_colour

    @property
    def success_colour(self):
        return self.config.success_colour

    @property
    def error_colour(self):
        return self.config.error_colour

    async def get_data(self, guild):
        async with self.pool.acquire() as conn:
            res = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", guild)
            if not res:
                await conn.execute(
                    "INSERT INTO data VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)",
                    guild,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                )
                return await self.get_data(guild)
            return res

    all_prefix = {}

    async def connect_postgres(self):
        self.pool = await asyncpg.create_pool(self.config.database_url, max_size=20, command_timeout=60)

    async def start_bot(self):
        await self.connect_postgres()
        cogs = [x.stem for x in Path("cogs").glob("*.py")]
        async with self.pool.acquire() as conn:
            data = await conn.fetch("SELECT guild, prefix from data")
        for row in data:
            self.all_prefix[row[0]] = row[1]
        for extension in cogs:
            try:
                self.load_extension(f"cogs.{extension}")
                print(f"loaded {extension}")
            except Exception as e:
                error = f"{extension}\n {type(e).__name__} : {e}"
                print(f"failed to load extension {error}")
            print("-" * 10)

        
        await self.start(self.config.token)

import datetime
import logging
import sys
import os
import traceback

import asyncpg
from discord.ext import commands

import config
from utils import tools

log = logging.getLogger(__name__)


class RandomBot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        self.start_time = datetime.datetime.utcnow()

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
    def error_colour(self):
        return self.config.error_colour

    all_prefix = {}

    async def connect_postgres(self):
        self.pool = await asyncpg.create_pool(config.db_url)

    async def start_bot(self):
        await self.connect_postgres()
        async with self.pool.acquire() as conn:
            data = conn.fetch("SELECT guild, prefix FROM data")
        for row in data:
            self.all_prefix[row[0]] = row[1]
        for extension in self.config.initial_extensions:
            try:
                self.load_extension(extension)
            except Exception:
                log.error(f"Failed to load extension {extension}.", file=sys.stderr)
                log.error(traceback.print_exc(), file=sys.stderr)
        await self.start(self.config.token)

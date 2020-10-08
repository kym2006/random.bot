import asyncio
import logging

import discord
from discord.ext import commands

import config
from classes.bot import Bot
from utils.tools import get_prefix

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

log = logging.getLogger(__name__)


async def _get_prefix(bot, message):
    prefix = await get_prefix(bot, message.guild)
    return commands.when_mentioned_or(prefix)(bot, message)


bot = Bot(
    command_prefix=_get_prefix,
    activity=discord.Activity(type=discord.ActivityType.watching, name=config.activity),
    heartbeat_timeout=300,
)




loop = asyncio.get_event_loop()
loop.run_until_complete(bot.start_bot())

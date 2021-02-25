import asyncio
import logging
import discord 
from discord.ext import commands

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
    prefix = get_prefix(bot, message.guild)
    return commands.when_mentioned_or(prefix)(bot, message)

intents=discord.Intents.default()
intents.members=True 
bot = Bot(
    command_prefix=_get_prefix,
    heartbeat_timeout=300,
    intents=intents,
    shard_count=2,
    case_insensitive=True,
    chunk_guilds_at_startup=True,
    help_command=None,
)

@bot.event
async def on_message(_):
    pass

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.start_bot())

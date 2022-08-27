import asyncio
import logging
import discord 
from discord.ext import commands
from classes.bot import Bot
from utils.tools import get_prefix
from discord.ext.commands import DefaultHelpCommand
print(DefaultHelpCommand)
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
intents.messages=True
bot = Bot(
    command_prefix='?',
    heartbeat_timeout=300,
    intents=intents,
    case_insensitive=True,
    chunk_guilds_at_startup=False,
    #help_command=DefaultHelpCommand(),
)

@bot.event
async def on_message(_):
    pass

asyncio.run(bot.start_bot())
#loop = asyncio.get_event_loop()
#loop.run_until_complete(bot.start_bot())
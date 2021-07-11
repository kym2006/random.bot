# Bot Info
import os

from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")
database_url = os.getenv("DB_URL")
statcord = os.getenv("statcord")
randomorg = os.getenv("RANDOMORGTOKEN")
pastebin = os.getenv("PASTEBIN")
if "testing" in os.environ:
    token = os.getenv("TEST_TOKEN")

# Additional shards to launch
additional_shards = 0

# The default prefix for commands
default_prefix = "?"

# Permissions to eval
owners = [
    298661966086668290,
    316213967485665281,
    412969691276115968,
    488283878189039626,
    446290930723717120,
    685456111259615252,
    712942935129456671,
    697747732772814921,
    782247763542016010,
    332754120010104833,
    676748194956181505
]

# Bot admins that have access to admin commands
admins = [
    412969691276115968,
    685456111259615252,
]

# Channels to send logs
join_channel = 725303414916907043
event_channel = 725303414916907044
admin_channel = 765896211139788830

# This is where patron roles are at
main_server = 725303414220914758

# Patron roles for premium servers
patron1 = 725303414220914763
patron2 = 725303414220914764
patron3 = 725303414220914765

# The colour used in embeds
primary_colour = 0x8125DA
success_colour = 0x00FF00
error_colour = 0xFF0000

initial_extensions = [
    "cogs.admin",
    "cogs.owner",
    "cogs.rand",
    "cogs.more",
    "cogs.org",
    "cogs.snippet",
    "cogs.economy",
    "cogs.configuration",
    "cogs.error_handler",
    "cogs.events",
    "cogs.general",
    "cogs.miscellaneous",
    "cogs.statcord"
]

down_commands=[

]

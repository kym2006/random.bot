# Bot's token
from dotenv import load_dotenv
import os 
load_dotenv()
token = os.getenv('TOKEN')
database_url = os.getenv('DB_URL')
# Additional shards to launch
additional_shards = 0

# The default prefix for commands
default_prefix = "@"


# The main bot owner
owners = [298661966086668290, 723794074498367498, 412969691276115968, 685456111259615252, 488283878189039626, 446290930723717120]

# Bot admins that have access to admin commands
admins = []


# Channels to send logs
event_channel = 725303414916907043
admin_channel = 725303414916907042

# This is where patron roles are at
main_server = 725303414220914758

# Patron roles for premium servers
premium1 = 000000000000000000
premium3 = 000000000000000000
premium5 = 000000000000000000

# The colour used in embeds
primary_colour = 0x8125DA
success_colour = 0x00FF00
error_colour = 0xFF0000

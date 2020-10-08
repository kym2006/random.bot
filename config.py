from dotenv import load_dotenv
import os

load_dotenv()


token = os.getenv('TOKEN')
db_url = os.getenv('DB_URL')
owners = [298661966086668290, 412969691276115968, 723794074498367498]

primary_colour = 0x00FF7F
error_colour = 0xFF0000

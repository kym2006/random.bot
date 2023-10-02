import asyncio 
import asyncpg 
import os 
from dotenv import load_dotenv
load_dotenv()
db = os.getenv("DB_URL")

async def run():
    conn = await asyncpg.connect(db)
    await conn.execute('''DROP TABLE lists''')
    await conn.execute('''CREATE TABLE lists(
                       userid bigint,
                       name VARCHAR(1000),
                       content VARCHAR(2048),
                       PRIMARY KEY (userid, name))
                       ''')

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
import asyncio 
import aiohttp 
import json 
import asyncpg 
import os 
from dotenv import load_dotenv
load_dotenv()
db = os.getenv("DB_URL")
async def run():
    conn = await asyncpg.connect(db)
    res = await conn.fetch("SELECT * FROM credit")
    '''
    for i in res:
        silver = i['silver']
        curgold = i['gold']
        await conn.execute("UPDATE credit set gold=$1 where userid=$2", curgold + (19+silver)//20, i['userid'])
    await conn.execute("UPDATE credit set silver=0")
    '''

loop = asyncio.get_event_loop()
loop.run_until_complete(run())


import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

_pool = None

async def init_pool():
    global _pool
    conn_string = os.getenv("PG_CONNECTION_STRING")
    if conn_string:
        _pool = await asyncpg.create_pool(dsn=conn_string)
    else:
        _pool = await asyncpg.create_pool(
            host=os.getenv("PGHOST", "localhost"),
            port=int(os.getenv("PGPORT", 5432)),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            database=os.getenv("PGDATABASE"),
        )

def get_pool():
    return _pool

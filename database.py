import aiosqlite

DB_ADDRESS: str = r"chinook.db"
DB_CONNECTION: aiosqlite.Connection = None


async def get_db_conn():
    return DB_CONNECTION


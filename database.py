import aiosqlite

# DB_ADDRESS: str = r"D:\Daftcode - kurs python\D_as_deploy\chinook.db"
DB_ADDRESS: str = r"D_as_deploy\chinook.db"
DB_CONNECTION: aiosqlite.Connection = None


async def get_db_conn():
    return DB_CONNECTION


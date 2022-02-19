import asyncio

async def get_login_user(pool, username):
    async with pool.acquire(timeout=10) as conn:
        user = await conn.fetchrow('SELECT * FROM users WHERE username = $1',
                                   username)
    return user
import asyncio

async def get_login_user(pool, username):
    async with pool.acquire(timeout=10) as conn:
        user = await conn.fetchrow('SELECT * FROM users WHERE username = $1',
                                   username)
    return user

async def get_posts(pool, login):
    async with pool.acquire(timeout=10) as conn:
        if login:
            user_id = await conn.fetchval('SELECT id FROM users WHERE username = $1', login)
            posts = await conn.fetch('SELECT * FROM posts INNER JOIN users ON posts.user_id = users.id WHERE '
                                     'posts.user_id = $1', user_id)
        else:
            posts = await conn.fetch('SELECT * FROM posts')
    posts = [dict(post) for post in posts]
    return posts
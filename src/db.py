import asyncio

async def get_login_user(pool, username):
    async with pool.acquire(timeout=10) as conn:
        user = await conn.fetchrow('SELECT * FROM users WHERE username = $1',
                                   username)
    return user

async def get_distributor_posts(pool, login):
    async with pool.acquire(timeout=10) as conn:
        if login:
            user_id = await conn.fetchval('SELECT id FROM users WHERE username = $1', login)
            posts = await conn.fetch('SELECT * FROM posts INNER JOIN users ON posts.user_id = users.id WHERE '
                                     'posts.user_id = $1 AND posts.type = $2', user_id, 'distributor')
        else:
            posts = await conn.fetch('SELECT * FROM posts WHERE posts.type = $1', 'distributor')
    posts = [dict(post) for post in posts]
    return posts

async def get_event_posts(pool):
    async with pool.acquire(timeout=10) as conn:
        posts = await conn.fetch('SELECT * FROM posts WHERE posts.type = $1', 'event')
    posts = [dict(post) for post in posts]
    return posts

async def add_post(pool, post, type, login):
    async with pool.acquire(timeout=10) as conn:
        user_id = await conn.fetchval('SELECT id FROM users WHERE username = $1', login)
        await conn.execute('INSERT INTO posts(title, org_name, food_name, address, date, allergens, image, user_id, type)'
                           ' VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9)', post.title.data, post.org_name.data,
                           post.food_name.data, post.address.data, post.date.data, post.allergens.data, post.image.data,
                           user_id, type)

async def acceptEvent(pool, id, login):
    async with pool.acquire(timeout=10) as conn:
        user = await conn.fetchrow('SELECT * FROM users WHERE username = $1', login)
        display_name = user['display_name']
        await conn.execute('UPDATE posts SET org_name = $1, type = $2 WHERE id = $3', display_name, 'distributor', id)
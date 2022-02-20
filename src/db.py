import asyncio

async def get_login_user(pool, username):
    async with pool.acquire(timeout=10) as conn:
        user = await conn.fetchrow('SELECT * FROM users WHERE username = $1',
                                   username)
    return user

async def get_consumer_posts(pool):
    async with pool.acquire(timeout=10) as conn:
        posts = await conn.fetch('SELECT * FROM posts WHERE posts.type = $1 AND posts.state = $2', 'distributor',
                                 'published')
    posts = [dict(post) for post in posts]
    return posts

async def get_distributor_posts(pool, login):
    async with pool.acquire(timeout=10) as conn:
        if login:
            user_id = await conn.fetchval('SELECT id FROM users WHERE username = $1', login)
            posts = await conn.fetch('SELECT * FROM posts INNER JOIN users ON posts.user_id = users.id WHERE '
                                     'posts.user_id = $1 AND posts.type = $2 AND posts.state = $3', user_id,
                                     'distributor', 'published')
            accepted_posts = await conn.fetch('SELECT *, posts.id AS post_id FROM posts INNER JOIN users ON posts.user_id = users.id WHERE '
                                     'posts.user_id = $1 AND posts.type = $2 AND posts.state = $3', user_id,
                                     'distributor', 'accepted')
        else:
            posts = await conn.fetch('SELECT * FROM posts WHERE posts.type = $1 AND posts.state = $2', 'distributor',
                                     'published')
            accepted_posts = await conn.fetch('SELECT * FROM posts WHERE posts.type = $1 AND posts.state = $2',
                                              'distributor', 'accepted')
    posts = [dict(post) for post in posts]
    accepted_posts = [dict(post) for post in accepted_posts]
    return posts, accepted_posts

async def get_event_posts(pool):
    async with pool.acquire(timeout=10) as conn:
        posts = await conn.fetch('SELECT * FROM posts WHERE posts.type = $1', 'event')
    posts = [dict(post) for post in posts]
    return posts

async def add_post(pool, post, type, login):
    async with pool.acquire(timeout=10) as conn:
        user_id = await conn.fetchval('SELECT id FROM users WHERE username = $1', login)
        await conn.execute('INSERT INTO posts(title, org_name, food_name, address, date, allergens, user_id, type, state)'
                           ' VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9)', post.title.data, post.org_name.data,
                           post.food_name.data, post.address.data, post.date.data, post.allergens.data, user_id, type,
                           'created')

async def acceptEvent(pool, id, login):
    async with pool.acquire(timeout=10) as conn:
        user = await conn.fetchrow('SELECT * FROM users WHERE username = $1', login)
        display_name = user['display_name']
        await conn.execute('UPDATE posts SET org_name = $1, type = $2, state = $3 WHERE id = $4', display_name,
                           'distributor', 'accepted', id)

async def publishEvent(pool, id):
    async with pool.acquire(timeout=10) as conn:
        await conn.execute('UPDATE posts SET state = $1 WHERE id = $2', 'published', id)
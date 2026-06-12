import asyncio
import os
import sys
import bcrypt
import asyncpg
from dotenv import load_dotenv

load_dotenv()

SALT_ROUNDS = 8

async def seed():
    conn_string = os.getenv("PG_CONNECTION_STRING")
    if conn_string:
        pool = await asyncpg.create_pool(dsn=conn_string)
    else:
        pool = await asyncpg.create_pool(
            host=os.getenv("PGHOST", "localhost"),
            port=int(os.getenv("PGPORT", 5432)),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            database=os.getenv("PGDATABASE"),
        )

    async with pool.acquire() as conn:
        # Drop tables in reverse dependency order (todos references users via FK)
        await conn.execute("DROP TABLE IF EXISTS todos")
        await conn.execute("DROP TABLE IF EXISTS users")

        await conn.execute("""
            CREATE TABLE users (
                user_id       SERIAL PRIMARY KEY,
                username      TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)

        await conn.execute("""
            CREATE TABLE todos (
                todo_id     SERIAL PRIMARY KEY,
                title       TEXT NOT NULL,
                is_complete BOOLEAN NOT NULL DEFAULT FALSE,
                user_id     INT REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)

        alice_hash = bcrypt.hashpw(b"password123", bcrypt.gensalt(SALT_ROUNDS)).decode()
        bob_hash = bcrypt.hashpw(b"password123", bcrypt.gensalt(SALT_ROUNDS)).decode()

        # RETURNING captures inserted user_ids so we don't hardcode them
        users = await conn.fetch("""
            INSERT INTO users (username, password_hash) VALUES
                ('alice', $1),
                ('bob',   $2)
            RETURNING user_id, username
        """, alice_hash, bob_hash)

        alice, bob = users[0], users[1]

        await conn.execute("""
            INSERT INTO todos (title, is_complete, user_id) VALUES
                ('Buy groceries',        FALSE, $1),
                ('Walk the dog',         FALSE, $1),
                ('Read a book',          TRUE,  $1),
                ('Set up the database',  TRUE,  $2),
                ('Build the API',        TRUE,  $2),
                ('Build the frontend',   FALSE, $2)
        """, alice["user_id"], bob["user_id"])

    await pool.close()
    return [dict(u) for u in users]


if __name__ == "__main__":
    try:
        users = asyncio.run(seed())
        print("Database seeded successfully.")
        print(f"  Users: {', '.join(u['username'] for u in users)}")
    except Exception as err:
        print(f"Error seeding database: {err}")
        sys.exit(1)

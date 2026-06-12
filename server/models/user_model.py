import bcrypt
from db.pool import get_pool

SALT_ROUNDS = 8

# Creates a new user. Returns { user_id, username } — never exposes password_hash.
async def create(username, password):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(SALT_ROUNDS)).decode()
    pool = get_pool()
    row = await pool.fetchrow(
        "INSERT INTO users (username, password_hash) VALUES ($1, $2) RETURNING user_id, username",
        username, password_hash
    )
    return dict(row)

# Returns { user_id, username } or None
async def find(user_id):
    pool = get_pool()
    row = await pool.fetchrow(
        "SELECT user_id, username FROM users WHERE user_id = $1",
        user_id
    )
    return dict(row) if row else None

# Returns { user_id, username } or None — used to check if a username is taken
async def find_by_username(username):
    pool = get_pool()
    row = await pool.fetchrow(
        "SELECT user_id, username FROM users WHERE username = $1",
        username
    )
    return dict(row) if row else None

# Verifies a password against the stored hash. Returns { user_id, username } if
# valid, or None if the username doesn't exist or the password is wrong.
async def validate_password(username, password):
    pool = get_pool()
    row = await pool.fetchrow(
        "SELECT * FROM users WHERE username = $1",
        username
    )
    if not row:
        return None
    user = dict(row)
    is_valid = bcrypt.checkpw(password.encode(), user["password_hash"].encode())
    if not is_valid:
        return None
    return {"user_id": user["user_id"], "username": user["username"]}

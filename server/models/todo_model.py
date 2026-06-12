from db.pool import get_pool

# Returns all todos for a specific user, ordered by creation time
async def list_by_user(user_id):
    pool = get_pool()
    rows = await pool.fetch(
        "SELECT * FROM todos WHERE user_id = $1 ORDER BY todo_id ASC",
        user_id
    )
    return [dict(r) for r in rows]

# Returns a single todo row (used for ownership checks before update/delete)
async def find(todo_id):
    pool = get_pool()
    row = await pool.fetchrow(
        "SELECT * FROM todos WHERE todo_id = $1",
        todo_id
    )
    return dict(row) if row else None

# Creates a new todo. Returns the full todo row.
async def create(title, user_id):
    pool = get_pool()
    row = await pool.fetchrow(
        "INSERT INTO todos (title, user_id) VALUES ($1, $2) RETURNING *",
        title, user_id
    )
    return dict(row)

# Updates is_complete for a todo. Returns the updated row.
async def update(todo_id, is_complete):
    pool = get_pool()
    row = await pool.fetchrow(
        "UPDATE todos SET is_complete = $1 WHERE todo_id = $2 RETURNING *",
        is_complete, todo_id
    )
    return dict(row) if row else None

# Deletes a todo by id
async def destroy(todo_id):
    pool = get_pool()
    row = await pool.fetchrow(
        "DELETE FROM todos WHERE todo_id = $1 RETURNING *",
        todo_id
    )
    return dict(row) if row else None

from fastapi import APIRouter

router = APIRouter()

@router.get("/todos")
async def list_todos():
    pass  # your logic here

@router.post("/todos")
async def create_todo():
    pass

@router.patch("/todos/{todo_id}")
async def update_todo(todo_id: int):
    pass

@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    pass
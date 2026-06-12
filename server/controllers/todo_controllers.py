from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
import models.todo_model as todo_model
from middleware.checkAuthentication import check_authentication

router = APIRouter()

@router.get("/todos")
async def list_todos(request: Request, user_id: int = Depends(check_authentication)):
    todos = await todo_model.list_by_user(user_id)
    return todos

@router.post("/todos", status_code=201)
async def create_todo(request: Request, user_id: int = Depends(check_authentication)):
    body = await request.json()
    title = body.get("title")
    if not title:
        return JSONResponse(status_code=400, content={"error": "Title is required."})
    todo = await todo_model.create(title, user_id)
    return JSONResponse(status_code=201, content=todo)

@router.patch("/todos/{todo_id}")
async def update_todo(todo_id: int, request: Request, user_id: int = Depends(check_authentication)):
    todo = await todo_model.find(todo_id)
    if not todo:
        return JSONResponse(status_code=404, content={"error": "Todo not found."})
    if todo["user_id"] != user_id:
        return JSONResponse(status_code=403, content={"error": "Not authorized."})
    body = await request.json()
    updated_todo = await todo_model.update(todo_id, body.get("is_complete"))
    return updated_todo

@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, request: Request, user_id: int = Depends(check_authentication)):
    # First find the todo to verify ownership
    todo = await todo_model.find(todo_id)
    if not todo:
        return JSONResponse(status_code=404, content={"error": "Todo not found."})
    if todo["user_id"] != user_id:
        return JSONResponse(status_code=403, content={"error": "Not authorized."})

    # Destroy the todo only after ownership has been verified
    destroyed_todo = await todo_model.destroy(todo_id)
    return destroyed_todo

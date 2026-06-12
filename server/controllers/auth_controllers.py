from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import models.user_model as user_model

router = APIRouter()

@router.post("/register", status_code=201)
async def register(request: Request):
    body = await request.json()
    username = body.get("username")
    password = body.get("password")
    if not username or not password:
        return JSONResponse(status_code=400, content={"error": "Username and password are required."})

    existing_user = await user_model.find_by_username(username)
    if existing_user:
        return JSONResponse(status_code=400, content={"error": "Username already taken."})

    user = await user_model.create(username, password)
    request.session["user_id"] = user["user_id"]
    return JSONResponse(status_code=201, content=user)

@router.post("/login")
async def login(request: Request):
    body = await request.json()
    username = body.get("username")
    password = body.get("password")
    user = await user_model.validate_password(username, password)
    if not user:
        return JSONResponse(status_code=401, content={"error": "Invalid credentials."})
    request.session["user_id"] = user["user_id"]
    return user

# Returns the logged-in user object, or null if no session exists.
# Returning JSON null (200) keeps the response format consistent — the frontend
# can always call response.json() without hitting a parse error.
@router.get("/me")
async def get_me(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JSONResponse(content=None)
    user = await user_model.find(user_id)
    return user

@router.delete("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out."}

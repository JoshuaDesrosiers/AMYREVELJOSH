import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

from middleware.log_routes import log_routes_middleware
# import checkAuthentication
from controllers.auth_controllers import router as auth_router
from controllers.todo_controllers import router as todos_router
from db.pool import init_pool

load_dotenv()

PORT = int(os.getenv("PORT", 8080))
FRONTEND_PATH = "../frontend/dist"

# ====================================
# App
# ====================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()
    yield

app = FastAPI(lifespan=lifespan)

# ====================================
# Middleware
# ====================================

app.middleware("http")(log_routes_middleware)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "dev-secret"))

# ====================================
# Auth routes
# ====================================

app.include_router(auth_router, prefix="/api/auth")

# ====================================
# Todo routes (all require authentication)
# ====================================

app.include_router(todos_router, prefix="/api")

# ====================================
# Static files
# ====================================

app.mount("/", StaticFiles(directory=FRONTEND_PATH, html=True), name="frontend")

# ====================================
# Error handling
# ====================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(exc)
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

# ====================================
# Run
# ====================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)

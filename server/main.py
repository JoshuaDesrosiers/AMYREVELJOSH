import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from middleware.log_routes import log_routes_middleware
from routers.todo import router

load_dotenv()

PORT = int(os.getenv("PORT", 8080))
FRONTEND_PATH = "../frontend/dist"

# ====================================
# App
# ====================================

app = FastAPI()

# ====================================
# Middleware
# ====================================

app.middleware("http")(log_routes_middleware)

# ====================================
# Todo routes
# ====================================

app.include_router(router, prefix="/api")

# ====================================
# Static files
# ====================================

app.mount("/", StaticFiles(directory=FRONTEND_PATH, html=True), name="frontend")

# ====================================
# Error handling
# ====================================

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


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
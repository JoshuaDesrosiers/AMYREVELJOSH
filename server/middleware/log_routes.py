from fastapi import Request
from datetime import datetime

async def log_routes_middleware(request: Request, call_next):
    time = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    print(f"{request.method}: {request.url.path} - {time}")
    response = await call_next(request)
    return response

from fastapi import Request

async def log_routes_middleware(request: Request, call_next):
    print(f"{request.method} {request.url.path}")
    response = await call_next(request)
    return response
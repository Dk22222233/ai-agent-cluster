from fastapi import FastAPI
from app.api.routers import user_router, agent_router, integration_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request


app=FastAPI()

@app.exception_handler(Exception)
async def cors_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers={"Access-Control-Allow-Origin": "http://localhost:5173"},
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "null",               # ← required for file:// based pages
    ],
    allow_credentials=True,   # must be True when using Authorization header
    allow_methods=["*"],
    allow_headers=["*"],      # allows Authorization, Content-Type, etc.
)
app.include_router(user_router)
app.include_router(agent_router)
app.include_router(integration_router)
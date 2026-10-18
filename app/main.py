from fastapi import FastAPI
from app.api.routers import user_router, agent_router, integration_router
app=FastAPI()
app.include_router(user_router)
app.include_router(agent_router)
app.include_router(integration_router)
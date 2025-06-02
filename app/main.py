
from fastapi import FastAPI
from app.routes.auth import auth_router

app = FastAPI(title="Tijzi Auth Backend")

app.include_router(auth_router, prefix="/auth")

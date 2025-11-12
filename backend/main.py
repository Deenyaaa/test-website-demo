from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.routers import web, api
from backend.db import init_db

app = FastAPI(
    title="Test Website Demo",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/redoc"
)

# === Static files ===
app.mount("/static", StaticFiles(directory="static"), name="static")

# === Initialize Database ===
init_db()

# === Include routers ===
app.include_router(web.router)
app.include_router(api.router)

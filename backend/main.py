from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import init_db
from routers import game

app = FastAPI(
    title="Text-Based Adventure: The Lost Kingdom of Aethermoor",
    version="1.0.0",
    description="A Python/FastAPI text adventure game with PostgreSQL persistence.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game.router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {
        "name": "Aethermoor Adventure API",
        "docs": "/docs",
        "health": "ok",
    }

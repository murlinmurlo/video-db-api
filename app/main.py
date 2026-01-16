from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import create_tables, engine
from . import routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Database tables created")
    yield
    engine.dispose()
    print("Database connection closed")

app = FastAPI(
    title="Video database API",
    description="REST API сервис для работы с базой данных видео",
    version="1.0.0",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(routes.router)

@app.get("/")
def read_root():
    return {
        "message": "Video database API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
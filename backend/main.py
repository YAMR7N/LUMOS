from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api.endpoints import auth, chat, upload, figures, export
from core.config import settings
from core.database import init_db
from services.retrieval import init_vector_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await init_vector_db()
    yield
    # Shutdown
    # Add cleanup code here if needed


app = FastAPI(
    title="Study Assistant API",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(figures.router, prefix="/api/figures", tags=["figures"])
app.include_router(export.router, prefix="/api/export", tags=["export"])


@app.get("/")
async def root():
    return {"message": "Study Assistant API", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        ws_max_size=16 * 1024 * 1024  # 16MB for WebSocket messages
    )
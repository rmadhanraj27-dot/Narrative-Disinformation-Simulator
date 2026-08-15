from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.mongodb import (
    check_database_connection,
    close_database_connection
)

from app.database.init_db import initialize_database

from app.routes.auth import router as auth_router
from app.routes.events import router as events_router
from app.routes.news import router as news_router


# ============================================================
# APPLICATION LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting application...")

    database_connected = await check_database_connection()

    if database_connected:

        print("MongoDB connection successful!")

        await initialize_database()

    else:

        print("MongoDB connection failed!")

    yield

    print("Application shutting down...")

    await close_database_connection()


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Narrative Disinformation Simulator & Detector",
    version="1.0.0",
    description=(
        "AI-based proactive misinformation "
        "analysis system."
    ),
    lifespan=lifespan
)


# ============================================================
# ROUTES
# ============================================================

app.include_router(
    auth_router
)

app.include_router(
    events_router
)

app.include_router(
    news_router
)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
async def root():

    return {
        "message": (
            "Narrative Disinformation Simulator "
            "API is running"
        )
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health_check():

    database_connected = (
        await check_database_connection()
    )

    return {
        "status": "healthy",
        "database": (
            "connected"
            if database_connected
            else "disconnected"
        )
    }
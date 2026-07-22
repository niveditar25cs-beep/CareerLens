from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.init_db import init_db
from app.routes import auth, students, opportunities, recommendation, dashboard, notification


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup and shutdown actions."""
    # Create tables on startup
    await init_db()
    yield


# ==========================================
# Application Configuration
# ==========================================
app = FastAPI(
    title="CareerLens API",
    description="Backend API for CareerLens – a smart, modular platform for discovering and managing career opportunities.",
    version="1.0.0",
    lifespan=lifespan,
)

# ==========================================
# CORS Middleware Configuration
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# API Routers Configuration
# ==========================================
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(opportunities.router, prefix="/api/opportunities", tags=["Opportunities"])
app.include_router(recommendation.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(notification.router, prefix="/api/notifications", tags=["Notifications"])


# ==========================================
# Root Endpoint
# ==========================================
@app.get("/", tags=["Root"])
async def root_endpoint():
    """
    Root endpoint to verify that the CareerLens API is running successfully.
    """
    return {
        "status": "success",
        "message": "Welcome to the CareerLens API. The server is running successfully!"
    }


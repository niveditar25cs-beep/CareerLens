from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine
from app.database.init_db import init_db
from app.routes import auth, students, opportunities, recommendation, dashboard, notification

app = FastAPI(
    title="CareerLens API",
    description="Backend API for CareerLens – a smart career opportunity platform for students.",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(opportunities.router, prefix="/api/opportunities", tags=["Opportunities"])
app.include_router(recommendation.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(notification.router, prefix="/api/notifications", tags=["Notifications"])


@app.on_event("startup")
async def startup_event():
    """Initialize the database on application startup."""
    await init_db()


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to CareerLens API"}

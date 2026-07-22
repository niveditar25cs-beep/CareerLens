from app.database.database import engine, Base

# Import all models so they are registered with Base.metadata
from app.models import student, opportunity, saved, recommendation, notification  # noqa: F401


async def init_db():
    """Create all database tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully.")

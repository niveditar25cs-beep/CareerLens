from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.database.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(300), nullable=False)
    message = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False)
    notification_type = Column(String(50), nullable=True)  # e.g., "deadline", "new_match", "general"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

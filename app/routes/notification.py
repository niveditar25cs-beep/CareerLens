from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database.database import get_db
from app.models.notification import Notification
from app.models.student import Student
from app.utils.jwt_handler import get_current_student

router = APIRouter()


@router.get("/")
async def get_notifications(
    current_student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Get all notifications for the current student."""
    result = await db.execute(
        select(Notification)
        .where(Notification.student_id == current_student.id)
        .order_by(Notification.created_at.desc())
    )
    return result.scalars().all()


@router.put("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    current_student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Mark a notification as read."""
    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.student_id == current_student.id,
        )
    )
    notification = result.scalar_one_or_none()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    await db.commit()
    return {"message": "Notification marked as read"}


@router.put("/read-all")
async def mark_all_as_read(
    current_student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Mark all notifications as read for the current student."""
    result = await db.execute(
        select(Notification).where(
            Notification.student_id == current_student.id,
            Notification.is_read == False,  # noqa: E712
        )
    )
    notifications = result.scalars().all()
    for notif in notifications:
        notif.is_read = True
    await db.commit()
    return {"message": f"{len(notifications)} notifications marked as read"}

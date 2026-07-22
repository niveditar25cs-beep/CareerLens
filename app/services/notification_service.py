"""
Notification service for creating and managing student notifications.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notification import Notification


async def create_notification(
    db: AsyncSession,
    student_id: int,
    title: str,
    message: str = "",
    notification_type: str = "general",
) -> Notification:
    """
    Create a new notification for a student.

    Args:
        db: Async database session.
        student_id: The ID of the student to notify.
        title: Notification title.
        message: Notification body text.
        notification_type: Category of notification (deadline, new_match, general).

    Returns:
        The created Notification object.
    """
    notification = Notification(
        student_id=student_id,
        title=title,
        message=message,
        notification_type=notification_type,
    )
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    return notification


async def notify_deadline_approaching(db: AsyncSession, student_id: int, opportunity_title: str):
    """Send a deadline reminder notification."""
    return await create_notification(
        db=db,
        student_id=student_id,
        title="Deadline Approaching",
        message=f'The deadline for "{opportunity_title}" is coming up soon!',
        notification_type="deadline",
    )


async def notify_new_match(db: AsyncSession, student_id: int, opportunity_title: str):
    """Send a new match notification."""
    return await create_notification(
        db=db,
        student_id=student_id,
        title="New Opportunity Match",
        message=f'A new opportunity "{opportunity_title}" matches your profile!',
        notification_type="new_match",
    )


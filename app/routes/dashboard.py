from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.database.database import get_db
from app.models.student import Student
from app.models.opportunity import Opportunity
from app.models.saved import SavedOpportunity
from app.models.notification import Notification
from app.utils.jwt_handler import get_current_student

router = APIRouter()


@router.get("/")
async def get_dashboard(
    current_student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Get dashboard summary for the current student."""
    # Total opportunities
    opp_count = await db.execute(select(func.count(Opportunity.id)))
    total_opportunities = opp_count.scalar()

    # Saved opportunities
    saved_count = await db.execute(
        select(func.count(SavedOpportunity.id)).where(
            SavedOpportunity.student_id == current_student.id
        )
    )
    total_saved = saved_count.scalar()

    # Unread notifications
    notif_count = await db.execute(
        select(func.count(Notification.id)).where(
            Notification.student_id == current_student.id,
            Notification.is_read == False,  # noqa: E712
        )
    )
    unread_notifications = notif_count.scalar()

    return {
        "student_name": current_student.full_name,
        "total_opportunities": total_opportunities,
        "saved_opportunities": total_saved,
        "unread_notifications": unread_notifications,
    }

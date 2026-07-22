from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.database.database import get_db
from app.models.opportunity import Opportunity
from app.schemas.opportunity import OpportunityCreate, OpportunityResponse, OpportunityUpdate

router = APIRouter()


@router.get("/", response_model=List[OpportunityResponse])
async def list_opportunities(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    opportunity_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List opportunities with optional filtering and pagination."""
    query = select(Opportunity)
    if opportunity_type:
        query = query.where(Opportunity.opportunity_type == opportunity_type)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(opportunity_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single opportunity by ID."""
    result = await db.execute(select(Opportunity).where(Opportunity.id == opportunity_id))
    opportunity = result.scalar_one_or_none()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity


@router.post("/", response_model=OpportunityResponse, status_code=201)
async def create_opportunity(data: OpportunityCreate, db: AsyncSession = Depends(get_db)):
    """Create a new opportunity."""
    opportunity = Opportunity(**data.model_dump())
    db.add(opportunity)
    await db.commit()
    await db.refresh(opportunity)
    return opportunity


@router.put("/{opportunity_id}", response_model=OpportunityResponse)
async def update_opportunity(
    opportunity_id: int,
    updates: OpportunityUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing opportunity."""
    result = await db.execute(select(Opportunity).where(Opportunity.id == opportunity_id))
    opportunity = result.scalar_one_or_none()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(opportunity, field, value)

    await db.commit()
    await db.refresh(opportunity)
    return opportunity


@router.delete("/{opportunity_id}", status_code=204)
async def delete_opportunity(opportunity_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an opportunity."""
    result = await db.execute(select(Opportunity).where(Opportunity.id == opportunity_id))
    opportunity = result.scalar_one_or_none()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    await db.delete(opportunity)
    await db.commit()

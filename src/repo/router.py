from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from sqlmodel import Session

from src.core.database import get_session
from src.auth.dependencies import get_current_user
from src.repo.analytics_repo import AnalyticsRepository
from src.analytics_service import AnalyticsService
from src.schemas import SalesTrendResponse, InventoryResponse, Dataset

router = APIRouter(tags=["Analytics"])

@router.get("/sales-trend", response_model=SalesTrendResponse)
def sale_trend(
    start: datetime = Query(..., description="Start date for the trend analysis"),
    end: datetime = Query(..., description="End date for the trend analysis"),
    session: Session = Depends(get_session)
):
    if end < start:
        raise HTTPException(status_code=400, detail="End date must be after start date")
    
    repo = AnalyticsRepository(session)
    service = AnalyticsService(repo)
    return service.sales_trend_chart(get_current_user.organization_id, start=start, end=end)

@router.get("/inventory", response_model=InventoryResponse)
def inventory(
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    repo = AnalyticsRepository(session)
    service = AnalyticsService(repo)
    return service.inventory_chart(current_user.organization_id)

@router.get("/average-sales")
def sales_summary(
    start: datetime = Query(...),
    end: datetime = Query(...),
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    if end < start:
        raise HTTPException(status_code=400, detail="End date must be after start date")
    
    repo = AnalyticsRepository(session)
    service = AnalyticsService(repo)
    return service.sales_avg(current_user.organization_id, start=start, end=end)
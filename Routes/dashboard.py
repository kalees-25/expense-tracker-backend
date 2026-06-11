from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session


from schemas.dashboard import DashboardSummaryResponse

from core.database.connection import get_db
from core.security import get_current_user

from services.dashboard.summary import (
    get_dashboard_summary
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary" , response_model=DashboardSummaryResponse)
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_dashboard_summary(
        db,
        current_user.id
    )
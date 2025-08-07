from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud.billing_history import get_billing_history
from app.database import get_db
from app.schemas.billing import BillingPreviewResponse

router = APIRouter(prefix="/billing/history", tags=["Billing History"])

@router.get("/", response_model=List[BillingPreviewResponse])
def fetch_billing_history(
    company_id: Optional[int] = Query(None),
    project_id: Optional[int] = Query(None),
    start_month: Optional[int] = Query(None),
    start_year: Optional[int] = Query(None),
    end_month: Optional[int] = Query(None),
    end_year: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    return get_billing_history(
        db=db,
        company_id=company_id,
        project_id=project_id,
        start_month=start_month,
        start_year=start_year,
        end_month=end_month,
        end_year=end_year
    )

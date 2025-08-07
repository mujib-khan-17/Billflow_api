from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.billing import BillingCreateRequest, BillingPreviewResponse, BillingSaveRequest
from app.crud.billing_generation import preview_billing, save_billing
from app.utils.auth import get_current_user
from app.routers.auth import get_db
from typing import List

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.post("/preview", response_model=List[BillingPreviewResponse])
def generate_monthly_preview(
    request: BillingCreateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["Admin", "Manager"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    return preview_billing(db, request)


@router.post("/save", response_model=List[BillingPreviewResponse])
def save_generated_bills(
    bills: List[BillingSaveRequest],
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["Admin", "Manager"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    return save_billing(db, bills, user_id=int(current_user["sub"]))

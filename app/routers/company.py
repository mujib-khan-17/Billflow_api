from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CompanyManagement, user
from app.schemas.company import CompanyCreate, CompanyResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/companies", tags=["Company"])

@router.get("/", response_model=List[CompanyResponse])
def get_companies(db: Session = Depends(get_db), current_user: user = Depends(get_current_user)):
    companies = db.query(CompanyManagement).filter(CompanyManagement.is_deleted == False).all()
    return companies

@router.post("/", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    existing = db.query(CompanyManagement).filter(
        CompanyManagement.company_name == company.company_name
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Company already exists")

    new_company = CompanyManagement(**company.dict())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company
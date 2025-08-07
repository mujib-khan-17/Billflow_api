from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CompanyManagement, user
from app.schemas.company import CompanyResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/companies", tags=["Company"])

@router.get("/", response_model=List[CompanyResponse])
def get_companies(db: Session = Depends(get_db), current_user: user = Depends(get_current_user)):
    companies = db.query(CompanyManagement).filter(CompanyManagement.is_deleted == False).all()
    return companies


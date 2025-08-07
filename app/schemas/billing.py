from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class BillingType(str, Enum):
    Hosting = "Hosting"

class BillingCreateRequest(BaseModel):
    month: int
    year: int

class BillingPreviewResponse(BaseModel):
    type: str
    company: str
    contact_person: str
    contact_email: str
    month_year: str
    project_name: str
    hosting_amount: float
    currency: str
    details: str
    project_id: int

    class Config:
        orm_mode = True

class BillingSaveRequest(BaseModel):
    project_id: int
    amount: float
    currency: str
    month: int
    year: int
    details: str


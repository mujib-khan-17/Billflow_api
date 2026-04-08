from pydantic import BaseModel, EmailStr

from app.models.company import CompanyStatus

class CompanyResponse(BaseModel):
    id: int
    company_name: str

    class Config:
        orm_mode = True

class CompanyCreate(BaseModel):
    company_name: str
    contact_name: str
    contact_email_address: EmailStr
    accounts_email_address: EmailStr
    contact_number: str
    status: CompanyStatus
    created_by: int
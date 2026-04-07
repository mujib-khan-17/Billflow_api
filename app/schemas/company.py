from pydantic import BaseModel

class CompanyResponse(BaseModel):
    id: int
    company_name: str

    class Config:
        orm_mode = True
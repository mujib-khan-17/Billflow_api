from pydantic import BaseModel, ConfigDict

class CompanyResponse(BaseModel):
    id: int
    company_name: str

    model_config = ConfigDict(from_attributes=True)
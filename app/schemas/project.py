from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.models.project import ProjectStatus

class ProjectCreate(BaseModel):
    project_code: str
    project_name: str
    beta_url: Optional[str] = None
    beta_server: Optional[str] = None
    beta_release_date: Optional[date] = None
    production_url: Optional[str] = None
    production_server: Optional[str] = None
    live_date: Optional[date] = None
    hosting_amount: Optional[float] = None
    company_id: int
    currency: str
    status: ProjectStatus  

class ProjectResponse(BaseModel):
    id: int
    project_code: str
    project_name: str

    class Config:
        orm_mode = True

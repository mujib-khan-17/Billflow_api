from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date, datetime
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
    hosting_start_date: Optional[date] = None   
    company_name: str
    currency: Optional[str] = None
    status: ProjectStatus  

class ProjectFilter(BaseModel):
    status: Optional[ProjectStatus] = None
    company_id: Optional[int] = None
    sort_by: Optional[str] = Field(default="created_at")  
    sort_order: Optional[str] = Field(default="desc")  

class ProjectResponse(BaseModel):
    id: int
    project_code: str
    project_name: str
    beta_url: Optional[str]
    beta_server: Optional[str]
    beta_release_date: Optional[datetime] 
    production_url: Optional[str] = None
    production_server: Optional[str] = None
    live_date: Optional[datetime]  
    hosting_amount: Optional[float]
    hosting_start_date: Optional[datetime]
    company_name: Optional[str] = None
    currency: str
    status: ProjectStatus
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class ProjectUpdate(BaseModel):
    project_code: Optional[str]
    project_name: Optional[str]
    beta_url: Optional[str]
    beta_server: Optional[str]
    beta_release_date: Optional[date] = None
    production_url: Optional[str]
    production_server: Optional[str]
    live_date: Optional[date] = None
    hosting_amount: Optional[float] = None
    hosting_start_date: Optional[date] = None
    currency: Optional[str] = None
    status: Optional[ProjectStatus]
    company_name: Optional[str]
    
    @model_validator(mode="before")
    @classmethod
    def check_live_date_for_production(cls, data):
        status = data.get("status")
        live_date = data.get("live_date")

        if status == "Production" and not live_date:
            raise ValueError("live_date is required when status is 'Production'")

        if status == "Beta":
            data["live_date"] = None 
            data["hosting_start_date"] = None

        return data
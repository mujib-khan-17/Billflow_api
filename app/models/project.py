import enum
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, Enum, DECIMAL, ForeignKey
from app.database import Base
from sqlalchemy.sql import func

class ProjectStatus(enum.Enum):
    WIP = "WIP"
    Beta = "Beta"
    Production = "Production"
    OnHold = "On Hold"

class ProjectManagement(Base):
    __tablename__ = "project_management"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String(50), unique=True, nullable=False)
    project_name = Column(String(100), nullable=False)
    company_id = Column(Integer, ForeignKey("company_management.id"), nullable=False)
    beta_url = Column(Text, nullable=True)
    beta_server = Column(String(100), nullable=True)
    beta_release_date = Column(DateTime, nullable=True)
    production_url = Column(Text, nullable=True)
    production_server = Column(String(100), nullable=True)
    live_date = Column(DateTime, nullable=True)
    hosting_amount = Column(DECIMAL(10, 2), nullable=False)
    hosting_start_date = Column(DateTime, nullable=True)
    currency = Column(String(10), nullable=True)
    status = Column(Enum(ProjectStatus), nullable=False)
    created_by = Column(Integer, ForeignKey("user_master.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("user_master.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
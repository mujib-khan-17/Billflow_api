from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import enum

class CompanyStatus(enum.Enum):
    Active = "Active"
    InActive = "InActive"

class CompanyManagement(Base):
    __tablename__ = "company_management"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100), unique=True, nullable=False)
    contact_name = Column(String(100), nullable=False)
    contact_email_address = Column(String(100), unique=True, nullable=False)
    accounts_email_address = Column(String(100), nullable=False)
    contact_number = Column(String(20), nullable=False)
    status = Column(Enum(CompanyStatus), nullable=False)
    created_by = Column(Integer, ForeignKey("user_master.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("user_master.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

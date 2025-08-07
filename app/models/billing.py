from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, DECIMAL, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class BillingType(enum.Enum):
    Hosting = "Hosting"

class Billing(Base):
    __tablename__ = "billing"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(BillingType), nullable=False, default=BillingType.Hosting)
    billing_datetime = Column(DateTime, server_default=func.now(), nullable=False)
    project_id = Column(Integer, ForeignKey("project_management.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(10), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    details = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("user_master.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("user_master.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_deleted = Column(Boolean, default=False, nullable=False)

    project = relationship("ProjectManagement", back_populates="billings")


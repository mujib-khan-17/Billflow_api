from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum

class UserRole(enum.Enum):
    Admin = "Admin"
    Manager = "Manager"
    User = "User"

class UserStatus(enum.Enum):
    Active = "Active"
    InActive = "InActive"

class UserMaster(Base):
    __tablename__ = "user_master"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email_id = Column(String(100), unique=True, nullable=False)
    department = Column(String(100), nullable=True)
    password = Column(String(120), nullable=False)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.Active)
    role = Column(Enum(UserRole), nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

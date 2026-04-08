from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    email_id: EmailStr
    password: str
    role: str   # or Enum if you have
    created_by: int

class UserLogin(BaseModel):
    email: EmailStr
    password: str
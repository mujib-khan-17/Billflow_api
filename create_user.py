# create_user.py
from app.database import SessionLocal
from app.models.user import UserMaster, UserRole, UserStatus
from app.utils.auth import hash_password

db = SessionLocal()

new_user = UserMaster(
    employee_code="EMP001",
    first_name="Admin",
    last_name="User",
    email_id="admin@example.com",
    department="IT",
    password=123,
    status=UserStatus.Active,
    role=UserRole.Admin,
    created_by=1,
)

db.add(new_user)
db.commit()
db.refresh(new_user)

print(f"User created with ID: {new_user.id}")

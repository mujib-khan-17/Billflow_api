from sqlalchemy.orm import Session
from app.models.user import UserMaster

def get_user_by_email(db: Session, email: str):
    return db.query(UserMaster).filter(UserMaster.email_id == email).first()

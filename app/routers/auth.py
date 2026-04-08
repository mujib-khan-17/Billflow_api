from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse
from app.database import SessionLocal, get_db
from app.schemas.user import UserCreate
from app.utils.auth import verify_password
from app.utils.jwt import create_access_token
from app.crud.auth import get_user_by_email
from app.utils.config import settings
from app.models.user import User
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=settings.USER_NOT_FOUND)

    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=settings.PASSWORD_INCORRECT)

    token_data = {"sub": str(user.id), "email": user.email_id, "role": user.role.value}
    access_token = create_access_token(token_data)
    return TokenResponse(access_token=access_token)

@router.post("/token", response_model=TokenResponse)
def login_oauth2(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)  
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=settings.USER_NOT_FOUND)

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=settings.PASSWORD_INCORRECT)

    token_data = {"sub": str(user.id), "email": user.email_id, "role": user.role.value}
    access_token = create_access_token(token_data)
    return TokenResponse(access_token=access_token)

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}
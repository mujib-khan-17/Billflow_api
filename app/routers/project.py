from fastapi import APIRouter, Depends
from app.crud.project import create_project
from sqlalchemy.orm import Session
from app.routers.auth import get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/")
def get_all_projects(current_user: dict = Depends(get_current_user)):
    return {"msg": "Projects accessed", "user": current_user}


@router.post("/", response_model=ProjectResponse)
def add_project(project: ProjectCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return create_project(db=db, project=project, user_id=int(current_user["sub"]))
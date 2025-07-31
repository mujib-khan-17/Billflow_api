from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session
from app.crud.project import create_project, get_projects, soft_delete_project, update_project
from app.routers.auth import get_db
from app.schemas.project import ProjectCreate, ProjectFilter, ProjectResponse, ProjectUpdate
from app.utils.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[ProjectResponse])
def get_all_projects(
    status: Optional[str] = Query(None),
    company_id: Optional[int] = Query(None),
    sort_by: Optional[str] = Query("created_at"),
    sort_order: Optional[str] = Query("desc"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    filters = ProjectFilter(
        status=status,
        company_id=company_id,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return get_projects(db, filters)

@router.post("/", response_model=ProjectResponse)
def add_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["Admin", "Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to add a project."
        )
    return create_project(db=db, project=project, user_id=int(current_user["sub"]))


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project_by_id(
    project: ProjectUpdate,
    project_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["Admin", "Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update projects."
        )

    return update_project(db=db, project_id=project_id, project=project, user_id=int(current_user["sub"]))

@router.delete("/{project_id}", response_model=dict)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["Admin", "Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete projects."
        )

    deleted_project = soft_delete_project(db, project_id)

    if not deleted_project:
        raise HTTPException(status_code=404, detail="Project not found or already deleted")

    return {"message": "Project deleted successfully"}
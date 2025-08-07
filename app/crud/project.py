from typing import List
from fastapi import HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from app.models.company import CompanyManagement
from app.models.project import ProjectManagement, ProjectStatus
from app.schemas.project import ProjectCreate, ProjectFilter, ProjectResponse, ProjectUpdate

def create_project(db: Session, project: ProjectCreate, user_id: int):
    company = db.query(CompanyManagement).filter(
        CompanyManagement.company_name == project.company_name
    ).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    new_project = ProjectManagement(
        project_code=project.project_code,
        project_name=project.project_name,
        beta_url=project.beta_url,
        beta_server=project.beta_server,
        beta_release_date=project.beta_release_date,
        production_url=project.production_url,
        production_server=project.production_server,
        live_date=project.live_date,
        hosting_amount=project.hosting_amount,
        hosting_start_date=project.hosting_start_date,
        company_id=company.id,
        currency=project.currency,
        status=ProjectStatus(project.status),
        created_by=user_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project



def get_projects(db: Session, filters: ProjectFilter) -> List[ProjectResponse]:
    query = (
        db.query(ProjectManagement, CompanyManagement.company_name)
        .join(CompanyManagement, ProjectManagement.company_id == CompanyManagement.id)
        .filter(ProjectManagement.is_deleted == False)
    )

    if filters.status:
        query = query.filter(ProjectManagement.status == filters.status)

    if filters.company_id:
        query = query.filter(ProjectManagement.company_id == filters.company_id)

    sort_column = getattr(ProjectManagement, filters.sort_by, ProjectManagement.created_at)
    query = query.order_by(asc(sort_column) if filters.sort_order == "asc" else desc(sort_column))

    results = query.all()

    project_responses = []
    for project, company_name in results:
        project_responses.append(ProjectResponse(
            id=project.id,
            project_code=project.project_code,
            project_name=project.project_name,
            beta_url=project.beta_url,
            beta_server=project.beta_server,
            beta_release_date=project.beta_release_date,
            production_url=project.production_url,
            production_server=project.production_server,
            live_date=project.live_date,
            hosting_amount=project.hosting_amount,
            hosting_start_date=project.hosting_start_date,
            company_id=project.company_id,
            company_name=company_name,
            currency=project.currency,
            status=project.status,
            created_at=project.created_at,
        ))

    return project_responses


def update_project(db: Session, project_id: int, project: ProjectUpdate, user_id: int):
    db_project = db.query(ProjectManagement).filter(ProjectManagement.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    for field, value in project.dict(exclude_unset=True).items():
        setattr(db_project, field, value)

    db_project.updated_by = user_id
    db.commit()
    db.refresh(db_project)
    return db_project

def soft_delete_project(db: Session, project_id: int):
    project = db.query(ProjectManagement).filter(ProjectManagement.id == project_id).first()

    if not project:
        return "not_found"
    if project.is_deleted:
        return "already_deleted"

    project.is_deleted = True
    db.commit()
    db.refresh(project)
    return "deleted"

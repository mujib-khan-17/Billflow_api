from sqlalchemy.orm import Session
from app.models.project import ProjectManagement
from app.schemas.project import ProjectCreate

def create_project(db: Session, project: ProjectCreate, user_id: int):
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
        company_id=project.company_id,
        currency=project.currency,
        status=project.status,
        created_by=user_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

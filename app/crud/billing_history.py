from sqlalchemy.orm import Session
from sqlalchemy import and_, extract
from datetime import date
from typing import List, Optional
from app.models import Billing, ProjectManagement, CompanyManagement
from app.schemas.billing import BillingPreviewResponse

def get_billing_history(
    db: Session,
    company_id: Optional[int] = None,
    project_id: Optional[int] = None,
    start_month: Optional[int] = None,
    start_year: Optional[int] = None,
    end_month: Optional[int] = None,
    end_year: Optional[int] = None,
) -> List[BillingPreviewResponse]:
    query = db.query(Billing, ProjectManagement, CompanyManagement).\
        join(ProjectManagement, Billing.project_id == ProjectManagement.id).\
        join(CompanyManagement, ProjectManagement.company_id == CompanyManagement.id)

    if company_id:
        query = query.filter(ProjectManagement.company_id == company_id)

    if project_id:
        query = query.filter(Billing.project_id == project_id)

    if start_month and start_year and end_month and end_year:
        start_value = start_year * 100 + start_month
        end_value = end_year * 100 + end_month
        query = query.filter(
             and_(
                (Billing.year * 100 + Billing.month) >= start_value,
                (Billing.year * 100 + Billing.month) <= end_value
            )
        )

    results = query.all()
    billing_list = []

    for billing, project, company in results:
    
        project_status = str(project.status.value if hasattr(project.status, "value") else project.status).strip().lower()

        if project_status == "production":
            project_url = project.production_url
        elif project_status == "beta":
            project_url = project.beta_url

        elif project_status == "wip":
            project_url = project.beta_url or project.production_url
        else:
            project_url = "N/A"

            project_url = project_url or "N/A"
        
        month_year = f"{billing.month:02d}-{billing.year}"
        details = f"Hosting fees for domain {project_url} for the month of {month_year}."

        billing_list.append(BillingPreviewResponse(
            type="Hosting",
            company=company.company_name,
            contact_person=company.contact_name,
            contact_email=company.contact_email_address,
            month_year=month_year,
            project_name=project.project_name,
            hosting_amount=billing.amount,
            currency=billing.currency,
            details=details,
            project_id=project.id
        ))

    return billing_list

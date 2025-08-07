from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.billing import Billing
from app.models.company import CompanyManagement
from app.models.project import ProjectManagement
from app.schemas.billing import BillingCreateRequest, BillingSaveRequest
from datetime import datetime

def preview_billing(db: Session, request: BillingCreateRequest):
    month, year = request.month, request.year

    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year+1, 1, 1)
    else:
        last_day = datetime(year, month+1, 1)

    existing_bills = db.query(Billing.project_id).filter(
        Billing.month == month,
        Billing.year == year,
        Billing.is_deleted == False
    ).all()
    existing_project_ids = {bill.project_id for bill in existing_bills}

    selected_month = datetime(year, month, 1)

    projects = db.query(ProjectManagement).filter(
        ProjectManagement.status.in_(["WIP", "Beta", "Production"]),
        ProjectManagement.is_deleted == False,
        ProjectManagement.hosting_start_date >= first_day,
        ProjectManagement.hosting_start_date < last_day  
    ).all()

    preview = []

    for project in projects:
        if project.id in existing_project_ids:
            continue  

        company = project.company  

        url = (
            project.production_url
            if project.status == "Production"
            else project.beta_url
        )

        detail = f"Hosting fees for domain {url} for the month of {selected_month.strftime('%B %Y')}."

        preview.append({
            "type": "Hosting",
            "company": company.company_name,
            "contact_person": company.contact_name,
            "contact_email": company.contact_email_address,
            "month_year": selected_month.strftime('%B %Y'),
            "project_name": project.project_name,
            "hosting_amount": project.hosting_amount,
            "amount": project.hosting_amount,
            "currency": project.currency,
            "details": detail,
            "project_id": project.id,
            "month": month,
            "year": year
        })

    return preview


def save_billing(db: Session, bills: List[BillingSaveRequest], user_id: int):
    project_ids = [b.project_id for b in bills]
    month = bills[0].month
    year = bills[0].year

    existing = db.query(Billing.project_id).filter(
        Billing.project_id.in_(project_ids),
        Billing.month == month,
        Billing.year == year,
        Billing.is_deleted == False
    ).all()
    existing_ids = {e.project_id for e in existing}

    if existing_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Bills already saved for projects: {list(existing_ids)} in {month}/{year}"
        )

    saved = []
    for b in bills:
        bill = Billing(
            project_id=b.project_id,
            amount=b.amount,
            currency=b.currency,
            month=b.month,
            year=b.year,
            details=b.details,
            created_by=user_id,
        )
        db.add(bill)
        saved.append(bill)

    db.commit()

    for bill in saved:
        db.refresh(bill)

    saved_ids = [b.id for b in saved]

    enriched = (
        db.query(
            Billing.id,
            Billing.project_id,
            CompanyManagement.company_name.label("company"),
            CompanyManagement.contact_name.label("contact_person"),
            CompanyManagement.contact_email_address.label("contact_email"),
            ProjectManagement.project_name,
            Billing.amount.label("hosting_amount"),
            Billing.currency,
            Billing.details,
            func.concat(Billing.month, '-', Billing.year).label("month_year"),
        )
        .join(ProjectManagement, Billing.project_id == ProjectManagement.id)
        .join(CompanyManagement, ProjectManagement.company_id == CompanyManagement.id)
        .filter(Billing.id.in_(saved_ids))
        .all()
    )

    result = [
        {   
            "type" : "Hosting",
            "project_id": row.project_id,
            "id": row.id,
            "company": row.company,
            "contact_person": row.contact_person,
            "contact_email": row.contact_email,
            "project_name": row.project_name,
            "hosting_amount": row.hosting_amount,
            "currency": row.currency,
            "details": row.details,
            "month_year": row.month_year,
        }
        for row in enriched
    ]

    return result

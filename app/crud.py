from sqlalchemy.orm import Session

from app.models import JobApplication


def get_applications(db: Session):
    return (
        db.query(JobApplication)
        .order_by(JobApplication.id.desc())
        .all()
    )


def create_application(db: Session, company: str, role: str, status: str) -> JobApplication:
    row = JobApplication(company=company, role=role, status=status)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update_application(
    db: Session,
    app_id: int,
    company: str | None = None,
    role: str | None = None,
    status: str | None = None,
) -> JobApplication | None:
    row = db.get(JobApplication, app_id)
    if row is None:
        return None

    if company is not None:
        row.company = company
    if role is not None:
        row.role = role
    if status is not None:
        row.status = status

    db.commit()
    db.refresh(row)
    return row


def delete_application(db: Session, app_id: int) -> bool:
    row = db.get(JobApplication, app_id)
    if row is None:
        return False

    db.delete(row)
    db.commit()
    return True

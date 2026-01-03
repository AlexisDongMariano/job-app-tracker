from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models import JobApplication


def get_applications(db: Session):
    return (
        db.query(JobApplication)
        .order_by(JobApplication.id.desc())
        .all()
    )


def create_application(db: Session, company: str, role: str, status: str) -> JobApplication:
    existing = (
        db.query(JobApplication)
        .filter(JobApplication.company == company, JobApplication.role == role)
        .first()
    )
    if existing:
        raise ValueError('The company + role already exists.')

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


##############
def _apply_filters(qry, *, status: str | None, q: str | None):
    if status is not None:
        qry = qry.filter(JobApplication.status == status)

    if q is not None and q.strip():
        term = f'%{q.strip()}%'
        qry = qry.filter(
            or_(
                JobApplication.company.ilike(term),
                JobApplication.role.ilike(term),
            )
        )
    return qry
    

def count_applications(db: Session, *, status: str | None = None, q: str | None = None) -> int:
    qry = db.query(func.count(JobApplication.id))
    qry = _apply_filters(qry, status=status, q=q)
    return qry.scalar() or 0


def get_applications_page(
    db: Session,
    *,
    limit: int,
    offset: int,
    status: str | None = None,
    q: str | None = None,
):
    qry = db.query(JobApplication).order_by(JobApplication.id.desc())
    qry = _apply_filters(qry, status=status, q=q)
    return qry.offset(offset).limit(limit).all()
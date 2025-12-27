from datetime import datetime
from enum import Enum
from fastapi import Depends, FastAPI, Form, Request, HTTPException
from fastapi import Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models, crud
from app.database import engine, get_db


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# -------------------------
# Pydantic Schemas (API)
# -------------------------
class JobStatus(str, Enum):
    Applied = 'Applied'
    Interview = 'Interview'
    Offer = 'Offer'
    Rejected = 'Rejected'


class JobApplicationOut(BaseModel):
    id: int
    company: str
    role: str
    status: JobStatus
    created_at: datetime
    updated_at: datetime  

    class Config:
        from_attributes = True  # allows returning SQLAlchemy objects directly


class JobApplicationCreate(BaseModel):
    company: str
    role: str
    status: JobStatus


class JobApplicationUpdate(BaseModel):
    company: str | None = None
    role: str | None = None
    status: JobStatus | None = None


class PaginatedJobApplications(BaseModel):
    items: list[JobApplicationOut]
    total: int
    limit: int
    offset: int
    has_more: bool


# -------------------------
# HTML Routes (UI)
# -------------------------
@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    job_applications = crud.get_applications(db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "job_applications": job_applications},
    )


@app.post("/applications")
def add_application(
    company: str = Form(...),
    role: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    crud.create_application(db, company=company, role=role, status=status)
    return RedirectResponse(url="/", status_code=303)


@app.post("/applications/{app_id}/edit")
def update_application_ui(
    app_id: int,
    company: str = Form(...),
    role: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    row = crud.update_application(
        db,
        app_id=app_id,
        company=company,
        role=role,
        status=status,
    )
    # UI: simple redirect even if missing
    return RedirectResponse(url="/", status_code=303)


@app.post("/applications/{app_id}/delete")
def delete_application_ui(app_id: int, db: Session = Depends(get_db)):
    crud.delete_application(db, app_id=app_id)
    return RedirectResponse(url="/", status_code=303)


# -------------------------
# API Routes (JSON)
# -------------------------
@app.get("/api/applications", response_model=list[JobApplicationOut])
def api_list_applications(db: Session = Depends(get_db)):
    return crud.get_applications(db)


@app.get('/api/applications/paged', response_model=PaginatedJobApplications)
def api_list_applications_paged(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description='Number of items to return'),
    offset: int = Query(0, ge=0, description='Number of items to skip'),
):
    total = crud.count_applications(db)
    items = crud.get_applications_page(db, limit=limit, offset=offset)
    has_more = (offset + limit) < total

    return {
        'items': items,
        'total': total,
        'limit': limit,
        'offset': offset,
        'has_more': has_more,
    }


@app.post("/api/applications", response_model=JobApplicationOut, status_code=201)
def api_create_application(payload: JobApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(
        db,
        company=payload.company,
        role=payload.role,
        status=payload.status,
    )


@app.patch("/api/applications/{app_id}", response_model=JobApplicationOut)
def api_update_application(app_id: int, payload: JobApplicationUpdate, db: Session = Depends(get_db)):
    row = crud.update_application(
        db,
        app_id=app_id,
        company=payload.company,
        role=payload.role,
        status=payload.status,
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return row


@app.delete("/api/applications/{app_id}", status_code=204)
def api_delete_application(app_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_application(db, app_id=app_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Application not found")
    return None




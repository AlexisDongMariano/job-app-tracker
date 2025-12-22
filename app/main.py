from app import models
from app.database import engine, get_db
from app.models import JobApplication

from fastapi import Depends, FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from pydantic import BaseModel


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.mount('/static', StaticFiles(directory='app/static'), name='static')
templates = Jinja2Templates(directory='app/templates')


# -------------------------
# Pydantic Schemas (API)
# -------------------------
class JobApplicationOut(BaseModel):
    id: int
    company: str
    role: str
    status: str

    class Config:
        from_attributes = True


class JobApplicationCreate(BaseModel):
    company: str
    role: str
    status: str


class JobApplicationUpdate(BaseModel):
    company: str | None = None
    role: str | None = None
    status: str | None = None


# -------------------------
# HTML Routes (UI)
# -------------------------
@app.get('/', response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    job_applications = (
        db.query(JobApplication)
        .order_by(JobApplication.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        'index.html',
        {
            'request': request, 
            'job_applications': job_applications
        },
    )


@app.post('/applications')
def add_application(
    company: str = Form(...),
    role: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    app_row = JobApplication(company=company, role=role, status=status)
    db.add(app_row)
    db.commit()
    return RedirectResponse(url='/', status_code=303)


@app.post('/applications/{app_id}/status')
def update_application_status_ui(
    app_id: int,
    status: str = Form(...),
    db: Session = Depends(get_db),
): 
    row = db.get(JobApplication, app_id)
    if row is None:
        return RedirectResponse(url='/', status_code=303)
    
    row.status = status
    db.commit()
    return RedirectResponse(url='/', status_code=303)


@app.post('/applications/{app_id}/delete')
def delete_application_ui(app_id: int, db: Session = Depends(get_db)):
    row = db.get(JobApplication, app_id)
    if row is None:
        return RedirectResponse(url='/', status_code=303)
    
    db.delete(row)
    db.commit()
    return RedirectResponse(url='/', status_code=303)


# -------------------------
# API Routes (JSON)
# -------------------------
@app.get('/api/applications', response_model=list[JobApplicationOut])
def api_list_applications(db: Session = Depends(get_db)):
    return (
        db.query(JobApplication)
        .order_by(JobApplication.id.desc())
        .all()
    )

@app.post("/api/applications", response_model=JobApplicationOut, status_code=201)
def api_create_application(payload: JobApplicationCreate, db: Session = Depends(get_db)):
    row = JobApplication(company=payload.company, role=payload.role, status=payload.status)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@app.patch("/api/applications/{app_id}", response_model=JobApplicationOut)
def api_update_application(app_id: int, payload: JobApplicationUpdate, db: Session = Depends(get_db)):
    row = db.get(JobApplication, app_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Application not found")

    if payload.company is not None:
        row.company = payload.company
    if payload.role is not None:
        row.role = payload.role
    if payload.status is not None:
        row.status = payload.status

    db.commit()
    db.refresh(row)
    return row


@app.delete("/api/applications/{app_id}", status_code=204)
def api_delete_application(app_id: int, db: Session = Depends(get_db)):
    row = db.get(JobApplication, app_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(row)
    db.commit()
    return None
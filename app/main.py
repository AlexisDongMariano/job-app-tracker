from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')

templates = Jinja2Templates(directory='app/templates')

job_applications = [{
        'company': 'company1',
        'role': 'role1',
        'status': 'job offer'
    }]

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
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
):
    job_applications.append(
        {
            'company': company,
            'role': role,
            'status': status,
        }
    )
    return RedirectResponse(url='/', status_code=303)
    
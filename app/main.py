from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')

templates = Jinja2Templates(directory='app/templates')

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    job_applications = [{
        'company': 'company1',
        'role': 'role1',
        'status': 'job offer'
    }]
    return templates.TemplateResponse(
        'index.html',
        {'request': request, 'job_applications': job_applications},
    )
    
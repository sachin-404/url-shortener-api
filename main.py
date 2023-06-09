from fastapi import FastAPI, Request, Form, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
import validators
from configs import schemas, models
from configs.database import engine, SessionLocal
from src import crud
from starlette.datastructures import URL

BASE_URL: str = "http://localhost:8000"

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

def raise_exception(error_message):
    raise HTTPException(status_code=400, detail=error_message)

def raise_url_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(BASE_URL)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key = db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


@app.get("/")
async def index(request: Request):
    return "helloooooo"
    # return templates.TemplateResponse("index.html", {"request": request})

@app.post("/input_url", response_model=schemas.URLInfo)
async def input_url(url: schemas.URLBase, db: SessionLocal() = Depends(get_db)):
    if not validators.url(url.input_url):
        raise_exception("Entered URL is not valid")
    db_url = crud.create_db_url(url, db)
    return get_admin_info(db_url)

@app.get("/{url_key}")
async def redirect_to_url(request: Request, url_key: str, db:SessionLocal() = Depends(get_db)):
    db_url = crud.get_db_url_by_key(db=db, key=url_key)
    if db_url:
        return RedirectResponse(db_url.input_url)
    else:
        raise_url_not_found(request)
        
@app.get("/admin/{secret_key}", name="administration info", response_model=schemas.URLInfo)
async def get_url_info(request: Request, secret_key: str, db: SessionLocal() = Depends(get_db)):
    db_url = crud.get_db_url_by_secret_key(db, secret_key)
    if db_url:
        return get_admin_info(db_url)
    else:
        raise_url_not_found(request)
        
    

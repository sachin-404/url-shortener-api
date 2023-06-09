from fastapi import FastAPI, Request, Form, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
import validators
from configs import schemas, models
from configs.database import engine, SessionLocal
from src import crud

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


@app.get("/")
async def index(request: Request):
    return "helloooooo"
    # return templates.TemplateResponse("index.html", {"request": request})

@app.post("/input_url", response_model=schemas.URLInfo)
async def input_url(url: schemas.URLBase, db: SessionLocal() = Depends(get_db)):
    if not validators.url(url.input_url):
        raise_exception("Entered URL is not valid")
    db_url = crud.create_db_url(url, db)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key
    
    return db_url

@app.get("/{url_key}")
async def redirect_to_url(request: Request, url_key: str, db:SessionLocal() = Depends(get_db)):
    db_url = crud.get_db_url_by_key(db=db, key=url_key)
    if db_url:
        return RedirectResponse(db_url.input_url)
    else:
        raise_url_not_found(request)
    

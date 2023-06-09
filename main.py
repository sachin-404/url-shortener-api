from fastapi import FastAPI, Request, Form, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
import validators
from configs import schemas, models
from configs.database import engine, SessionLocal
import secrets

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

def raise_url_not_found(error_message):
    raise HTTPException(status_code=400, detail=error_message)

@app.get("/")
async def index(request: Request):
    return "helloooooo"
    # return templates.TemplateResponse("index.html", {"request": request})

@app.post("/input_url", response_model=schemas.URLInfo)
async def input_url(url: schemas.URLBase, db: SessionLocal() = Depends(get_db)):
    if not validators.url(url.input_url):
        raise_exception("Entered URL is not valid")
    
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(
        input_url=url.input_url, key=key, secret_key=secret_key
    )
    
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key
    
    return db_url

@app.get("/{url_key}")
async def redirect_to_url(request: Request, url_key: str, db:SessionLocal() = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.key == url_key, models.URL.is_active).first()
    if db_url:
        return RedirectResponse(db_url.input_url)
    else:
        raise_url_not_found("Provided URL doesnt exist!!")
    

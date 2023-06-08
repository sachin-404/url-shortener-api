from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
import validators
from src import schemas

app = FastAPI()

templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

def raise_exception(error_message):
    raise HTTPException(status_code=400, detail=error_message)

@app.get("/")
async def index(request: Request):
    return "helloooooo"
    # return templates.TemplateResponse("index.html", {"request": request})

@app.post("/input_url")
async def url_input(url: schemas.BaseModel):
    if not validators.url(url.target_url):
        return raise_exception("Entered URL is not valid")
    return url
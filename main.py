from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/url_input", response_class= HTMLResponse)
async def url_input(request: Request, url_input: str = Form(default=None)):
    if url_input is not None and url_input.strip() != "":
        print(url_input)
    return templates.TemplateResponse("index.html", {"request": request, "url_input": url_input})
    
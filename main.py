from typing import Optional
from fastapi import FastAPI, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
films = [
    {
      "name": "Blade Runner",
      "director": "Ridley Scott",
    },
    {
      "name": "The Matrix",
      "director": "The Wachowskis",
    },
    {
      "name": "The Matrix Reloaded",
      "director": "The Wachowskis",
    },
    {
      "name": "Harry Potter",
      "director": "Chris Columbus",
    }
    ]
@app.get("/", response_class=HTMLResponse)
async def index(request: Request, hx_request: Optional[str] = Header(None)):
    context={
      "request": request,
      "films": films
    }
    if hx_request:
        return templates.TemplateResponse("components/moviesTable.html", context)
    return templates.TemplateResponse("index.html", context)

@app.get("/load-more", response_class=HTMLResponse)
async def load_more(request: Request):
    return templates.TemplateResponse("components/moviesTable.html", 
    {
      "request": request,
      "films": films
    })

@app.post("/new-film", response_class=HTMLResponse)
async def new_film(request: Request):
    data = await request.form()
    films.append({
        "name": data["name"],
        "director": data["director"]
    })
    return templates.TemplateResponse("components/moviesTable.html", 
    {
      "request": request,
      "films": films
    })
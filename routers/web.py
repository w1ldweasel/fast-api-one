from fastapi import APIRouter, Request, Form, Depends#, Cookie
from sqlmodel import Session
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db import get_session
from routers.cars import get_cars

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

"""
<html>
    <head>
        <title>Carsharing Demo</title>
    </head>
    <body>
        <h1>Welcome to the Car Sharing service</h1>
        <p> Here is some text for you</p>
    </body>

</html>
"""

#Use of star below turns everything coming after it in arguments into key word pairs so order doesn't matter, wanted to see params in order seen by user
#whereas python normally wants arguments without defaults to appear first
# Form(...) tells python to use form param
#the 3 dots are part of python ellipsis class
@router.post("/search", response_class=HTMLResponse)
def search(*, size: str = Form(...), doors: int = Form(...),
           request: Request,
           session: Session = Depends(get_session)):
    cars = get_cars(size=size, doors=doors, session=session)
    return templates.TemplateResponse("search_results.html",
                                      {"request": request, "cars": cars})
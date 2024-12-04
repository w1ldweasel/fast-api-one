from fastapi import APIRouter #Request, Form, Depends, Cookie
#from sqlmodel import Session
from starlette.responses import HTMLResponse
#from fastapi.templating import Jinja2Templates

#from db import get_session
#from routers.cars import get_cars

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home():
    return """
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

import uvicorn
from fastapi import FastAPI, Request
from sqlmodel import SQLModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from db import engine
from routers import cars, web
from routers.cars import BadTripException

app = FastAPI(title='Car Sharing')
app.include_router(web.router)
app.include_router(cars.router)

#db = load_db()

@app.on_event("startup") #"startup" value means as name says, tells FastAPI this is first action performed before any client requests processed. Create DB on startup
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.exception_handler(BadTripException)
async def unicorn_exception_handler(request: Request, exc: BadTripException):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Bad Trip"},

    )

if __name__ =='__main__':
    uvicorn.run("carsharing:app", reload=True)

from fastapi import FastAPI
from sqlmodel import SQLModel
from db import engine
import uvicorn

from routers import cars, web

app = FastAPI(title='Car Sharing')
app.include_router(web.router)
app.include_router(cars.router)

#db = load_db()

@app.on_event("startup") #"startup" value means as name says, tells FastAPI this is first action performed before any client requests processed. Create DB on startup
def on_startup():
    SQLModel.metadata.create_all(engine)


if __name__ =='__main__':
    uvicorn.run("carsharing:app", reload=True)

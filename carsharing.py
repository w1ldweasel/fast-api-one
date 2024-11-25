from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime
from sqlmodel import SQLModel, create_engine, Session, select

from schemas import CarInput, CarOutput, TripOutput, TripInput, Car, Trip
import uvicorn


app = FastAPI(title='Car Sharing')
#db = load_db()

engine = create_engine(
    sqlite:///carsharing.db", 
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=True  # Log generated SQL
)


@app.on_event("startup") #"startup" value means as name says, tells FastAPI this is first action performed before any client requests processed
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")#decorator to turn function below into path operation
def welcome(name):
    """Return a welcome message."""
    return {'message': f"Welcome, {name}, to the Car Sharing service"}

@app.get('/date')
def date():
    """Return current time"""
    return {'date': datetime.now()}

def get_session():
    #return Session(engine)
    with Session(engine) as session:
        yield session

#Add an operation called get_cars()
#Served at /api/cars
#Returns all car data

@app.get('/api/cars')
def get_cars(size: str|None = None, doors: int|None = None, session: Session = Depends(get_session)) -> list:
    # Before Python 3.10, this way of using pipe symbol not available, upper case L for List obj
    # def get_cars(size: Optional[str] = None, doors: Optional[str] = None) -> List:
    '''By default, query parameters are required 
    Make them optional by specifying a default value, can be any value as long as it matches required type, e.g. m or 5 in this case
    Don't forget to make the type hint accept None as well, e.g. in this case it won't work with int hence need to use pipe
    '''
    
    #with Session(engine) as session: - no longer required, replaced with above dependency injection, done in typehint arg
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors >= doors)

    return session.exec(query).all()#all returns all python objects

@app.get('/api/cars/{id}', response_model=CarOutput) 
def car_by_id(id: int, session: Session = Depends(get_session)):# -> dict pydantic change from car dict to car obj 
    car = session.get(Car, id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f'No car with id = {id}.' )

@app.post('/api/cars/', response_model=Car)
def add_car(car_input: CarInput, session: Session = Depends(get_session)) -> Car:
    #with Session(engine) as session:
    new_car = Car.from_orm(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car

@app.delete('/api/cars/{id}', status_code=204)
def remove_car(id: int, session: Session = Depends(get_session)) -> None:
    car = session.get(car, id)
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f'No car with id={id}.')

@app.put('/api/cars/{id}', response_model=CarOutput)
def change_car(id: int, new_data: CarInput, session: Session = Depends(get_session))-> Car:
    car = session.get(Car, id)
    if car:
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        session.commit()
        return car
    else:
        raise HTTPException(status_code=404, detail=f'No car with id={id}.')
    
    
@app.post("/api/cars/{car_id}/trips", response_model=Trip)
def add_trip(car_id: int, trip_input: TripInput, session: Session = Depends(get_session)) -> Trip:
    car = session.get(Car, car_id)
    if car:
        new_trip = Trip.from_orm(trip_input, update={'car_id': car_id})
        car.trips.append(new_trip)
        session.commit()
        session.refresh(new_trip)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")

if __name__ =='__main__':
    uvicorn.run("carsharing:app", reload=True)

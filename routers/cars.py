from fastapi import Depends, HTTPException, APIRouter
from datetime import datetime
from sqlmodel import Session, select

from db import get_session
from schemas import Car, CarInput, CarOutput, Trip, TripInput

router = APIRouter(prefix="/api/cars")
#using this prefix allows removal of this url from all the operators that had it before, below

#Original replaced by web.py get request
'''@router.get("/")#decorator to turn function below into path operation
def welcome(name):
    """Return a welcome message."""
    return {'message': f"Welcome, {name}, to the Car Sharing service"}
'''

@router.get('/date')
def date():
    """Return current time"""
    return {'date': datetime.now()}

#Add an operation called get_cars()
#Served at /api/cars
#Returns all car data

@router.get('/')
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

@router.get('/{id}', response_model=CarOutput) 
def car_by_id(id: int, session: Session = Depends(get_session)):# -> dict pydantic change from car dict to car obj 
    car = session.get(Car, id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f'No car with id = {id}.' )

@router.post('/', response_model=Car)
def add_car(car_input: CarInput, session: Session = Depends(get_session)) -> Car:
    #with Session(engine) as session:
    new_car = Car.from_orm(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car

@router.delete('/{id}', status_code=204)
def remove_car(id: int, session: Session = Depends(get_session)) -> None:
    car = session.get(car, id)
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f'No car with id={id}.')

@router.put('/{id}', response_model=CarOutput)
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
    
    
@router.post("/{car_id}/trips", response_model=Trip)
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
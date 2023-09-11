from fastapi import FastAPI, HTTPException
from datetime import datetime

from schemas import load_db, save_db, CarInput, CarOutput, TripOutput, TripInput
import uvicorn


app = FastAPI(title='Car Sharing')
db = load_db()

@app.get("/")#decorator to turn function below into path operation
def welcome(name):
    """Return a welcome message."""
    return {'message': f"Welcome, {name}, to the Car Sharing service"}

@app.get('/date')
def date():
    """Return current time"""
    return {'date': datetime.now()}

#Add an operation called get_cars()
#Served at /api/cars
#Returns all car data

@app.get('/api/cars')
def get_cars(size: str|None = None, doors: int|None = None) -> list:
    # Before Python 3.10, this way of using pipe symbol not available, upper case L for List obj
    # def get_cars(size: Optional[str] = None, doors: Optional[str] = None) -> List:
    '''By default, query parameters are required 
    Make them optional by specifying a default value, can be any value as long as it matches required type, e.g. m or 5 in this case
    Don't forget to make the type hint accept None as well, e.g. in this case it won't work with int hence need to use pipe
    '''
    result = db
    if size:
        result = [car for car in result if car.size == size]
        
    if doors:
        result = [car for car in result if car.doors >= doors]

    return result

@app.get('/api/cars/{id}') 
def car_by_id(id: int):# -> dict pydantic change from car dict to car obj 
    result = [car for car in db if car.id == id]

    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail=f'No car with id = {id}.' )

@app.post('/api/cars/', response_model=CarOutput)
def add_car(car: CarInput) -> CarOutput:
    new_car = CarOutput(size=car.size, doors=car.doors, fuel=car.fuel, transmission=car.transmission, id=len(db)+1)
    db.append(new_car)
    save_db(db)
    return new_car

@app.delete('/api/cars/{id}', status_code=204)
def remove_car(id: int) -> None:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=404, detail=f'No car with id={id}.')

@app.put('/api/cars/{id}', response_model=CarOutput)
def change_car(id: int, new_data: CarInput)-> CarOutput:
    matches = [car for car in db if car.id == id]
    if matches:
        car=matches[0]
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        save_db(db)
        return car
    else:
        raise HTTPException(status_code=404, detail=f'No car with id={id}.')
    
    
@app.post("/api/cars/{car_id}/trips", response_model=TripOutput)
def add_trip(car_id: int, trip: TripInput) -> TripOutput:
    matches = [car for car in db if car.id == car_id]
    if matches:
        car = matches[0]
        new_trip = TripOutput(id=len(car.trips)+1, start=trip.start, end=trip.end, description=trip.description)
        car.trips.append(new_trip) 
        save_db(db)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")

if __name__ =='__main__':
    uvicorn.run("carsharing:app", reload=True)

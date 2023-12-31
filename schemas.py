import json
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

class TripInput(BaseModel):
    start: int
    end: int
    description: str

class TripOutput(TripInput):
    id: int

'''class Trip(TripInput, table=True):
    id: int | None = Field(default=None, primary_key=True)
    car_id: int = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="trips")'''

class CarInput(BaseModel):
    size: str
    fuel: str | None = 'electric'
    doors: int
    transmission: str | None = "auto"

    class Config:
        json_schema_extra = {
            "example": {
                "size": "m",
                "doors": 5,
                "transmission": "manual",
                "fuel": "hybrid"
            }
        }
class CarOutput(CarInput):
    id: int
    size: str
    fuel: str | None = 'electric'
    doors: int
    transmission: str | None = "auto"
    trips: list[TripOutput] = []


def load_db() -> list[CarOutput]:
    '''Load a list of Car objects from a JSON file'''
    with open('cars.json') as f:
        return [CarOutput.parse_obj(obj) for obj in json.load(f)]
    
def save_db(cars: list[CarOutput]):
    with open('cars.json', 'w') as f:
        json.dump([car.dict() for car in cars], f, indent=4 )
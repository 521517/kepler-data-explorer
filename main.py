from fastapi import FastAPI
from get_data_from_nasa import process_nasa_data
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class PlanetData(BaseModel):
    planet_number: int
    orbit: str
    size: str
    temperature: str
    sunlight_received: str
    transit_duration: str
    transit_depth: str
    detection_snr: float
    impact_parameter: float
    interesting_features: List[str]

class KeplerSystemData(BaseModel):
    star_system: str
    number_of_planets: int
    star_temperature: str
    star_size: str
    star_mass: Optional[str]
    star_age: Optional[str]
    ra_dec: str
    potential_planets: List[PlanetData]
    system_note: Optional[str] = None
    discovery_date: str
    last_update: str
    smart_summary: str  # New field

@app.get("/")
async def root():
    return {"message": "Welcome to the Kepler Data API"}

@app.get("/kepler/{kepid}", response_model=KeplerSystemData)
async def get_kepler_data(kepid: int):
    return process_nasa_data(kepid)
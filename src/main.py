from datetime import datetime
import os

from fastapi import FastAPI, Query
from pydantic import BaseModel

from loguru import logger

app = FastAPI()

CACHE_DIR = os.getenv("CACHE_DIR", "/tmp/taxi-data-api")
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

class Trip(BaseModel):
    tpep_pickup_datetime: datetime
    tpep_dropoff_datetime: datetime
    trip_distance: float
    fare_amount: float

class TripsResponse(BaseModel):
    trips: list[Trip]
    next_from_ms: int

@app.get("/trips", response_model=TripsResponse)
async def get_trip(
    from_ms: int = Query(..., description="Unix milliseconds"),
    n_results: int = Query(100, description="Number of results to output")
):
    # Log the received parameters
    logger.info(f"Received from_ms: {from_ms}, n_results: {n_results}")

    from src.utils import get_year_and_month
    year, month = get_year_and_month(from_ms)
    logger.info(f"Extracted year: {year}, month: {month}")
    
    from src.taxi_data import read_parquet_file
    df = read_parquet_file(year, month)
    
    # add column with tpep_pickup_datetime as unix milliseconds
    df["tpep_pickup_datetime_ms"] = df["tpep_pickup_datetime"].astype(int)
    
    # filter df to only include rows where tpep_pickup_datetime_ms is greater than from_ms
    df = df[df["tpep_pickup_datetime_ms"] > from_ms]
    
    # get the first n_results rows
    df = df.head(n_results)
    
    # convert df to list of Trip
    trips = df.to_dict(orient="records")
    trips = [Trip(**trip) for trip in trips]

    # get the next from_ms
    next_from_ms = int(trips[-1].tpep_pickup_datetime.timestamp() * 1000)

    return TripsResponse(trips=trips, next_from_ms=next_from_ms)
from typing import Optional

from fastapi import FastAPI, Query
from loguru import logger
from pydantic import BaseModel

from src.backend import Trip, get_trips

app = FastAPI()


class TripsResponse(BaseModel):
    trips: Optional[list[Trip]] = None
    next_from_ms: Optional[int] = None
    message: Optional[str] = None


@app.get('/trips', response_model=TripsResponse)
def get_trip(
    from_ms: int = Query(..., description='Unix milliseconds'),
    n_results: int = Query(100, description='Number of results to output'),
):
    # Log the received parameters
    logger.info(
        f'Received request with params from_ms: {from_ms}, n_results: {n_results}'
    )

    # get the trips from the backend
    trips: list[Trip] = get_trips(from_ms, n_results)

    # format the response object TripsResponse
    if len(trips) > 0:
        return TripsResponse(
            trips=trips,
            next_from_ms=trips[-1].tpep_pickup_datetime_ms,
            message=f'Success. Returned {len(trips)} trips.',
        )
    else:
        return TripsResponse(message='No trips found for the given time range.')


@app.get('/health')
def health_check():
    return {'status': 'healthy!'}

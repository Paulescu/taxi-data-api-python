import os
from datetime import datetime
from typing import Optional

import pandas as pd
import requests
from loguru import logger
from pydantic import BaseModel

CACHE_DIR = os.getenv('CACHE_DIR', '/tmp/taxi-data-api-python/')
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


class Trip(BaseModel):
    tpep_pickup_datetime: datetime
    tpep_dropoff_datetime: datetime
    trip_distance: float
    fare_amount: float

    @property
    def tpep_pickup_datetime_ms(self) -> int:
        return int(self.tpep_pickup_datetime.timestamp() * 1000)


def get_trips(from_ms: int, n_results: int) -> list[Trip]:
    """
    Returns a list of sorted trips from the given from_ms timestamp, with a maximum of n_results.
    The trips are returned in chronological order.

    Args:
        from_ms: The timestamp in milliseconds to start the search from.
        n_results: The maximum number of results to return.

    Returns:
        A list of trips.
    """
    from src.utils import get_year_and_month

    year, month = get_year_and_month(from_ms)
    logger.info(f'Extracted year: {year}, month: {month}')

    # load parquet file with the data
    df: Optional[pd.DataFrame] = read_parquet_file(year, month)

    if df is None:
        logger.info(f'No trips found for the given year: {year}, month: {month}')
        return []

    # Convert datetime to Unix timestamp in milliseconds
    df['tpep_pickup_datetime_ms'] = (
        df['tpep_pickup_datetime'].astype(int) / 10**3
    ).astype(int)

    # filter df to only include rows where tpep_pickup_datetime_ms is greater than from_ms
    df = df[df['tpep_pickup_datetime_ms'] > from_ms]

    # get the first n_results rows
    df = df.head(n_results)

    # convert df to list of Trip
    trips = df.to_dict(orient='records')
    trips = [Trip(**trip) for trip in trips]

    return trips


def download_parquet_file(year: int, month: int):
    """
    Download the parquet file for the given year and month from the NYC Taxi and Limousine Commission.

    https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

    Args:
        year: The year to download the file for.
        month: The month to download the file for.
    """
    # URL to download the file from
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet'

    # Download the file
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'{CACHE_DIR}/yellow_tripdata_{year}-{month:02d}.parquet', 'wb') as f:
            f.write(response.content)
        logger.info(f'Downloaded file: yellow_tripdata_{year}-{month:02d}.parquet')
    else:
        logger.info(f'Failed to download file: {response.status_code}')


def read_parquet_file(year: int, month: int) -> Optional[pd.DataFrame]:
    """
    Read the parquet file for the given year and month.

    Args:
        year: The year to read the file for.
        month: The month to read the file for.

    Returns:
        A pandas DataFrame with the data, or None if the file couldn't be read.
    """
    # check if the file exists
    if not os.path.exists(f'{CACHE_DIR}/yellow_tripdata_{year}-{month:02d}.parquet'):
        logger.info(f'File not found: yellow_tripdata_{year}-{month:02d}.parquet')
        logger.info(f'Downloading file: yellow_tripdata_{year}-{month:02d}.parquet')
        download_parquet_file(year, month)

    logger.info(f'Reading file: yellow_tripdata_{year}-{month:02d}.parquet')
    try:
        df = pd.read_parquet(
            f'{CACHE_DIR}/yellow_tripdata_{year}-{month:02d}.parquet', engine='pyarrow'
        )
    except Exception as e:
        logger.info(f'Failed to read file: {e}')
        return None

    # filter the df to only include the columns we need
    df = df[
        [
            'tpep_pickup_datetime',
            'tpep_dropoff_datetime',
            'trip_distance',
            'fare_amount',
        ]
    ]

    # filter rows where tpep_pickup_datetime is in that year and month
    df = df[df['tpep_pickup_datetime'].dt.year == year]
    df = df[df['tpep_pickup_datetime'].dt.month == month]

    # sort the df by tpep_pickup_datetime
    df = df.sort_values(by='tpep_pickup_datetime')

    return df


if __name__ == '__main__':
    # used for debugging purposes
    # import argparse

    # # argparse
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--year", type=int, required=True)
    # parser.add_argument("--month", type=int, required=True)
    # args = parser.parse_args()

    # df = read_parquet_file(args.year, args.month)

    # # df = read_parquet_file(2023, 2)
    # print(df.head())
    # print(df.tail())

    trips = get_trips(from_ms=1674561748000, n_results=100)

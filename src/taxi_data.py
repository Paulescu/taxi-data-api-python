import os

import pandas as pd
from loguru import logger
import requests

CACHE_DIR = os.getenv("CACHE_DIR", "/tmp/taxi-data-api-python/")
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def download_parquet_file(year: int, month: int):
    """
    Download the parquet file for the given year and month.
    """
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"
    
    """
    https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet
    https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-02.parquet
    """
    # Download the file
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"{CACHE_DIR}/yellow_tripdata_{year}-{month:02d}.parquet", "wb") as f:
            f.write(response.content)
        logger.info(f"Downloaded file: yellow_tripdata_{year}-{month:02d}.parquet")
    else:
        raise Exception(f"Failed to download file: {response.status_code}")

def read_parquet_file(year: int, month: int):
    """
    Read the parquet file for the given year and month.
    """
    # check if the file exists
    if not os.path.exists(f"{CACHE_DIR}/yellow_tripdata_{year}-{month:02d}.parquet"):
        logger.info(f"File not found: yellow_tripdata_{year}-{month:02d}.parquet")
        logger.info(f"Downloading file: yellow_tripdata_{year}-{month:02d}.parquet")
        download_parquet_file(year, month)

    logger.info(f"Reading file: yellow_tripdata_{year}-{month:02d}.parquet")
    df = pd.read_parquet(f"{CACHE_DIR}/yellow_tripdata_{year}-{month:02d}.parquet", engine='pyarrow')
    
    # filter the df to only include the columns we need
    df = df[["tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_distance", "fare_amount"]]
    
    # filter rows where tpep_pickup_datetime is in that year and month
    df = df[df["tpep_pickup_datetime"].dt.year == year]
    df = df[df["tpep_pickup_datetime"].dt.month == month]

    # sort the df by tpep_pickup_datetime
    df = df.sort_values(by="tpep_pickup_datetime")

    return df

if __name__ == "__main__":

    import argparse
    
    # argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--month", type=int, required=True)
    args = parser.parse_args()

    df = read_parquet_file(args.year, args.month)
    
    # df = read_parquet_file(2023, 2)
    print(df.head())
    print(df.tail())


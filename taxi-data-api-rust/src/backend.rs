use chrono::{DateTime, Utc, Datelike};    
use serde::Serialize;
use log::{info, error};
use anyhow::Result;
use polars::prelude::*;

#[derive(Debug, Serialize)]
pub struct Trip {
    tpep_pickup_datetime: DateTime<Utc>,
    tpep_dropoff_datetime: DateTime<Utc>,
    trip_distance: f64,
    fare_amount: f64,
}

#[allow(dead_code)]
fn get_fake_trips() -> Vec<Trip> {
    let one_trip = Trip {
        tpep_pickup_datetime: Utc::now(),
        tpep_dropoff_datetime: Utc::now(),
        trip_distance: 0.0,
        fare_amount: 0.0,
    };
    vec![one_trip]
}

/// Reads taxi trip data from a parquet file and returns a vector of Trip structs
/// 
/// # Arguments
/// 
/// * `file_path` - Path to the parquet file containing taxi trip data
/// * `from_ms` - Unix timestamp in milliseconds to filter trips after this time
/// * `n_results` - Maximum number of trips to return
/// 
/// # Returns
/// 
/// Returns a Result containing a Vec of Trip structs if successful, or an error if the
/// file cannot be read or the data is invalid
fn get_trips_from_file(
    file_path: &str, 
    from_ms: i64, 
    n_results: i64
) -> Result<Vec<Trip>> {

    let df = LazyFrame::scan_parquet(file_path, Default::default())?
        .select([
            col("tpep_pickup_datetime"),
            col("tpep_dropoff_datetime"),
            col("trip_distance"),
            col("fare_amount"),
        ])
        .filter(col("tpep_pickup_datetime").gt_eq(lit(from_ms * 1_000_000)))
        .sort("tpep_pickup_datetime", Default::default())
        .limit(n_results as u32)
        .collect()?;
    
    let pickup_series = df
        .column("tpep_pickup_datetime")?
        .datetime()
        .expect("pickup datetime column should be datetime type");
    
    let dropoff_series = df
        .column("tpep_dropoff_datetime")?
        .datetime()
        .expect("dropoff datetime column should be datetime type");
    
    let distance_series = df
        .column("trip_distance")?
        .f64()
        .expect("distance column should be f64 type");
    
    let fare_series = df
        .column("fare_amount")?
        .f64()
        .expect("fare column should be f64 type");

    // Convert to Vec<Trip>
    let trips: Vec<Trip> = (0..df.height()).map(|i| {
        Trip {
            tpep_pickup_datetime: DateTime::<Utc>::from_timestamp_nanos(pickup_series.get(i).unwrap()),
            tpep_dropoff_datetime: DateTime::<Utc>::from_timestamp_nanos(dropoff_series.get(i).unwrap()),
            trip_distance: distance_series.get(i).unwrap(),
            fare_amount: fare_series.get(i).unwrap(),     
        }
    })
    .collect();

    Ok(trips)
}

pub async fn get_trips(from_ms: i64, n_results: i64) -> Result<Vec<Trip>> {
    
    let (year, month) = get_year_and_month(from_ms);
    info!("Extracted year: {}, month: {}", year, month);

    // Download the parquet file
    info!("Downloading parquet file for year: {}, month: {}", year, month);
    let file_path = download_parquet_file(year, month).await?;

    // Get the trips from the file
    let trips = get_trips_from_file(&file_path, from_ms, n_results)?;

    // TODO: Fake data for now
    // let trips = get_fake_trips();

    info!("Returning {} trips", trips.len());
    Ok(trips)
}

pub async fn download_parquet_file(year: i32, month: i32) -> Result<String> {
    
    let url = format!(
        "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{}-{:02}.parquet", 
        year,
        month
    );
    let file_path = format!("yellow_tripdata_{}-{:02}.parquet", year, month);

    // Check if the file already exists. If it does, return the file path.
    if tokio::fs::try_exists(&file_path).await? {
        info!("File {} already exists", &file_path);
        return Ok(file_path);
    }

    info!("Downloading file from {}", &url);
    let response = reqwest::get(&url).await?;
    if response.status().is_success() {

        let bytes = response.bytes().await?;

        // async copy of bytes to file
        tokio::fs::write(&file_path, bytes).await?;
        
        info!("File {} downloaded successfully", &file_path);
    } else {
        error!("Failed to download file");
    }
    Ok(file_path)
}

pub fn get_year_and_month(from_ms: i64) -> (i32, i32) {
    let datetime = DateTime::<Utc>::from_timestamp(from_ms / 1000, 0).unwrap();
    (datetime.year(), datetime.month() as i32)
}

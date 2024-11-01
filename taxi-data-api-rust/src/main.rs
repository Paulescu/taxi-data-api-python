use actix_web::{App, HttpServer, web, HttpResponse};
use log::{info, error};
use std::env;
use serde::Deserialize;
use env_logger::Env;

mod backend;
use crate::backend::{get_trips, get_fake_trips};

async fn health() -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "status": "healthy",
        "timestamp": chrono::Utc::now().to_rfc3339()
    }))
}

#[derive(Deserialize)]
struct TripsQuery {
    from_ms: i64,
    n_results: i64
}

async fn trips(query: web::Query<TripsQuery>) -> HttpResponse {
    match get_fake_trips(query.from_ms, query.n_results).await {
        Ok(trips) => HttpResponse::Ok().json(trips),
        Err(e) => HttpResponse::InternalServerError().body(e.to_string())
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {

    // Initialize the logger
    env_logger::init_from_env(Env::new().default_filter_or("info"));

    let port = env::var("PORT")
        .unwrap_or_else(|_| "8080".to_string())
        .parse::<u16>()
        .expect("PORT must be a valid number");
    
    info!("Starting server on port {}", port);

    HttpServer::new(|| {
        App::new()
            .wrap(actix_web::middleware::Logger::default())
            .route("/health", web::get().to(health))
            .route("/trips", web::get().to(trips))
    })
    .bind(("0.0.0.0", port))?
    .run()
    .await.map_err(|e| {
        error!("Error starting server: {}", e);
        e
    })
}
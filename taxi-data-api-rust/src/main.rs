use actix_web::{App, HttpServer, web, HttpResponse};
use log::{info, error};
use std::env;
use env_logger::Env;

async fn health() -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "status": "healthy",
        "timestamp": chrono::Utc::now().to_rfc3339()
    }))
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
    })
    .bind(("0.0.0.0", port))?
    .run()
    .await.map_err(|e| {
        error!("Error starting server: {}", e);
        e
    })
}
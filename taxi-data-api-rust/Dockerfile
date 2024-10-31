### Build stage
FROM rust:1.76-slim as builder
WORKDIR /usr/src/app
# Install OpenSSL development packages for compilation
RUN apt-get update && \
    apt-get install -y pkg-config libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy only the necessary files for building
COPY Cargo.toml Cargo.lock ./
COPY src src/

# Build the application
RUN cargo build --release


### Runtime stage
FROM debian:bookworm-slim
WORKDIR /usr/local/bin
COPY --from=builder /usr/src/app/target/release/taxi-data-api-rust .
RUN apt-get update && apt-get install -y libssl-dev ca-certificates && rm -rf /var/lib/apt/lists/*

# Run as non-root user for better security
# RUN useradd -m myapp
# USER myapp

EXPOSE 8080
CMD ["./taxi-data-api-rust"]
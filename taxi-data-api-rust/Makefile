export PORT=8089

# Runs the API locally
run-dev:
	cargo run

# Commands to check the API works as expected when running locally
health-check-local:
	curl -X GET "http://localhost:$(PORT)/health"

sample-request-local:
	curl -X GET "http://localhost:$(PORT)/trips?from_ms=1714204800000&n_results=100"

sample-request-no-results-local:
	curl -X GET "http://localhost:$(PORT)/trips?from_ms=1727430298000&n_results=100"

build:
	docker build -t taxi-data-api-rust .

run: build
	docker run -p $(PORT):8080 taxi-data-api-rust
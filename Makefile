run-dev:
	poetry run uvicorn src.api:app --reload --port $${PORT:-8090}

build-naive:
	@echo "Building naive image"
	@time docker build -f Dockerfile.naive -t taxi-data-api-python:naive-build .

	@echo "Naive image size"
	@docker images --format "{{.Size}}" taxi-data-api-python:naive-build

build-single-stage:
	@echo "Building single-stage image"
	@time docker build -f Dockerfile.1stage -t taxi-data-api-python:single-stage-build .

	@echo "Single-stage image size"
	@docker images --format "{{.Size}}" taxi-data-api-python:single-stage-build

build-multi-stage:
	@echo "Building multi-stage image"
	@time docker build -f Dockerfile.2stage -t taxi-data-api-python:multi-stage-build .

	@echo "Multi-stage image size"
	@docker images --format "{{.Size}}" taxi-data-api-python:multi-stage-build

build: build-multi-stage

run:
	docker run -p $${PORT:-8090}:8000 taxi-data-api-python:multi-stage-build

lint:
	poetry run ruff check --fix .

format:
	poetry run ruff format .

all: lint format build run

health-check:
	curl -X GET "http://localhost:$${PORT:-8090}/health"

sample-request:
	curl -X GET "http://localhost:$${PORT:-8090}/trips?from_ms=1674561748000&n_results=100"

sample-request-no-results:
	curl -X GET "http://localhost:$${PORT:-8090}/trips?from_ms=1727430298000&n_results=100"

check-image-sizes:
	docker images --format "{{.Size}}" taxi-data-api-python:single-stage-build

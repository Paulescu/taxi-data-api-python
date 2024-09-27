run-dev:
	poetry run uvicorn src.api:app --reload --port ${PORT}

build:
	docker build -t taxi-data-api-python .

run:
	docker run -p ${PORT}:8000 taxi-data-api-python

lint:
	poetry run ruff check --fix .

format:
	poetry run ruff format .

all: lint format build run

sample-request:
	curl -X GET "http://localhost:${PORT}/trips?from_ms=1674561748000&n_results=100"

sample-request-no-results:
	curl -X GET "http://localhost:${PORT}/trips?from_ms=1727430298000&n_results=100"
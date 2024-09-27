run-dev:
	poetry run uvicorn src.main:app --reload --port 8085

build:
	docker build -t taxi-data-api-python .

run:
	docker run -p 8085:8000 taxi-data-api-python

all: build run

request-1:
	curl -X GET "http://localhost:8085/trips?from_ms=1674561748000&n_results=100"

# request-2:
# 	curl -X GET "http://localhost:8081/trip?from_ms=1704070676000"

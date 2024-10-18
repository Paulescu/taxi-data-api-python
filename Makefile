# feel free to change the PORT value if you have another service running on port 8092
export PORT=8095

install:
	@echo "Downloading and installing Python Poetry"
	curl -sSL https://install.python-poetry.org | python3 -
	poetry env use $(shell which python3.10)
	poetry install

run-dev:
	poetry run uvicorn src.api:app --reload --port $(PORT)

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

run: build
	docker run \
		-e ELASTICSEARCH_HOST=http://elasticsearch:9200 \
		-e ELASTICSEARCH_INDEX=taxi_data_api \
		--network elasticsearch \
		-p $(PORT):8000 \
		taxi-data-api-python:multi-stage-build

test:
	poetry run pytest tests/

lint:
	poetry run ruff check --fix .

format:
	poetry run ruff format .

all: lint format test build run

# Commands to check the API works as expected when running locally
health-check-local:
	curl -X GET "http://localhost:$(PORT)/health"

sample-request-local:
	curl -X GET "http://localhost:$(PORT)/trips?from_ms=1674561748000&n_results=100"

sample-request-no-results-local:
	curl -X GET "http://localhost:$(PORT)/trips?from_ms=1727430298000&n_results=100"

many-requests-local:
	@N=$${N:-10}; \
	for i in $$(seq 1 $$N); do \
		echo "Request $$i:"; \
		$(MAKE) sample-request-local; \
		echo; \
	done

# Commands to check the API from the production environment works as expected
health-check-production:
	curl -X GET "https://paulescu-taxi-data-api-python-ayolbhnl.gimlet.app/health"

sample-request-production:
	curl -X GET "https://paulescu-taxi-data-api-python-ayolbhnl.gimlet.app/trips?from_ms=1674561748000&n_results=100"

sample-request-no-results-production:
	curl -X GET "https://paulescu-taxi-data-api-python-ayolbhnl.gimlet.app/trips?from_ms=1727430298000&n_results=100"

# Command to check the size of the local Docker images
check-image-sizes: build-naive build-single-stage build-multi-stage
	@echo "Naive image size"
	@docker images --format "{{.Size}}" taxi-data-api-python:naive-build

	@echo "Single-stage image size"
	@docker images --format "{{.Size}}" taxi-data-api-python:single-stage-build

	@echo "Multi-stage image size"
	@docker images --format "{{.Size}}" taxi-data-api-python:multi-stage-build

# Commands to start and stop the Elasticsearch and Kibana containers
start-infra:
	docker compose up -d

stop-infra:
	docker compose down
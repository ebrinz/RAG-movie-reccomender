# Define variables
DOCKER_COMPOSE = docker-compose
PROJECT_NAME = movie_recco
DOCKER_API_CONTAINER = api
DOCKER_LLM_CONTAINER = llm
DOCKER_NETWORK = my_network
BROWSER_CMD = open
ENV_FILE = .env

.PHONY: all build up data ingest pull logs open down clean desolate

# Default task
all: build up data ingest pull open

# Build Docker Compose stack
build:
	@echo "Building Docker Compose stack..."
	$(DOCKER_COMPOSE) --env-file $(ENV_FILE) build

# Start Docker Compose stack
up:
	@echo "Starting Docker Compose stack..."
	$(DOCKER_COMPOSE) --env-file $(ENV_FILE) up -d

# Ingest data into the database
data:
	@echo "Downloading data and creating embeddings..."
	$(DOCKER_COMPOSE) exec $(DOCKER_API_CONTAINER) python /app/src/api/build.py

# Ingest data into the database
ingest:
	@echo "Ingesting data into the database..."
	$(DOCKER_COMPOSE) exec $(DOCKER_API_CONTAINER) python /app/src/api/ingest.py

# Pull the Llama3 model
pull:
	@echo "Pulling the Llama3 model..."
	@curl -X POST http://localhost:11434/api/pull \
		-H "Content-Type: application/json" \
		-d '{"model": "llama3"}'

# Show logs of all containers
logs:
	@echo "Displaying logs of all containers..."
	$(DOCKER_COMPOSE) logs -f

# open browser to web service
open:
	@echo "Opening browser at http://localhost:3000..."
	$(BROWSER_CMD) http://localhost:3000

# Start Docker Compose stack
down:
	@echo "Exiting Docker Compose stack..."
	$(DOCKER_COMPOSE) down

# Stop and clean up the Docker Compose stack
clean:
	@echo "Stopping and removing Docker Compose stack..."
	@docker-compose down --volumes --remove-orphans || echo "Docker Compose is already stopped."
	@echo "Removing volumes associated with the project '${PROJECT_NAME}'..."
	@docker volume ls --filter "name=${PROJECT_NAME}_" --format "{{.Name}}" | xargs -r docker volume rm || echo "No volumes to remove."
	@echo "Cleaning up unused Docker resources..."

# Blow all docker data out of the water
desolate:
	@echo "Stopping all running containers..."
	@docker stop $(docker ps -aq) || echo "No running containers to stop."
	@echo "Removing all containers..."
	@docker rm $(docker ps -aq) || echo "No containers to remove."
	@echo "Removing all images..."
	@docker rmi $(docker images -q) -f || echo "No images to remove."
	@echo "Removing all volumes..."
	@docker volume rm $(docker volume ls -q) || echo "No volumes to remove."
	@echo "Removing all networks..."
	@docker network rm $(docker network ls -q) || echo "No networks to remove."
	@echo "Pruning all build cache..."
	@docker builder prune -f || echo "No build cache to prune."
	@echo "Pruning system resources..."
	@docker system prune -a -f --volumes || echo "No resources to prune."
	@echo "Checking for dangling Docker processes..."
	@if ps aux | grep '[d]ockerd' >/dev/null; then \
		echo "Warning: Docker daemon is still running processes."; \
		echo "Killing dangling Docker processes..."; \
		pkill -f 'dockerd' || echo "Failed to kill Docker daemon. You may need to stop it manually."; \
	else \
		echo "No dangling Docker processes found."; \
	fi
	@echo "All Docker resources have been blown away. Cleanup complete."

# Offload data
room:
	@echo "Offloading chunk files to make room for another model..."
	@export EMBEDDING_MODEL=$$(grep EMBEDDING_MODEL $(ENV_FILE) | cut -d '=' -f2); \
	if [ -z "$$EMBEDDING_MODEL" ]; then \
		echo "Error: EMBEDDING_MODEL is not set in the .env file."; \
		exit 1; \
	fi; \
	ARTIFACT_DIR=./data/artifacts/$$EMBEDDING_MODEL; \
	mkdir -p $$ARTIFACT_DIR; \
	mv ./data/chunks/* $$ARTIFACT_DIR/ || echo "No files to move.";
	@echo "Offload complete. Files moved to ./data/artifacts/$$EMBEDDING_MODEL."


########## EVALS

# Setup evals environment for model analysis
setup-evals-env:
	cd evals && uv venv && source .venv/bin/activate && \
	uv pip install -r requirements.txt && \
	uv pip install ipykernel jupyter && \
	python -m ipykernel install --user --name=evals-kernel

#
# Download dataset
download-evals-data:
	cd evals && python -m embedding.cli download --config config/embedding_eval.yaml

# Prepare evaluation data
prepare-evals:
	cd evals && python -m embedding.cli prepare --config config/embedding_eval.yaml

# Run evaluation with prepared data
run-evals:
	cd evals && python -m embedding.cli evaluate \
		--config config/embedding_eval.yaml \
		--output results/embedding_benchmarks/results.csv \
		--verbose

# Run complete evaluation pipeline
evals: download-evals-data prepare-evals run-evals

# Watch evaluation tests
test-evals-watch:
	cd evals && pytest-watch embedding/tests/ -- -v --cov=embedding

# Clean up evals environment after use
clean-evals-env:
	rm -rf evals/.venv
	which jupyter > /dev/null && jupyter kernelspec uninstall evals-kernel -y || true
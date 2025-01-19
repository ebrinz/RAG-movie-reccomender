# Define variables
DOCKER_COMPOSE = docker-compose
PROJECT_NAME = movie_recco
DOCKER_API_CONTAINER = api
DOCKER_LLM_CONTAINER = llm
DOCKER_NETWORK = my_network
BROWSER_CMD = open
ENV_FILE = .env

.PHONY: all build up data ingest pull down clean logs

# Default task
all: build up data ingest pull

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

desolate:
	@echo "Pruning all dangling Docker images..."
	@docker image prune -f || echo "No dangling images to remove."
	@echo "Dangling image cleanup complete."
	@echo "Cleaning up unused Docker resources..."
	@docker system prune -f --volumes || echo "No resources to prune."
	@echo "Cleanup complete."

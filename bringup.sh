#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Step 0: Install Python dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Step 1: Run the data generation script
echo "Running data generator script..."
python3 ./data/generator.py

# Step 2: Bring up Docker containers
echo "Starting Docker containers..."
docker-compose up -d

# Step 3: Run the data generator script again
echo "Ingesting JSON into Postgres container..."
python3 ./data/ingest.py

echo "Setup complete!"
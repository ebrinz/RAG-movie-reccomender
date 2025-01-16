# FROM python:3.10-slim

# # Set the working directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the src directory into /app
# COPY src /app/src

# # Set PYTHONPATH to include /app
# ENV PYTHONPATH=/app/src

# # Expose port 5000 for Flask
# EXPOSE 5000

# # Use Gunicorn as the application server
# # CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.flask_app.main:app"]
# CMD ["python", "/app/src/flask_app/main.py"]




# Using ARM architecture for MAC M series
FROM --platform=linux/arm64 python:3.10-slim-buster
# else....
# FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Install system dependencies for Python packages (if necessary)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade transformers
RUN pip install torch --upgrade

# Preload the Hugging Face model during the build process
RUN python -c "from transformers import ModernBertModel, ModernBertConfig, AutoTokenizer; \
config = ModernBertConfig(); \
AutoTokenizer.from_pretrained('answerdotai/ModernBERT-large'); \
ModernBertModel.from_pretrained('answerdotai/ModernBERT-large', trust_remote_code=True)"


# Copy the src directory into /app
COPY src /app/src

# Set PYTHONPATH to include /app
ENV PYTHONPATH=/app/src

# Expose port 5000 for Flask
EXPOSE 5000

# Default command
CMD ["python", "/app/src/flask_app/main.py"]
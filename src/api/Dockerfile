
# Using ARM architecture for MAC M series
# FROM --platform=linux/arm64 python:3.10-slim-buster
# else....
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app
RUN env
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
# RUN python -c "from transformers import ModernBertModel, ModernBertConfig, AutoTokenizer; \
# config = ModernBertConfig(); \
# AutoTokenizer.from_pretrained('answerdotai/ModernBERT-large'); \
# ModernBertModel.from_pretrained('answerdotai/ModernBERT-large', trust_remote_code=True)"

# Copy the src directory into /app
COPY src/ /app/src
RUN mkdir -p /app/data/chunks

# Receive build arguments
ARG EMBEDDING_MODEL
ARG VECTOR_DIM
ARG DATABASE_URL

ENV EMBEDDING_MODEL=${EMBEDDING_MODEL}
ENV VECTOR_DIM=${VECTOR_DIM}
ENV DATABASE_URL=${DATABASE_URL}

RUN echo $EMBEDDING_MODEL

RUN python /app/src/api/build.py

# Set PYTHONPATH to include /app
ENV PYTHONPATH=/app/src

# Expose port 5000 for Flask
EXPOSE 5000

# Default command
CMD ["python", "/app/src/api/main.py"]
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src directory into /app
COPY src /app/src

# Set PYTHONPATH to include /app
ENV PYTHONPATH=/app/src

# Expose port 5000 for Flask
EXPOSE 5000

# Use Gunicorn as the application server
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.flask_app.main:app"]
CMD ["python", "/app/src/flask_app/main.py"]
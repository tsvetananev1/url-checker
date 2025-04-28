# Use a Python base image
FROM python:3.13-slim

# Working directory inside the container
WORKDIR /app

# Copy local files to the container
COPY main.py .
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for Prometheus metrics
EXPOSE 8000

# Launch the application
CMD ["python", "main.py"]

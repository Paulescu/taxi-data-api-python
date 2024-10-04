# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only the pyproject.toml and poetry.lock files to leverage Docker cache
COPY pyproject.toml poetry.lock README.md /app/

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]

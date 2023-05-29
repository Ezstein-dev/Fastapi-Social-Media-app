# syntax = docker/dockerfile:1.2
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env cat /etc/secrets/.env

# Run the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

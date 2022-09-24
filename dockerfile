# Dockerfile, Image, Container
FROM python:3.10-slim

LABEL maintainer "Matteo Mastro Libro, anise_avowed01@icloud.com"

# Set working directory in the container
WORKDIR /usr/src/app

# Copy and install packages
COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# Copy app fold to app folder in container
COPY /app /usr/src/app/

# Changing to non-root user
RUN useradd -m appUser
USER appUser

# Run locally on port 8050
CMD gunicorn --bind 0.0.0.0:8050 app:server

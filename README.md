# mozio_app
# Mozio Service Area API

This project aims to develop an API for managing service areas of transportation providers as Mozio expands internationally. This API allows transportation providers to define and update their service areas easily.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [API Usage](#api-usage)
- [Testing](#testing)
- [License](#license)

## Features

- **CRUD Operations**: Manage providers and service areas.
- **GeoJSON Search**: Find service areas that contain a given latitude and longitude.
- **FastAPI Documentation**: Generated API docs with Swagger and Redoc.
- **Unit Testing**: Includes tests for the API.

## Technologies

- Python
- FastAPI
- PostgreSQL
- Docker
- Docker Compose

## Installation

### Prerequisites

- Docker
- Docker Compose
- Git
- Python 3.9+

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/narminnsn/mozio_app.git
cd mozio_app
```

### 2. Environment Variables
Create a .env file in the root directory with the following content:

- POSTGRES_DB=<db_name>
- POSTGRES_USER=<db_user>
- POSTGRES_PASSWORD=<db_password>

These environment variables are used by Docker Compose to configure the PostgreSQL.


### 3. Starting Docker

Make sure Docker is running on your machine. To start the application along with PostgreSQL and Redis using Docker Compose, run:

```bash
docker-compose up
```
This command will start the PostgreSQL and Redis services. Ensure that the services are running properly, and you should see logs indicating that the database is ready to accept connections.

### 4. Virtual Environment

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```



### 5. Running Migrations

After the services are up, run the database migrations:

```bash
alembic revision --autogenerate -m "your migration message"
alembic upgrade head
```

This will create the database tables for you.

### 6. Running Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

# Usage

You can test the API using the following endpoints:

- **List Providers**: `GET /providers`
- **Create New Provider**: `POST /providers`
- **Get Provider by ID**: `GET /providers/{id}`
- **Update Provider by ID**: `PUT /providers/{id}`
- **Delete Provider by ID**: `DELETE /providers/{id}`
- **List Service Areas**: `GET /service-areas`
- **Create New Service Area**: `POST /service-areas`
- **Get Service Areas by ID**: `GET /service-areas/{id}`
- **Update Service Areas by ID**: `PUT /service-areas/{id}`
- **Delete Service Areas by ID**: `DELETE /service-areas/{id}`
- **Search Service Areas by Lat/Lng**: `GET /service-areas/locations?lat={lat}&lng={lng}`


# API Documentation

For detailed API documentation, visit:

- Swagger: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

# Testing

You can use a testing framework like `pytest` or `unittest` to test your code. To run the tests, use:

```bash
pytest
```
or

```bash
python -m unittest discover

```


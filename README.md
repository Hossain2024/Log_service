# Log Processing Service

A FastAPI REST API for ingesting and retrieving application logs.

## Features

- Create log records.
- Retrieve a log by its ID.
- List logs with optional service and severity filters.
- Store data in SQLite by default or PostgreSQL through `DATABASE_URL`.
- Interactive API documentation through Swagger UI.

## Requirements

- Python 3.9 or later
- `pip`

## Installation

Clone the repository, create a virtual environment, and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Locally

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

Interactive documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Configuration

Without configuration, the application uses a SQLite database at `./logs.db`.

To use PostgreSQL, set the `DATABASE_URL` environment variable before starting the application:

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/logs"
uvicorn app.main:app --reload
```

The application automatically uses the Psycopg 3 driver for PostgreSQL URLs.

## API Endpoints

### Health Check

```http
GET /health
```

Example response:

```json
{
	"status": "healthy"
}
```

### Database Information

```http
GET /database-info
```

Example response:

```json
{
	"database": "sqlite",
	"driver": "pysqlite"
}
```

### Create a Log

```http
POST /logs
Content-Type: application/json
```

Request body:

```json
{
	"log_id": "test-002",
	"service_name": "payment-service",
	"level": "ERROR",
	"message": "Payment failed",
	"timestamp": "2026-09-21T12:00:00Z"
}
```

Using curl:

```bash
curl -X POST http://127.0.0.1:8000/logs \
	-H "Content-Type: application/json" \
	-d '{
		"log_id": "test-002",
		"service_name": "payment-service",
		"level": "ERROR",
		"message": "Payment failed",
		"timestamp": "2026-09-21T12:00:00Z"
	}'
```

Successful response: `201 Created`

```json
{
	"log_id": "test-002",
	"service_name": "payment-service",
	"level": "ERROR",
	"message": "Payment failed",
	"timestamp": "2026-09-21T12:00:00"
}
```

### Get All Logs

```http
GET /logs
```

Logs are returned in descending timestamp order. Optional filters:

```http
GET /logs?service_name=payment-service&level=ERROR
```

Valid values for `level` are:

- `DEBUG`
- `INFO`
- `WARNING`
- `ERROR`

Using curl:

```bash
curl "http://127.0.0.1:8000/logs?service_name=payment-service&level=ERROR"
```

Successful response: `200 OK`

```json
[
	{
		"log_id": "test-002",
		"service_name": "payment-service",
		"level": "ERROR",
		"message": "Payment failed",
		"timestamp": "2026-09-21T12:00:00"
	}
]
```

### Get a Log by ID

```http
GET /logs/{log_id}
```

Example:

```bash
curl http://127.0.0.1:8000/logs/test-002
```

Successful response: `200 OK`.

## Validation and Errors

- `201 Created`: log was saved successfully.
- `200 OK`: request completed successfully.
- `404 Not Found`: the requested log ID does not exist.
- `409 Conflict`: a log with the same `log_id` already exists.
- `422 Unprocessable Entity`: request data failed validation.

Validation rules:

- `log_id`: 1 to 100 characters.
- `service_name`: 1 to 100 characters.
- `message`: 1 to 1000 characters.
- `level`: `DEBUG`, `INFO`, `WARNING`, or `ERROR`.
- `timestamp`: a valid date-time value.

## Project Structure

```text
app/
├── main.py                  # Creates the FastAPI app and registers routes
├── database.py              # Database engine, sessions, and shared SQLAlchemy Base
├── models/                  # SQLAlchemy database models
│   └── log.py               # Definition of the logs table
├── schemas/                 # Pydantic request and response models
│   └── log.py               # Log validation and API serialization
├── routers/                 # HTTP endpoint definitions
│   └── logs.py              # /logs routes
├── services/                # Application/business logic
│   └── log_service.py       # Duplicate checks and service operations
└── repositories/            # Database access logic
		└── log_repository.py    # Queries, inserts, and filtering
```

The request flow is:

```text
HTTP request
		-> router
		-> service
		-> repository
		-> database
```

## Deployment

The included `Procfile` starts the application on the port supplied by the hosting platform:

```text
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

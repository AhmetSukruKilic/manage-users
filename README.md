# User Management API

A REST API for managing users with CRUD operations, built with FastAPI and PostgreSQL.

## Features

- ✅ Add new users with hashed passwords
- ✅ Edit user attributes (name, email, password)
- ✅ Delete users
- ✅ Get user by ID
- ✅ Get all users
- ✅ Password hashing with bcrypt
- ✅ PostgreSQL database
- ✅ Docker containerization

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Password Hashing**: bcrypt (via passlib)
- **Containerization**: Docker & Docker Compose

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. The `.env` file is already configured with default settings. You can modify it if needed.

2. Start the services:
```bash
docker-compose up --build
```

2. The API will be available at `http://localhost:8080`

3. Access the database admin panel (Adminer) at `http://localhost:8081`
   - System: PostgreSQL
   - Server: db
   - Username: userapi
   - Password: userapi
   - Database: userapi

## API Endpoints

### Health Check

```bash
curl http://localhost:8080/health
```

### Login (POST /auth/login)

Login with email and password:

```bash
curl -X POST \
-d '{"email": "test@example.com", "password": "securepasswd"}' \
-H 'Content-Type: application/json' \
http://localhost:8080/auth/login
```

**Response (200)**:
```json
{"id": 1, "name": "Test", "email": "test@example.com"}
```

**Errors**:
- `400`: Bad request
- `401`: Invalid email or password
- `500`: Server error

### Add a User (PUT /users)

```bash
curl -X PUT \
-d '{"name": "Test", "email": "test@example.com", "password": "securepasswd"}' \
-H 'Content-Type: application/json' \
http://localhost:8080/users
```

**Response (200)**:
```json
{"id": 1, "name": "Test", "email": "test@example.com"}
```

**Errors**:
- `400`: Bad request
- `403`: User with that email already exists
- `500`: Server error

### Edit a User

```bash
curl -X PATCH \
-d '{"name": "No name", "password": "strongpasswd"}' \
-H 'Content-Type: application/json' \
http://localhost:8080/users/1
```

**Response (200)**:
```json
{"id": 1, "name": "No name", "email": "test@example.com"}
```

**Errors**:
- `400`: Bad request
- `404`: User with that id does not exist
- `500`: Server error

### Delete a User

```bash
curl -X DELETE \
http://localhost:8080/users/1
```

**Response (200)**: Empty response `{}`

**Errors**:
- `400`: Bad request
- `404`: User with that id does not exist
- `500`: Server error

### Get User by ID

```bash
curl -X GET \
http://localhost:8080/users/1
```

**Response (200)**:
```json
{"id": 1, "name": "No name", "email": "test@example.com"}
```

**Errors**:
- `400`: Bad request
- `404`: User with that id does not exist
- `500`: Server error

### Get All Users

```bash
curl -X GET \
http://localhost:8080/users
```

**Response (200)**:
```json
[
  {"id": 1, "name": "No name", "email": "test@example.com"},
  {"id": 2, "name": "Test2", "email": "test2@example.com"}
]
```

**Errors**:
- `400`: Bad request
- `500`: Server error

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- Swagger UI: http://localhost:8080/docs

## Project Structure

```
user-management-api/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app initialization
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # Database connection
│   ├── auth.py           # Password hashing utilities
│   └── routers/
│       ├── __init__.py
│       └── users.py      # User CRUD endpoints
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Environment Variables

The application uses a `.env` file for configuration:

```env
# Database Configuration
DATABASE_URL=postgresql://userapi:userapi@db:5432/userapi
POSTGRES_USER=userapi
POSTGRES_PASSWORD=userapi
POSTGRES_DB=userapi

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8080
```

## Security

- Passwords are hashed using bcrypt before storing in the database
- Password hashes are never returned in API responses
- Database credentials should be changed in production
- The `.env` file is in `.gitignore` to prevent committing sensitive data

## Development

To run without Docker:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL and configure DATABASE_URL environment variable:
```bash
export DATABASE_URL="postgresql://userapi:userapi@localhost:5432/userapi"
```

3. Run the application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## Stopping the Application

```bash
docker-compose down
```

To remove volumes as well:
```bash
docker-compose down -v
```


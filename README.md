### Synergy Test Task (FastAPI + React + Docker)

This repository contains a backend (FastAPI, PostgreSQL) and a frontend (React + TypeScript) that demonstrate:
- Random user data retrieval from `randomuser.me` ([docs](https://randomuser.me/))
- Editing and persisting data in PostgreSQL
- Managing, sorting, editing, and deleting saved data

### Project Structure
```
backend/   # FastAPI app, SQLAlchemy models, tests, Dockerfile
frontend/  # React Vite TS app, Dockerfile
docker-compose.yml
```

### Backend
- Endpoints:
  - `GET /external/random-user` — fetch a random user and map to our schema
  - `POST /users` — create user
  - `GET /users?sort=first_name|last_name|email` — list with sorting
  - `GET /users/{id}` — retrieve
  - `PUT /users/{id}` — update
  - `DELETE /users/{id}` — delete
- DB tables are created on startup.
- Tests: `pytest`, sample API tests in `backend/tests`.

### Frontend
  - `/` — CRUD operations for users

### Prerequisites
- Docker and Docker Compose installed locally

### Environment Variables
- Create a `.env` file in the root directory with the following variables:
```
# backend
# backend
ENVIRONMENT="development"
DEBUG="false"
IS_DOCKER="false"

DATABASE_URL="postgresql://<user>:<password>@localhost:5432/<name>"
CORS_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173"]

# frontend
VITE_API_URL="http://localhost:8000"
```

### Run (Docker Compose)
```bash
docker compose build
docker compose up
```
- Backend: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`

### Tests
```bash
cd backend
pytest
```

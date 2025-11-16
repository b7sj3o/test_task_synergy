### Synergy Test Task (FastAPI + React + Docker)

This repository contains a backend (FastAPI, PostgreSQL) and a frontend (React + TypeScript) that demonstrate:
- Random user data retrieval from `randomuser.me` ([docs](https://randomuser.me/))
- Editing and persisting data in PostgreSQL
- Managing, sorting, editing, and deleting saved data

### Project Structure
```
backend/   # FastAPI app, SQLAlchemy models, tests, Dockerfile
frontend/  # React + TS app with two pages, Dockerfile
docker-compose.yml
```

### Backend
- Entities: `User` (1) — `Address` (many), `User` (1) — `Bank` (1), `Bank` (1) — `Address` (1)
- Endpoints:
  - `GET /external/random-user` — fetch a random user and map to our schema
  - `POST /users` — create user (+ nested address/bank)
  - `GET /users?sort=first_name|last_name|email` — list with sorting
  - `GET /users/{id}` — retrieve
  - `PUT /users/{id}` — update (naive replace strategy for addresses/bank)
  - `DELETE /users/{id}` — delete
- DB tables are created on startup. Formatting via Black.
- Tests: `pytest`, sample API tests in `backend/tests`.

### Frontend
- Two pages:
  - `/random` — fetch random user, edit locally, save to DB
  - `/manage` — list with sorting, edit inline, delete
- API client in `frontend/src/lib/api.ts`.

### Prerequisites
- Docker and Docker Compose

### Run (Docker Compose)
```bash
docker compose build
docker compose up
```
- Backend: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`

### Local Development (optional)
Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/synergy"
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```
Set `VITE_API_URL` env (or update in `src/lib/api.ts`) to point to your backend.

### Tests
```bash
cd backend
pytest
```

### Formatting
```bash
cd backend
black app tests
```

### Notes
- This code aims to be clean and easily extensible with a simple service layer and typed schemas.
- For brevity of the test task, migrations are not included; tables are created automatically on startup.



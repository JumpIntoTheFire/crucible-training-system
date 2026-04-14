# The Crucible Training System

A full-stack fitness coaching platform built as a CV portfolio project. Demonstrates real engineering decisions across the entire stack — custom workout builder, JWT auth, REST API, and a Dockerised multi-service architecture.

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, React Router DOM 7, Vite 7 |
| Backend | FastAPI (Python 3.11), Uvicorn |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Infra | Docker Compose |

## Features

- **Exercise library** — 873 exercises with images, searchable and filterable by name, muscle group, and training category
- **Workout builder** — add exercises, configure sets/reps/rest, reorder and save named workout plans
- **Auth** — register/login with JWT; workouts persist to the database per user, with localStorage fallback when logged out
- **Contact form** — server-side validation, stored in PostgreSQL
- **Package pages** — four subscription tiers with CTAs

## Quick Start (Docker)

**Prerequisites:** Docker and Docker Compose installed.

```bash
git clone https://github.com/JumpIntoTheFire/crucible-training-system.git
cd crucible-training-system

# Copy and configure environment files
cp frontend/.env.example frontend/.env
cp .env.example .env          # backend secrets

# Start all services
docker compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5174 |
| Backend API | http://localhost:8001 |
| API Docs | http://localhost:8001/docs |

### Load the Exercise Library

After the containers are up, run the ingest script once to populate the database.
Provide the path to your exercise data directory (JSON + images):

```bash
EXERCISE_DATA_PATH=/path/to/exercise/data docker compose up --build
docker compose exec backend python -m backend.scripts.ingest_exercises
```

## Local Development (without Docker)

```bash
# Backend
cd CTS_Full_Stack
python -m venv backend/.venv
backend/.venv/Scripts/activate        # Windows
# source backend/.venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
uvicorn backend.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

## Environment Variables

### Backend (`.env`)
| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `SECRET_KEY` | Yes (prod) | JWT signing key — minimum 32 random bytes |
| `CORS_ORIGINS` | No | Comma-separated allowed origins (default: localhost) |

### Frontend (`frontend/.env`)
| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://localhost:8001` | Backend API base URL |

## API

Full interactive docs available at `/docs` (Swagger UI) when the backend is running.

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| GET | `/` | — | Health check |
| GET | `/exercises` | — | List exercises (search, filter, paginate) |
| POST | `/contact` | — | Submit contact form |
| POST | `/auth/register` | — | Create account |
| POST | `/auth/login` | — | Login, returns JWT |
| GET | `/workouts` | JWT | List user's saved workout plans |
| POST | `/workouts` | JWT | Save a new workout plan |
| DELETE | `/workouts/{id}` | JWT | Delete a workout plan |

## Running Tests

```bash
pip install pytest httpx
pytest backend/tests/ -v
```

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI app, CORS, route mounting
│   ├── models.py            # SQLAlchemy ORM models
│   ├── auth.py              # JWT utilities, password hashing
│   ├── routes/
│   │   ├── exercises.py     # GET /exercises with filtering + pagination
│   │   ├── auth.py          # POST /auth/register, /auth/login
│   │   └── workouts.py      # GET/POST/DELETE /workouts (JWT protected)
│   ├── schemas/
│   │   └── exercises.py     # Pydantic response schemas
│   ├── scripts/
│   │   └── ingest_exercises.py  # Bulk-load exercises from JSON + images
│   └── tests/
│       ├── test_auth.py
│       ├── test_exercises.py
│       └── test_workouts.py
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── contexts/AuthContext.jsx
│       └── components/
│           ├── Layout.jsx
│           ├── ExerciseBuilder.jsx
│           ├── ExerciseCard.jsx
│           ├── WorkoutPanel.jsx
│           ├── AuthPage.jsx
│           └── ...
│
├── docker-compose.yml
└── requirements.txt
```

## Security Notes

- Passwords hashed with bcrypt (passlib)
- JWTs signed with HS256; `SECRET_KEY` must be set via environment — the app refuses to start in production without it
- CORS origins configurable via `CORS_ORIGINS` environment variable
- SQL injection protected by SQLAlchemy ORM parameterised queries
- Input validation on all endpoints via Pydantic

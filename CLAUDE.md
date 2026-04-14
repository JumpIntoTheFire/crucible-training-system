# CLAUDE.md — The Crucible Training System (CTS)

## Project Purpose
A full-stack fitness coaching platform built as a CV portfolio project. The goal is to demonstrate technical depth through a fully custom workout builder, subscription tiers, and supporting features. It must be production-quality and showcase real engineering decisions.

## Stack

| Layer     | Technology                                      |
|-----------|-------------------------------------------------|
| Frontend  | React 19, React Router DOM 7, Vite 7            |
| Backend   | FastAPI (Python), Uvicorn                       |
| Database  | PostgreSQL (`cts_db` on localhost:5432)         |
| ORM       | SQLAlchemy 2.0                                  |
| Schemas   | Pydantic (via FastAPI)                          |
| Images    | Static files served by FastAPI `/images` route  |

## Project Structure

```
Full stack/
├── backend/
│   ├── main.py                  # FastAPI app, CORS, route mounting
│   ├── models.py                # SQLAlchemy ORM models (Contact, Exercise)
│   ├── init_db.py               # DB session / get_db() dependency
│   ├── routes/
│   │   └── exercises.py         # GET /exercises with filtering
│   ├── schemas/
│   │   └── exercises.py         # Pydantic response schemas
│   ├── scripts/
│   │   ├── ingest_exercises.py  # Bulk-load exercises from JSON + images
│   │   └── validate_images.py   # Image presence checker
│   └── static/images/           # 873 exercise image folders (served via /images)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Root router
│   │   ├── main.jsx             # React entry point
│   │   ├── index.css            # Global styles
│   │   └── components/
│   │       ├── Layout.jsx       # Nav + dropdown
│   │       ├── HomePage.jsx     # Landing page (3 brand pillars)
│   │       ├── Packages.jsx     # Package routing wrapper
│   │       ├── BasicPage.jsx    # £60/month tier
│   │       ├── PremiumPage.jsx  # £90/month tier
│   │       ├── UltraPage.jsx    # Upper tier
│   │       ├── ElitePage.jsx    # Top tier
│   │       ├── ContactPage.jsx  # Contact form → POST /contact
│   │       ├── ExerciseBuilder.jsx # Exercise library viewer
│   │       └── NotFound.jsx
│   └── public/                  # Static assets (images, etc.)
│
├── CLAUDE.md                    # This file
├── CHANGELOG.txt                # Chronological dev log (oldest top, newest bottom)
└── commands.txt                 # Dev command reference
```

## Dev Commands

```bash
# Docker (preferred — runs everything)
docker compose up --build         # first run
docker compose up                 # subsequent runs
docker compose down               # stop
docker compose down -v            # stop + delete DB volume

# Ingest exercises into Docker DB (after containers are up)
# Exercise source is mounted at /exercise_data via docker-compose volume
docker compose exec backend python -m backend.scripts.ingest_exercises

# Local (non-Docker)
backend\.venv\Scripts\activate
uvicorn backend.main:app --reload   # from project root

cd frontend && npm run dev

set PYTHONPATH=. && python backend/scripts/ingest_exercises.py
```

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- DB: `postgresql://postgres:postgres@localhost:5432/cts_db` (local) / `@db:5432` (Docker)

## Docker Architecture

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Orchestrates db, backend, frontend services |
| `backend/Dockerfile` | Python 3.11-slim, installs deps, runs init_db + uvicorn |
| `frontend/Dockerfile` | Node 20-alpine, installs deps, runs Vite dev server |
| `requirements.txt` | Pinned Python dependencies |
| `.dockerignore` | Excludes .venv, __pycache__, node_modules from build context |
| `frontend/.env` | `VITE_API_URL=http://localhost:8000` (used by both local and Docker) |

**Key decisions:**
- `DATABASE_URL` is read from environment in `models.py` — Docker sets it to `@db:5432`, local fallback uses `@localhost:5432`
- All `localhost:8000` references in frontend use `import.meta.env.VITE_API_URL`
- Backend volume-mounts `./backend:/app/backend` for hot reload without rebuild
- Frontend volume-mounts `src/` and `public/` only — `node_modules` stays in the container
- DB waits for healthcheck before backend starts (`pg_isready`); backend has `restart: on-failure`

## Database Models

### Contact
| Column  | Type    |
|---------|---------|
| id      | Integer PK |
| name    | String  |
| email   | String  |
| message | Text    |

### Exercise
| Column           | Type          |
|------------------|---------------|
| id               | Integer PK    |
| name             | String        |
| force            | String        |
| level            | String        |
| mechanic         | String        |
| equipment        | String        |
| primaryMuscles   | ARRAY(Text)   |
| secondaryMuscles | ARRAY(Text)   |
| instructions     | ARRAY(Text)   |
| category         | String        |
| startImage       | String (path) |
| endImage         | String (path) |

## API Endpoints

| Method | Route      | Description                              |
|--------|------------|------------------------------------------|
| GET    | /          | Health check                             |
| POST   | /contact   | Save contact form submission to DB       |
| GET    | /exercises | List exercises, filter by tag/muscle     |
| GET    | /images/.. | Serve static exercise images             |

## Key Decisions & Constraints
- Run uvicorn from project root (`Full stack/`), not from `backend/` — imports rely on `backend.` package prefix
- Python virtual environment is at `backend/.venv` (use this one, not the root `.venv`)
- CORS is explicitly allowed for `http://localhost:5173`
- Exercise images are stored in `backend/static/images/{exercise-name}/` with `0.jpg` (start) and `1.jpg` (end)

## Goals (CV Portfolio)
- **Primary**: Fully custom workout builder — user selects exercises, sets, reps, and saves/exports a plan
- **Secondary**: Show technical breadth — auth, database design, REST API, React state management, responsive UI
- **Quality bar**: Production-quality code, no half-finished features, clean architecture
- **Changelog**: Every change logged to `CHANGELOG.txt` with date and time, oldest at top, newest at bottom

---

## Roadmap

### Current State (as of 2026-04-09)
- Backend API functional: `/exercises` (873 exercises with images), `/contact`, static image serving
- Frontend routes wired: Home, Packages (4 tiers), Contact, `/builder`
- `ExerciseBuilder.jsx` is a raw list dump — no search, no builder, no workout logic
- `App.jsx` contains ~200 lines of commented-out debug iterations (needs cleaning)
- `main.py` and `schemas/exercises.py` also contain dead commented code
- No auth, no user accounts, no saved workouts

---

### Phase 1 — Codebase Cleanup & Stable Foundation
**Goal:** Every file is clean, routing works end-to-end, and the app renders correctly in the browser.

| # | Task | Testable Milestone |
|---|------|--------------------|
| 1.1 | Delete all commented-out code in `App.jsx`, `main.py`, `schemas/exercises.py` | Files contain only live code |
| 1.2 | Add pagination to `GET /exercises` (`?skip=0&limit=20`) | curl returns first 20, second page returns next 20 |
| 1.3 | Add search param to `GET /exercises` (`?search=bench`) | curl with search filters by exercise name |
| 1.4 | Apply a consistent design system (CSS variables: colours, fonts, spacing) to `index.css` | All pages use the same palette/fonts |
| 1.5 | Verify all routes render without errors in browser | Navigate to /, /packages/basic, /contact, /builder — no blank screens |

---

### Phase 2 — Core Workout Builder
**Goal:** A user can search exercises, add them to a workout plan with sets/reps/rest, and see their plan live.

| # | Task | Testable Milestone |
|---|------|--------------------|
| 2.1 | Rebuild `ExerciseBuilder.jsx` with search bar + muscle-group filter | Typing "bench" shows only bench exercises |
| 2.2 | Exercise cards show name, category, primary muscles, start image | Card renders correctly for each exercise |
| 2.3 | "Add to Workout" button appends exercise to a workout state (right-side panel) | Click add → exercise appears in workout list |
| 2.4 | Each workout entry has editable sets, reps, rest fields | User can type "4 sets, 8 reps, 90s rest" per exercise |
| 2.5 | Workout panel has remove, reorder (up/down), and clear all controls | Remove/reorder works without page refresh |
| 2.6 | "Save Workout" stores plan to localStorage with a name | Refresh page → named workout still appears |
| 2.7 | Saved workouts list lets user load/delete previous plans | Load plan → workout panel repopulates correctly |

---

### Phase 3 — User Auth & Backend Persistence
**Goal:** Users can register, log in, and have their workouts saved to the database under their account.

| # | Task | Testable Milestone |
|---|------|--------------------|
| 3.1 | Add `User` model: id, username, email, hashed_password | `users` table created in cts_db |
| 3.2 | Add `WorkoutPlan` model: id, user_id, name, created_at, exercises (JSONB) | `workout_plans` table created |
| 3.3 | `POST /auth/register` + `POST /auth/login` endpoints with JWT | curl login returns a JWT token |
| 3.4 | Password hashing with bcrypt | Plain-text passwords never stored |
| 3.5 | JWT middleware protects workout routes | Request without token returns 401 |
| 3.6 | `POST /workouts` saves plan to DB under logged-in user | Plan persists after localStorage cleared |
| 3.7 | `GET /workouts` returns user's plans | Only the logged-in user's plans returned |
| 3.8 | `DELETE /workouts/{id}` removes a plan | Deleted plan no longer appears in list |
| 3.9 | Frontend login/register forms + auth context (JWT stored in memory/httpOnly) | Login → builder shows saved workouts |

---

### Phase 4 — Polish & Portfolio Features
**Goal:** The app looks and feels production-quality and demonstrates additional technical depth.

| # | Task | Testable Milestone |
|---|------|--------------------|
| 4.1 | Workout export to PDF or printable view | Click export → browser print dialog with formatted plan |
| 4.2 | Exercise detail modal (full instructions, both images, all metadata) | Click exercise → modal opens with full info |
| 4.3 | Workout history page — list all past plans with date | `/history` shows plans sorted by date |
| 4.4 | Responsive layout — works on mobile and tablet | Resize to 375px — no horizontal scroll, usable UI |
| 4.5 | Package pages — real content with CTA buttons linking to contact | Each tier page has real copy and a working CTA |
| 4.6 | Loading skeletons / error states throughout | No raw "Loading..." or blank screens anywhere |
| 4.7 | Environment config — move hardcoded localhost URLs to `.env` | `VITE_API_URL` used everywhere in frontend |

---

### Phase Order Rationale
Phases must be completed in order — each phase's output is the foundation of the next.
Do not start Phase 3 until the workout builder (Phase 2) is fully functional end-to-end.
Do not start Phase 4 polish until auth and persistence (Phase 3) are working.

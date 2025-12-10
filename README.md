# Air Quality Monitoring System (Backend + Frontend)

A full-stack air quality monitoring system built with a Flask backend, a Vue 3 (Vite) frontend, and PostgreSQL for data storage. It supports user authentication, city catalog management, historical AQI queries, latest readings, monthly statistics, health advice, and scheduled data synchronization from AQICN.

## Overview

- Backend: Flask 3.x REST API with token-based auth, APScheduler for background jobs, psycopg2 for PostgreSQL.
- Frontend: Vue 3 + Pinia + Vue Router, Vite dev server with proxy to the backend.
- Database: PostgreSQL with tables for users, cities, air quality data, health advice, sync logs, and analytics.
- Sync: Hourly job to fetch air quality data from AQICN and persist to the database.

## Repository Structure

```
.
├─ backend/
│  ├─ app/
│  │  ├─ api/                 # Flask blueprints (auth, users, data, admin)
│  │  │  ├─ auth/             # Auth endpoints
│  │  │  ├─ users/            # User profile endpoints
│  │  │  ├─ data/             # Cities, AQI query & stats
│  │  │  ├─ admin/            # Admin (placeholder)
│  │  ├─ extensions/          # App extensions (db pool)
│  │  ├─ repositories/        # DB access layer (cities, users, AQI, analytics, sync logs)
│  │  ├─ services/            # External integrations and business services (auth, AQICN)
│  │  ├─ tasks/               # APScheduler jobs
│  │  ├─ utils/               # Response helpers
│  │  └─ __init__.py          # Flask app factory
│  ├─ db/sql/                 # PostgreSQL schema (DDL)
│  └─ tests/                  # Test scaffold
├─ frontend/
│  └─ vue-project/            # Vue 3 + Vite app
│     ├─ src/components       # UI components
│     ├─ src/views            # Route views (Dashboard, Profile, Admin)
│     ├─ src/stores           # Pinia stores (user, dashboard)
│     ├─ src/router           # Vue Router setup
│     ├─ vite.config.ts       # Dev server proxy to backend
│     └─ package.json         # Dev scripts
├─ scripts/                   # Helper scripts
│  └─ start.ps1               # Windows startup helper (env + DB check + run)
├─ run.py                     # Unified dev/prod runner (Flask/Gunicorn)
├─ requirements.txt           # Python dependencies
├─ .env                       # Project environment variables (development)
├─ quickstart.bat / .sh       # Quickstart scripts
├─ api_import_example.py      # API usage demo client
├─ import_data.py             # Data import orchestration script
└─ test_api.py                # API smoke test script
```

## Prerequisites

- Python 3.10+
- Node.js 20+ (or 22+)
- PostgreSQL 13+ (local or remote)

## Environment Configuration

Create `.env` in the project root (already present in this repository). Key variables:

- `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql://user:pass@localhost:5432/air_quality_db`)
- `SECRET_KEY`: Flask secret used for token signing
- `CORS_ORIGINS`: Allowed origins for CORS (e.g., `*` during development)
- `AQICN_API_TOKEN`: Token for AQICN API access
- `PORT` / `HOST`: Default Flask dev server host/port

Note: Do not commit real tokens or secrets. For development, prefer local `.env`.

## Database Setup

Use the SQL files under `backend/db/sql` to initialize the PostgreSQL schema:

```
psql -U postgres -c "CREATE DATABASE air_quality_db;"
psql -U postgres -d air_quality_db -f backend/db/sql/001_create_users.sql
psql -U postgres -d air_quality_db -f backend/db/sql/002_create_cities.sql
psql -U postgres -d air_quality_db -f backend/db/sql/003_create_air_quality_data.sql
psql -U postgres -d air_quality_db -f backend/db/sql/004_create_health_advice.sql
psql -U postgres -d air_quality_db -f backend/db/sql/005_create_sync_logs.sql
psql -U postgres -d air_quality_db -f backend/db/sql/006_create_user_analytics.sql
```

Tables and purpose:

- `users`: accounts with `phone`, hashed passwords, `role`, `tag`, `default_city_id`
- `cities`: catalog of cities with `name`, `province`, coordinates
- `air_quality_data`: historical AQI and pollutant metrics per city and timestamp
- `health_advice`: rules mapped by pollutant, AQI level, and target group
- `sync_logs`: records of data sync runs (counts, status, duration)
- `user_analytics`: daily feature usage and city engagement metrics

## Backend: Run (Development)

Option A — Python runner:

```
python run.py --host 0.0.0.0 --port 5000
```

Option B — Windows helper (validates DB then runs):

```
# PowerShell
./scripts/start.ps1 -DatabaseUrl "postgresql://user:pass@localhost:5432/air_quality_db" -SecretKey "dev-secret" -Port 5000
```

The app factory loads environment via `python-dotenv`, initializes the DB pool, optionally enables CORS, registers blueprints, and starts the APScheduler job.

## Backend: Run (Production)

Use Gunicorn via `run.py`:

```
python run.py --production --host 0.0.0.0 --port 8000 --workers 4
```

Behind a reverse proxy (NGINX/IIS), configure TLS, request limits, and CORS. Ensure environment variables are set for the process.

## Frontend: Development

```
cd frontend/vue-project
npm install
npm run dev
```

The dev server proxies `/api/*` to the backend. Update proxy target in `vite.config.ts` to match your backend:

```ts
server: {
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:5000', // your Flask server
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```

## Key Backend Modules

- Auth tokens: time-limited tokens with `itsdangerous`; issue and verify in `backend/app/services/auth.py`
- DB pool: `psycopg2.pool.ThreadedConnectionPool` initialized in `backend/app/extensions/db.py`
- AQICN sync: hourly APScheduler job calling `backend/app/services/aqicn.py` to fetch and persist AQI
- Repositories: encapsulate SQL access for users, cities, air quality, analytics, and sync logs
- API responses: normalized helpers in `backend/app/utils/response.py`

## API Reference (Brief)

Authentication

- `POST /auth/register` — Register a user; returns `user` and `token`
- `POST /auth/login` — Login; returns `user` and `token`
- `GET /auth/me` — Get current user info (Bearer token required)

User Profile

- `GET /users/me` — Current user profile
- `PUT /users/me` — Update profile (`nickname`, `phone`, `default_city_id`)
- `PUT /users/me/tags` — Update `tag` (`normal`, `elderly`, `children`, `asthma`, `pregnant`)

Data

- `GET /data/cities` — List cities with optional `q`, `province`, pagination
- `GET /data/cities/{id}` — Get city details
- `GET /data/query` — Historical AQI by `city_id`, optional `start_time`, `end_time`, pagination
- `GET /data/detail` — Latest AQI for a city, also logs a user analytics event
- `GET /data/monthly-stats` — Monthly good-day ratio and PM2.5 average for a city

Request headers: `Authorization: Bearer <token>` required for `/data/*` and `/users/*`.

## Scheduled Jobs

APScheduler starts at app boot and runs an hourly job `sync_air_quality` that:

- Lists known cities
- Queries AQICN for each city
- Saves results to `air_quality_data`
- Updates a record in `sync_logs` with success/failure and counts

Configure `AQICN_API_TOKEN` in `.env` to enable successful requests.

## Data Import and Testing

- `import_data.py` — Adds baseline city records, triggers an AQICN sync, verifies data presence
- `api_import_example.py` — Demonstrates registration, login, cities query, latest AQI, history, and monthly stats via HTTP calls
- `test_api.py` — Smoke tests for core endpoints; run with the backend active

```
python import_data.py
python api_import_example.py
python test_api.py
```

## Security and CORS

- Tokens are signed with `SECRET_KEY` and time-limited by default to 7 days
- Do not expose real tokens in source; use environment variables
- Enable CORS carefully; default development wildcard `*` should be restricted in production

## Troubleshooting

- Database connection fails: verify `DATABASE_URL`; use `scripts/start.ps1` to validate connectivity
- Frontend requests failing: align Vite proxy target with backend host/port
- Empty data responses: ensure cities exist and `AQICN_API_TOKEN` is valid; run `import_data.py`
- 401 Unauthorized: confirm `Authorization: Bearer <token>` header is set

## License

Internal project documentation. Adjust licensing as appropriate for deployment.


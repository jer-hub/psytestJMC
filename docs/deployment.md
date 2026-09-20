# Deployment

## Docker (recommended for local / container hosts)

```bash
# Development (runserver + live mount)
docker compose up --build -d

# Production-style (gunicorn)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

On start, the entrypoint waits for Postgres, runs migrations, ensures the Django Site row, optionally seeds `data/fixtures/`, and creates a superuser when env vars are set.

Copy `.env.example` to `.env` and adjust secrets. Docker Compose also reads the same variables for DB credentials.

Useful commands:

```bash
docker compose logs -f web
docker compose exec web python manage.py check
./scripts/seed_data.sh   # inside the web container if re-seeding
```

## Vercel

Configured for Django 4.2 with `psytests.settings.vercel` when `VERCEL` is set (`psytests/wsgi.py`).

### Prerequisites

- Vercel CLI (`npm i -g vercel`)
- PostgreSQL (Vercel Postgres, Supabase, Railway, RDS, etc.)

### Deploy

```bash
vercel login
vercel --prod
```

### Environment variables

**Database:** `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGHOST`, `PGPORT`

**Django:** `SECRET_KEY`, optionally `DJANGO_SETTINGS_MODULE=psytests.settings.vercel`

**Email (optional):** `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`

**Social auth (optional):** `GOOGLE_CLIENT_ID`, `GOOGLE_SECRET_KEY`, `FB_CLIENT_ID`, `FB_SECRET_KEY`

### After first deploy

```bash
vercel env pull .env.production
python manage.py migrate --settings=psytests.settings.vercel
```

Or use `deploy_prep.ps1` / `deploy_prep.sh` for local production smoke checks.

### Notes

- Static files: WhiteNoise + `build_files.sh` / `collectstatic`
- Health check: `GET /health/`
- Related files: `vercel.json`, `.vercelignore`, `runtime.txt`, `psytests/settings/vercel.py`

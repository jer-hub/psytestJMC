# Deployment

## Docker (recommended)

### Development

```bash
cp .env.example .env
docker compose up --build -d
```

Uses the `development` image target and `runserver` with a live bind mount.

### Production-style (Gunicorn)

```bash
cp .env.example .env
# Set strong SECRET_KEY, DB_PASSWORD, DJANGO_SUPERUSER_*, ALLOWED_HOSTS, DEBUG=0
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

The production target collects static files at build time and runs Gunicorn.

### Entrypoint behavior

On start, `docker/entrypoint.sh` typically:

1. Waits for PostgreSQL
2. Runs `migrate`
3. Ensures the Django `Site` row from `SITE_DOMAIN` / `SITE_NAME`
4. Optionally seeds fixtures when `SEED_DATA=1`
5. Creates a superuser when `DJANGO_SUPERUSER_*` vars are set

### Operations

```bash
docker compose logs -f web
docker compose exec web python manage.py check
docker compose exec web sh scripts/seed_data.sh
```

Health check: `GET http://<host>:<port>/health/`

Put a reverse proxy (Caddy, Nginx, Traefik) in front for TLS in real deployments. Compose alone exposes HTTP on `WEB_PORT`.

---

## Vercel

Configured for Django 4.2 with `psytests.settings.vercel` when `VERCEL` is set (`psytests/wsgi.py`).

### Prerequisites

- [Vercel CLI](https://vercel.com/docs/cli) (`npm i -g vercel`)
- External PostgreSQL (Vercel Postgres, Supabase, Railway, RDS, etc.)

### Deploy

```bash
vercel login
vercel --prod
```

### Environment variables

**Database:** `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGHOST`, `PGPORT`

**Django:** `SECRET_KEY` (required), optionally `DJANGO_SETTINGS_MODULE=psytests.settings.vercel`

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
- Related files: `vercel.json`, `.vercelignore`, `runtime.txt`, `psytests/settings/vercel.py`
- Serverless Django has limits (long requests, background jobs). Prefer Docker/VM hosting for heavy admin or large IQ image uploads.

---

## Checklist before go-live

1. Unique `SECRET_KEY` and database credentials
2. `DEBUG` off; correct `ALLOWED_HOSTS`
3. Migrations applied against the production database
4. Seed or import reference data as needed
5. Email delivery verified (activation + password reset)
6. OAuth redirect URIs match the public domain
7. `/health/` monitored
8. Backups scheduled for PostgreSQL

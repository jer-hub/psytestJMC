# Configuration

Copy `.env.example` to `.env` for local and Compose runs. **Never commit `.env` or real secrets.**

## Settings modules

| Variable / entrypoint | Module |
|-----------------------|--------|
| `manage.py` / Compose `web` (default) | `psytests.settings.dev` |
| `DEBUG=0` prod-style Compose overlay | still `dev` module with hardened flags via env |
| `psytests.settings.prod` | Requires `SECRET_KEY`, `ALLOWED_HOST` |
| `VERCEL` set / `psytests.settings.vercel` | Vercel serverless |

Prefer setting `DJANGO_SETTINGS_MODULE` explicitly in deployment environments.

## Environment variables

### Database (Compose / local Postgres)

| Variable | Default (example) | Purpose |
|----------|-------------------|---------|
| `DB_NAME` | `psytest_db` | Database name |
| `DB_USER` | `postgres` | Database user |
| `DB_PASSWORD` | `123` | Database password — **change in shared environments** |
| `DB_HOST` | `localhost` / `db` in Compose | Hostname |
| `DB_PORT` | `5432` | Port |
| `DB_PUBLISH_PORT` | `5432` | Host port published by Compose |

### Web / site

| Variable | Purpose |
|----------|---------|
| `WEB_PORT` | Host port mapped to the web container (default `8000`) |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `SITE_DOMAIN` | Domain for Django `sites` framework (e.g. `localhost:8000`) |
| `SITE_NAME` | Display name for the site row |
| `DEBUG` | `1` / `0` (dev settings) |
| `SECRET_KEY` | Django secret — **required for real deployments** |
| `SEED_DATA` | `1` to load fixtures on container start |
| `DJANGO_SUPERUSER_USERNAME` | Bootstrap admin username |
| `DJANGO_SUPERUSER_EMAIL` | Bootstrap admin email |
| `DJANGO_SUPERUSER_PASSWORD` | Bootstrap admin password |

### Email

| Variable | Purpose |
|----------|---------|
| `EMAIL_BACKEND` | Override backend (dev defaults to console) |
| `EMAIL_HOST_USER` | SMTP username |
| `EMAIL_HOST_PASSWORD` | SMTP password / App Password |

Defaults in `common.py` target Gmail SMTP (`smtp.gmail.com:587`, TLS) when the SMTP backend is active.

### OAuth (optional)

| Variable | Purpose |
|----------|---------|
| `GOOGLE_CLIENT_ID` | Google OAuth client ID |
| `GOOGLE_SECRET_KEY` | Google OAuth secret |
| `FB_CLIENT_ID` | Facebook app ID |
| `FB_SECRET_KEY` | Facebook app secret |

Configure matching redirect URIs in the provider consoles for your `SITE_DOMAIN`.

### Vercel / managed Postgres

| Variable | Purpose |
|----------|---------|
| `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGHOST`, `PGPORT` | Database URL parts |
| `SECRET_KEY` | Django secret |
| `DJANGO_SETTINGS_MODULE` | Often `psytests.settings.vercel` |

## Security checklist

- [ ] Unique `SECRET_KEY` outside the repo
- [ ] Strong `DB_PASSWORD` and superuser password
- [ ] `DEBUG=0` in production
- [ ] Correct `ALLOWED_HOSTS` / HTTPS termination
- [ ] Real SMTP or a transactional email provider for activation mail
- [ ] OAuth secrets only in the host secret store

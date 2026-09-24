# Development

## Prerequisites

- Python **3.10** (matches `requirements.txt` and the Docker image)
- PostgreSQL **15** (or use Compose’s `db` service)
- Docker Desktop / Compose (recommended), **or** a local Postgres instance

## Option A — Docker (recommended)

```bash
cp .env.example .env
docker compose up --build -d
docker compose logs -f web
```

Open http://127.0.0.1:8000/

The entrypoint waits for Postgres, runs migrations, ensures the Django `Site` row, optionally loads fixtures when `SEED_DATA=1`, and creates a superuser from env vars.

### Common Compose commands

```bash
docker compose exec web python manage.py check
docker compose exec web python manage.py test
docker compose exec web python manage.py createsuperuser
docker compose exec web sh scripts/seed_data.sh
docker compose down          # stop
docker compose down -v       # stop and remove DB volume
```

Code is bind-mounted (`.:/app`) in the development service, so template/CSS edits reload with `runserver`.

## Option B — Virtual environment

1. Create and activate a venv:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy env and point DB at your Postgres:

   ```bash
   cp .env.example .env
   ```

   Set `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT` as needed (`psytests/settings/dev.py`).

4. Migrate and run:

   ```bash
   python manage.py migrate
   sh scripts/seed_data.sh   # optional fixtures
   python manage.py createsuperuser
   python manage.py runserver
   ```

## Seeding data

Preferred path: Django fixtures via `scripts/seed_data.sh`.

Fixtures cover education levels, departments, programs, years, and sample questions for personality, RIASEC, and IQ.

CSV import management commands exist under each app for regenerating from `data/csv/` (see comments in `scripts/seed_data.sh`).

## Email in development

By default, `psytests.settings.dev` uses the **console** email backend. Activation and password-reset messages print to the web container / terminal logs.

To use Gmail SMTP locally, set in `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=…
EMAIL_HOST_PASSWORD=…   # App Password, not your normal password
```

## Front-end notes

- Shared admin manage styles: `static/css/admin-manage.css`
- Site navbar: `static/css/nav-css.css`
- Public home: `static/css/homepage.css`
- After CSS changes in Docker, hard-refresh the browser (templates bump `?v=` query strings where used)

## Checks before opening a PR

```bash
python manage.py check
python manage.py test
```

See [Contributing](../CONTRIBUTING.md).

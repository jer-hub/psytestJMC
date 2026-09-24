# PsytestJMC

Django platform for student psychological assessments: career interest (RIASEC), Big Five personality, and IQ testing — plus profiles, counselor administration, and analytics.

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

- Email registration with activation, password reset, and optional Google / Facebook login
- Student profiles (education level, department, program, year)
- **Career (RIASEC)** interest assessment and results
- **Personality (Big Five)** assessment with ML-assisted program recommendations
- **IQ** assessment with scored outcomes
- Post-test evaluation / feedback questionnaire
- Administration: organization structure, users/counselors, question banks, statistics
- Docker Compose for local/dev and Gunicorn production-style runs
- Health check endpoint for monitoring (`/health/`)

## Quick start (Docker)

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine + Compose).

```bash
git clone https://github.com/jer-hub/psytestJMC.git
cd psytestJMC
cp .env.example .env
docker compose up --build -d
```

| Resource | URL / value |
|----------|-------------|
| App | http://127.0.0.1:8000/ |
| Django admin | http://127.0.0.1:8000/admin/ |
| Default superuser | `admin` / `admin123` (from `.env`) |

Stop: `docker compose down`

## About

PsytestJMC (PSYTEST) supports student career, personality, and IQ assessments for academic advising.  
Read more in [docs/about.md](docs/about.md).

## Documentation

| Guide | Description |
|-------|-------------|
| [About](docs/about.md) | Purpose, audiences, and contact |
| [Architecture](docs/architecture.md) | Apps, request flow, data model overview |
| [Development](docs/development.md) | Local setup (Docker & venv), seeding, checks |
| [Configuration](docs/configuration.md) | Environment variables and settings modules |
| [Deployment](docs/deployment.md) | Docker production-style and Vercel |
| [Administration](docs/administration.md) | Counselor / admin console overview |
| [Contributing](CONTRIBUTING.md) | How to propose changes |
| [Security](SECURITY.md) | Reporting vulnerabilities |

## Tech stack

| Layer | Choice |
|-------|--------|
| Backend | Django 4.2 |
| Database | PostgreSQL 15 |
| Auth | django-allauth + social-auth |
| App server | Gunicorn (production image) |
| Static files | WhiteNoise |
| Front-end | Bootstrap 5, HTMX, Chart.js |
| ML | scikit-learn, pandas, joblib (`ml_artifacts/`) |
| Containers | Docker multi-stage build + Compose |

## Project layout

```text
psytests/          # Project settings, URLs, shared views
accounts/          # Registration, login, activation
userprofile/       # Profile & personal stats
riasec/            # Career (RIASEC) test
personality_test/  # Big Five test (app label: personalityTest)
iqtest/            # IQ test
evaluation/        # Post-assessment feedback
administration/    # Admin modules (org, users, tests, stats)
ml_artifacts/      # Trained recommendation model
data/              # Fixtures, CSV, SQL helpers
templates/         # Project-level templates
static/            # CSS, JS, images, icons
docker/            # Entrypoint and container helpers
docs/              # Extended documentation
scripts/           # Seed and utility scripts
```

## Useful URLs

| Path | Purpose |
|------|---------|
| `/` | Home |
| `/assessment/` | Assessment hub |
| `/auth/login/` | Login |
| `/profile/` | Student profile |
| `/career/test/` | Career test |
| `/personality/test/` | Personality test |
| `/iq/` | IQ test |
| `/evaluation/` | Feedback |
| `/administration/` | Staff console |
| `/admin/` | Django admin |
| `/health/` | Liveness check |

## Validation

```bash
# Host (venv) or: docker compose exec web …
python manage.py check
python manage.py test
```

## License

MIT — see [LICENSE](LICENSE).

# PsytestJMC

PsytestJMC is a Django-based psychological assessment platform for students.  
It combines multiple assessments (career interest, personality, and IQ), profile management, and administrative analytics in one system.

## What the system does

- User registration/login with email activation
- Social login support (Google and Facebook)
- Student profile and educational background management
- Career assessment (RIASEC)
- Personality assessment (Big Five) with program recommendation
- IQ assessment with scored results
- Post-assessment user evaluation/feedback
- Administrative pages for organization, user management, test management, and statistics
- Health endpoint for deployment monitoring (`/health/`)

## Tech stack

- **Backend:** Django 4.2
- **Database:** PostgreSQL
- **App server:** Gunicorn
- **Static file serving:** WhiteNoise
- **ML/Data libraries:** scikit-learn, pandas, joblib
- **Runtime:** Docker Compose (recommended) or local Python 3.10; Vercel documented for serverless deploy

## Project structure

- `psytests/` — project configuration, shared views, settings, URL routing
- `accounts/` — authentication, registration, profile bootstrap, activation flow
- `userprofile/` — profile editing and user stats pages
- `riasec/` — career-interest test questions, answers, and results
- `personality_test/` — personality test, scoring, recommendation logic (Django app label `personalityTest`)
- `iqtest/` — IQ questions, choices, answers, and result scoring
- `evaluation/` — feedback/rating questionnaire after assessments
- `administration/` — admin-facing modules (organization, users, career, personality, IQ, statistics)
- `ml_artifacts/` — serialized ML model used for program recommendations
- `data/fixtures/`, `data/csv/`, `data/sql/` — seed data and SQL helpers
- `templates/`, `static/` — project UI templates and assets
- `docker/`, `docker-compose.yml` — container runtime
- `docs/deployment.md` — Docker and Vercel deployment details

## Request flow (high-level)

1. User registers/logs in and completes profile information.
2. User takes one or more assessments (`/career/`, `/personality/`, `/iq/`).
3. Answers are persisted in app-specific `Answer` models.
4. Scores are computed and saved in app-specific `Result` models.
5. Personality results are passed to a trained model to recommend programs.
6. User sees consolidated outcomes through `/assessment/` and summary pages.

## Local development (Docker)

```bash
cp .env.example .env
docker compose up --build -d
```

App: http://127.0.0.1:8000/  
Default superuser (compose): `admin` / `admin123`

### Local development (venv)

> Use Python 3.10 to match `requirements.txt` / Docker image.

1. Clone the repository and enter it.
2. Create and activate a virtual environment.
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and configure Postgres (`DB_*` in `psytests/settings/dev.py`).
5. `python manage.py migrate`
6. Optionally: `sh scripts/seed_data.sh` and `python manage.py createsuperuser`
7. `python manage.py runserver`

## Validation commands

```bash
python manage.py check
python manage.py test
```

## Configuration

- Default settings: `psytests.settings.dev` (`manage.py`)
- Vercel settings: `psytests.settings.vercel` when `VERCEL` is set
- Env file: project-root `.env` (see `.env.example`)

## Deployment

See [docs/deployment.md](docs/deployment.md) for Docker and Vercel.

## Useful URLs

- Home: `/`
- Admin: `/admin/`
- Health check: `/health/`
- Auth: `/auth/login/`
- Profile: `/profile/`
- Career test: `/career/test/`
- Personality test: `/personality/test/`
- IQ test: `/iq/`
- Evaluation: `/evaluation/`
- Administration: `/administration/`

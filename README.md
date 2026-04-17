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
- **Deployment targets:** Vercel (documented), plus Docker/Procfile support

## Project structure

Top-level Django apps and modules:

- `psytests/` - project configuration, shared views, settings, URL routing
- `accounts/` - authentication, registration, profile bootstrap, activation flow
- `userprofile/` - profile editing and user stats pages
- `riasec/` - career-interest test questions, answers, and results
- `personalityTest/` - personality test, scoring, recommendation logic
- `iqtest/` - IQ questions, choices, answers, and result scoring
- `evaluation/` - feedback/rating questionnaire after assessments
- `administration/` - admin-facing modules (organization, users, career, personality, IQ, statistics)
- `models/` - serialized ML models (`.sav`) used for recommendations
- `templates/`, `static/`, `staticfiles/` - UI templates and assets

## Request flow (high-level)

1. User registers/logs in and completes profile information.
2. User takes one or more assessments (`/career/`, `/personality/`, `/iq/`).
3. Answers are persisted in app-specific `Answer` models.
4. Scores are computed and saved in app-specific `Result` models.
5. Personality results are passed to a trained model to recommend programs.
6. User sees consolidated outcomes through `/assessment/` and summary pages.

## Local development setup

> Recommended Python version is aligned with the project dependency set and deployment runtime (3.9/3.10).

1. Clone the repository and enter it.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure database settings for development (`psytests/settings/dev.py`) and ensure PostgreSQL is running.
5. Apply migrations:

```bash
python manage.py migrate
```

6. (Optional) Create admin user:

```bash
python manage.py createsuperuser
```

7. Run the server:

```bash
python manage.py runserver
```

## Validation commands

Run these before committing changes:

```bash
python manage.py check
python manage.py test
```

## Configuration and settings

- Default local settings module is `psytests.settings.dev` (see `manage.py`)
- Vercel production settings module is `psytests.settings.vercel`
- WSGI auto-selects Vercel settings when `VERCEL` environment variable is present

Important environment variables used in production:

- `SECRET_KEY`
- `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGHOST`, `PGPORT`
- `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
- `GOOGLE_CLIENT_ID`, `GOOGLE_SECRET_KEY`
- `FB_CLIENT_ID`, `FB_SECRET_KEY`

## Deployment notes

- See `README-DEPLOYMENT.md` and `DEPLOYMENT.md` for full Vercel setup.
- `vercel.json`, `build_files.sh`, and `psytests/settings/vercel.py` contain deployment-specific configuration.
- `Dockerfile` and `Procfile` are included for container/Gunicorn-based deployment workflows.

## Useful URLs

- Home: `/`
- Admin: `/admin/`
- Health check: `/health/`
- Auth: `/auth/`
- Profile: `/profile/`
- Career test: `/career/test/`
- Personality test: `/personality/test/`
- IQ test: `/iq/`
- Evaluation: `/evaluation/`
- Administration: `/administration/`


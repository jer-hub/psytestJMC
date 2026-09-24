# Architecture

## Overview

PsytestJMC is a multi-app Django project. Students authenticate, maintain a profile, take assessments, and view results. Staff use `/administration/` to manage organization data, test content, users, and aggregate statistics.

```text
Browser
  → Django URLs (psytests/urls.py)
    → accounts / userprofile / riasec / personality_test / iqtest / evaluation / administration
    → PostgreSQL
    → (personality) joblib model in ml_artifacts/
```

## Django apps

| App | Responsibility |
|-----|----------------|
| `psytests` | Settings packages, site-wide views (home, assessment hub, consent, health) |
| `accounts` | Sign-up, activation email, login, profile bootstrap signals |
| `userprofile` | Profile editing and per-user result summaries |
| `riasec` | Career interest questions, answers, RIASEC scoring |
| `personality_test` | Big Five items, scoring, program recommendation via ML |
| `iqtest` | IQ items (incl. rich text/images), choices, scoring |
| `evaluation` | Post-test feedback questionnaire |
| `administration` | Staff UI: organization, users, question banks, statistics |

## Assessment flow

1. User registers or signs in (optional social OAuth).
2. Profile fields (education level, department, program, year) are completed.
3. User opens `/assessment/` and starts a test (`/career/`, `/personality/`, `/iq/`).
4. Privacy consent gate may apply before the first run of a test.
5. Answers persist in each app’s `Answer` (or equivalent) models.
6. Results are computed and stored in each app’s `Result` models.
7. Personality results may be scored through a trained model to suggest programs.
8. Optional `/evaluation/` captures feedback after assessments.

## Administration modules

Under `/administration/`:

- **Organization** — education levels, year levels, departments, programs
- **Users** — search accounts and counselor permissions
- **Career / Personality / IQ** — manage questions and related content
- **Statistics** — filters and charts by assessment type
- **Interests** — RIASEC program interest mappings (career)

## Settings modules

| Module | Use |
|--------|-----|
| `psytests.settings.common` | Shared apps, middleware, auth, email, Quill, etc. |
| `psytests.settings.dev` | Local / Docker Compose (default in `manage.py`) |
| `psytests.settings.prod` | Stricter production (requires env secrets) |
| `psytests.settings.vercel` | Serverless Vercel runtime |

## Static & media

- Source assets live in `static/` and app `static/` folders.
- Development serves unhashed static files.
- Production image runs `collectstatic`; WhiteNoise serves them.
- Media uploads use `MEDIA_URL` / `MEDIA_ROOT` (see settings).

## Health check

`GET /health/` returns a simple success response for load balancers and uptime monitors.

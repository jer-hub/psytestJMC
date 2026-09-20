#!/bin/sh
set -e

echo "Waiting for database at ${DB_HOST:-db}:${DB_PORT:-5432}..."
python <<'PY'
import os
import time

import psycopg2

host = os.environ.get("DB_HOST", "db")
port = int(os.environ.get("DB_PORT", "5432"))
name = os.environ.get("DB_NAME", "psytest_db")
user = os.environ.get("DB_USER", "postgres")
password = os.environ.get("DB_PASSWORD", "123")

for attempt in range(60):
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=name,
            user=user,
            password=password,
        )
        conn.close()
        print("Database is ready.")
        break
    except psycopg2.OperationalError as exc:
        if attempt == 59:
            raise SystemExit(f"Database not ready: {exc}") from exc
        time.sleep(1)
PY

python manage.py migrate --noinput

python <<'PY'
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ.get("DJANGO_SETTINGS_MODULE", "psytests.settings.dev"))

import django

django.setup()

from django.contrib.sites.models import Site

domain = os.environ.get("SITE_DOMAIN", "localhost:8000")
name = os.environ.get("SITE_NAME", "psytestJMC")
site_id = int(os.environ.get("SITE_ID", "2"))

Site.objects.update_or_create(
    id=site_id,
    defaults={"domain": domain, "name": name},
)
print(f"Site ready: id={site_id} domain={domain}")
PY

if [ "${SEED_DATA:-0}" = "1" ]; then
  python <<'PY'
import os
import subprocess
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ.get("DJANGO_SETTINGS_MODULE", "psytests.settings.dev"))

import django

django.setup()

from accounts.models import EducationLevel

if EducationLevel.objects.exists():
    print("Seed data already present; skipping fixtures.")
    sys.exit(0)

fixtures = [
    "data/fixtures/educationlevel.json",
    "data/fixtures/department.json",
    "data/fixtures/program.json",
    "data/fixtures/year.json",
    "data/fixtures/personalitytest_question.json",
    "data/fixtures/riasec_question.json",
    "data/fixtures/riasec_offeredprogram.json",
    "data/fixtures/iqtest_question.json",
    "data/fixtures/choice.json",
]

for fixture in fixtures:
    print(f"Loading {fixture}...")
    subprocess.check_call([sys.executable, "manage.py", "loaddata", fixture])

print("Fixtures loaded.")
PY
fi

if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
  python <<'PY'
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ.get("DJANGO_SETTINGS_MODULE", "psytests.settings.dev"))

import django

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ["DJANGO_SUPERUSER_USERNAME"]
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@localhost")
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]

user, created = User.objects.get_or_create(
    username=username,
    defaults={"email": email, "is_staff": True, "is_superuser": True},
)
user.email = email
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()
print(("Created" if created else "Updated") + f" superuser: {username}")
PY
fi

exec "$@"

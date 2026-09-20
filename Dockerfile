# syntax=docker/dockerfile:1

FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY docker/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]


FROM base AS development

ENV DJANGO_SETTINGS_MODULE=psytests.settings.dev \
    DEBUG=1

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM base AS production

ENV DJANGO_SETTINGS_MODULE=psytests.settings.dev \
    DEBUG=0 \
    PORT=8000

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["sh", "-c", "gunicorn psytests.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120"]

#!/bin/bash

# Build the project
echo "Building the project..."
pip install -r requirements.txt

echo "Make migrations"
python3.9 manage.py makemigrations --noinput

echo "Migrate"
python3.9 manage.py migrate --noinput

echo "Collect static files"
python3.9 manage.py collectstatic --noinput --clear
